#!/usr/bin/env uv run python
# Description: Redesigned DuckDB SQL query utility for AI Forensic Agents.
# Supports dynamic case context, multi-evidence aggregation, and schema discovery.
# Usage: ./helpers/query_parquet.py --case <case_name> [--evidence <evidence_name>|all] [--query <SQL_QUERY>] [--schema] [--limit 1000]

import duckdb
import argparse
import sys
import os
import glob
import pandas as pd


def get_parquet_files(case_path: str, evidence: str) -> dict:
    """
    Returns a dictionary mapping table names to glob patterns or file paths.
    """
    targets = {}

    if evidence == "all":
        # Target all evidence folders in the case
        search_pattern = os.path.join(case_path, "*", "parquet", "*.parquet")
    else:
        # Target a specific evidence folder
        search_pattern = os.path.join(case_path, evidence, "parquet", "*.parquet")

    found_files = glob.glob(search_pattern)

    # Group by filename (e.g., fs_timeline.parquet -> table name: fs_timeline)
    for fpath in found_files:
        fname = os.path.basename(fpath)
        table_name = os.path.splitext(fname)[0]

        if table_name not in targets:
            targets[table_name] = []
        targets[table_name].append(fpath)

    return targets


def format_jsonl(df: pd.DataFrame, strict: bool) -> str:
    """
    Formats a pandas DataFrame as JSON Lines, optionally removing strict slash escapes
    for AI-friendly readability.
    """
    json_out = df.to_json(orient="records", lines=True, date_format="iso")
    if not strict:
        # Strip out standard JSON escapes for forward/backslashes to be more readable for AI agents
        json_out = json_out.replace("\\\\", "\\").replace("\\/", "/")
    return json_out


def format_as_markdown(df: pd.DataFrame) -> str:
    """
    Formats a pandas DataFrame as a Markdown table.
    """
    if df.empty:
        return "No results found."

    # Simple markdown table formatter
    header = "| " + " | ".join(map(str, df.columns)) + " |"
    separator = "| " + " | ".join(["---"] * len(df.columns)) + " |"

    rows = []
    for _, row in df.iterrows():
        rows.append(
            "| "
            + " | ".join(
                map(lambda x: str(x).replace("|", "\\|").replace("\n", " "), row.values)
            )
            + " |"
        )

    return "\n".join([header, separator] + rows)


def main():
    parser = argparse.ArgumentParser(
        description="Query forensic Parquet artifacts using DuckDB."
    )
    parser.add_argument(
        "--case", required=True, help="Name of the case (folder in scratch/)"
    )
    parser.add_argument(
        "--evidence",
        default="all",
        help="Name of the evidence folder or 'all' (default: all)",
    )
    parser.add_argument("--query", help="SQL query to execute against the views")
    parser.add_argument(
        "--schema", action="store_true", help="Display schema for available tables"
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of rows to return (default: 50)",
    )
    parser.add_argument(
        "--jsonl", action="store_true", help="Output results as JSON Lines (.jsonl)"
    )
    parser.add_argument(
        "--strict-jsonl",
        action="store_true",
        help="Do not remove slash escaping in JSONL output (keeps strict JSON formatting)",
    )

    # Custom handling for positional query if --query is not provided and not just --schema
    args, unknown = parser.parse_known_args()
    if unknown and not args.query:
        args.query = " ".join(unknown)

    case_path = os.path.join("scratch", args.case)
    if not os.path.exists(case_path):
        print(f"[-] Error: Case directory not found: {case_path}", file=sys.stderr)
        sys.exit(1)

    # Resolve parquet targets
    targets = get_parquet_files(case_path, args.evidence)

    if not targets and not os.path.exists(os.path.join(case_path, "iocs.jsonl")):
        print(
            f"[-] Error: No forensic artifacts found for case '{args.case}'",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        # Connect to an in-memory database
        con = duckdb.connect(":memory:")

        # Register IOCs view if it exists
        iocs_path = os.path.join(case_path, "iocs.jsonl")
        if os.path.exists(iocs_path):
            con.execute(
                f"CREATE VIEW iocs AS SELECT * FROM read_json_auto('{iocs_path}')"
            )

        # Register views for each table type
        for table_name in targets.keys():
            # The triage_extractor now provides a consistent, optimized schema:
            # (timestamp, data_type, parser, message, file_name_lower, details)
            # include the source image filename without path for joining across datasets
            select_clause = "*, string_split(filename_path, '/')[-3] AS imagename"

            if args.evidence == "all":
                # For multiple evidence files, use read_parquet with union_by_name=True
                glob_pattern = os.path.join(
                    case_path, "*", "parquet", f"{table_name}.parquet"
                )
                con.execute(
                    f"CREATE VIEW {table_name} AS SELECT {select_clause} FROM read_parquet('{glob_pattern}', filename='filename_path', union_by_name=True)"
                )
            else:
                # Single evidence file
                fpath = targets[table_name][0]
                con.execute(
                    f"CREATE VIEW {table_name} AS SELECT {select_clause} FROM read_parquet('{fpath}', filename='filename_path')"
                )

        if args.schema:
            if not args.jsonl:
                print(f"[*] Schema for Case: {args.case} (Evidence: {args.evidence})")

            # Show IOCs schema if it exists
            iocs_path = os.path.join(case_path, "iocs.jsonl")
            if os.path.exists(iocs_path):
                schema_df = con.execute("DESCRIBE iocs").fetchdf()
                if args.jsonl:
                    schema_df["table"] = "iocs"
                    print(format_jsonl(schema_df, args.strict_jsonl))
                else:
                    print("\nTable: iocs")
                    print(format_as_markdown(schema_df))

            for t_name in targets.keys():
                schema_df = con.execute(f"DESCRIBE {t_name}").fetchdf()
                if args.jsonl:
                    schema_df["table"] = t_name
                    print(format_jsonl(schema_df, args.strict_jsonl))
                else:
                    print(f"\nTable: {t_name}")
                    print(format_as_markdown(schema_df))

            if not args.query:
                sys.exit(0)

        if args.query:
            # Enforce limit if not already in query
            query = args.query.strip().rstrip(";")
            if "LIMIT" not in query.upper() and "DESCRIBE" not in query.upper():
                query += f" LIMIT {args.limit}"

            if not args.jsonl:
                print(f"[*] Executing DuckDB Query: {query}")
            else:
                print(f"[*] Executing DuckDB Query: {query}", file=sys.stderr)

            df = con.execute(query).fetchdf()

            if df.empty:
                if not args.jsonl:
                    print("[+] Query returned no results.")
                else:
                    print("[+] Query returned no results.", file=sys.stderr)
            else:
                # Cap output even if LIMIT was higher, to avoid overwhelming context
                if len(df) > args.limit:
                    if not args.jsonl:
                        print(
                            f"[!] Warning: Result set exceeded limit. Truncating to {args.limit} rows."
                        )
                    else:
                        print(
                            f"[!] Warning: Result set exceeded limit. Truncating to {args.limit} rows.",
                            file=sys.stderr,
                        )
                    df = df.head(args.limit)

                if args.jsonl:
                    print(format_jsonl(df, args.strict_jsonl))
                else:
                    print(format_as_markdown(df))

    except Exception as e:
        print(f"[-] DuckDB Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
