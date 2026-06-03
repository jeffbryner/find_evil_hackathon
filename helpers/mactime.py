#!/usr/bin/env python3
import sys
import argparse
import duckdb
import urllib.parse
import os


def unquote_path(x):
    if not isinstance(x, str):
        return x
    return urllib.parse.unquote(x)


def main():
    parser = argparse.ArgumentParser(
        description="mactime replacement in python using duckdb"
    )
    parser.add_argument("-b", "--bodyfile", required=True, help="body file location")
    parser.add_argument(
        "-d", action="store_true", help="Output in comma delimited format"
    )
    parser.add_argument("-z", "--timezone", help="Timezone (ignored, assumed UTC)")

    args = parser.parse_args()

    if not os.path.exists(args.bodyfile):
        print(f"Error: Bodyfile {args.bodyfile} not found.", file=sys.stderr)
        sys.exit(1)

    if os.path.getsize(args.bodyfile) == 0:
        # Bodyfile is empty. Just output the header line and exit 0.
        print("Date,Size,Type,Mode,UID,GID,Meta,File Name")
        sys.exit(0)

    con = duckdb.connect(database=":memory:")
    con.create_function("unquote_path", unquote_path, ["VARCHAR"], "VARCHAR")

    # Read the bodyfile
    # MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime
    try:
        con.execute(f"""
            CREATE TABLE body AS 
            SELECT 
                column00 AS md5,
                unquote_path(column01) AS name,
                column02 AS inode,
                column03 AS mode,
                column04 AS uid,
                column05 AS gid,
                column06 AS size,
                CAST(column07 AS BIGINT) AS atime,
                CAST(column08 AS BIGINT) AS mtime,
                CAST(column09 AS BIGINT) AS ctime,
                CAST(column10 AS BIGINT) AS crtime
            FROM read_csv('{args.bodyfile}', delim='|', header=False, quote='', ignore_errors=True);
        """)
    except Exception as e:
        # If it failed to read because it's invalid or empty, print the header and exit 0
        print(
            f"Warning: Bodyfile is invalid or empty ({e}). Writing header-only timeline.",
            file=sys.stderr,
        )
        print("Date,Size,Type,Mode,UID,GID,Meta,File Name")
        sys.exit(0)

    # Unpivot timestamps
    con.execute("""
        CREATE TABLE events AS
        SELECT mtime AS ts, 'm' AS activity, inode, name, mode, uid, gid, size FROM body WHERE mtime IS NOT NULL AND mtime > 0
        UNION ALL
        SELECT atime AS ts, 'a' AS activity, inode, name, mode, uid, gid, size FROM body WHERE atime IS NOT NULL AND atime > 0
        UNION ALL
        SELECT ctime AS ts, 'c' AS activity, inode, name, mode, uid, gid, size FROM body WHERE ctime IS NOT NULL AND ctime > 0
        UNION ALL
        SELECT crtime AS ts, 'b' AS activity, inode, name, mode, uid, gid, size FROM body WHERE crtime IS NOT NULL AND crtime > 0;
    """)

    # Group by timestamp and file metadata
    con.execute("""
        CREATE TABLE grouped_events AS
        SELECT 
            ts,
            size,
            list_aggregate(list(activity), 'string_agg', '') AS act_list,
            mode,
            uid,
            gid,
            inode,
            name
        FROM events
        GROUP BY ts, inode, name, mode, uid, gid, size
    """)

    # mactime date format: Mon Jan 01 2024 00:00:00
    # Type is MACB string
    export_query = """
    SELECT 
        strftime(to_timestamp(ts), '%a %b %d %Y %H:%M:%S') AS Date,
        size AS Size,
        (CASE WHEN contains(act_list, 'm') THEN 'm' ELSE '.' END ||
         CASE WHEN contains(act_list, 'a') THEN 'a' ELSE '.' END ||
         CASE WHEN contains(act_list, 'c') THEN 'c' ELSE '.' END ||
         CASE WHEN contains(act_list, 'b') THEN 'b' ELSE '.' END) AS Type,
        mode AS Mode,
        uid AS UID,
        gid AS GID,
        inode AS Meta,
        name AS "File Name"
    FROM grouped_events
    ORDER BY ts, name, inode
    """

    if args.d:
        # CSV output
        con.execute(
            f"COPY ({export_query}) TO '/dev/stdout' (HEADER, DELIMITER ',', QUOTE '\"', FORMAT CSV)"
        )
    else:
        # Tabular output (similar to mactime default) - for now just CSV as triage_extractor uses -d
        con.execute(
            f"COPY ({export_query}) TO '/dev/stdout' (HEADER, DELIMITER ',', QUOTE '\"', FORMAT CSV)"
        )


if __name__ == "__main__":
    main()
