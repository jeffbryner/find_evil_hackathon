import os
import sys
import json
import argparse
import pyarrow as pa
import pyarrow.parquet as pq
from datetime import datetime, timezone
import sqlite3
import zlib


def convert_plaso_to_parquet(plaso_path, parquet_path, batch_size=50000):
    print(f"Reading from {plaso_path}...")

    # Connect directly via sqlite3 to avoid heavy plaso/dfvfs/pytsk3 dependencies locally
    conn = sqlite3.connect(plaso_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    schema = pa.schema(
        [
            ("timestamp", pa.timestamp("us")),
            ("data_type", pa.string()),
            ("parser", pa.string()),
            ("message", pa.string()),
            ("display_name", pa.string()),
            ("file_name_lower", pa.string()),
            ("tag", pa.string()),
            ("details", pa.string()),  # JSON string
        ]
    )

    writer = pq.ParquetWriter(parquet_path, schema, compression="snappy")

    batch = []
    count = 0

    try:
        # Join event and event_data to get the core fields
        # Plaso stores serialized data in 'event_data' table, column '_data' (zlib compressed JSON)
        # 'event' table has the timestamp and links to 'event_data' via '_event_data_identifier'
        query = """
        SELECT 
            e.timestamp, 
            e.timestamp_desc,
            ed._data AS serialized_data
        FROM event e
        JOIN event_data ed ON e._event_data_identifier = 'event_data.' || ed._identifier
        ORDER BY e.timestamp ASC
        """

        cursor.execute(query)

        for row in cursor:
            try:
                # Plaso stores serialized data as zlib compressed JSON strings
                data_json = zlib.decompress(row["serialized_data"]).decode("utf-8")
                event_data = json.loads(data_json)
            except Exception as e:
                # print(f"Error decompressing/parsing event data: {e}")
                continue

            # 1. Basic Fields
            data_type = event_data.get("data_type", "N/A")
            parser = event_data.get("_parser_chain", "N/A")
            display_name = event_data.get("display_name", "N/A")

            # 2. Message (without Plaso formatters, we use a fallback)
            # Future improvement: implement some common formatters locally if needed
            message = (
                event_data.get("message")
                or event_data.get("body")
                or event_data.get("filename")
            )

            if not message or message == "N/A":
                # Try to build a message from common fields
                if data_type.startswith("windows:registry"):
                    key_path = event_data.get("key_path", "")
                    value_name = event_data.get("value_name", "")
                    value_data = event_data.get("value_data", "")
                    message = f"Registry: {key_path}\\{value_name} = {value_data}"
                elif data_type.startswith("windows:evtx"):
                    source = event_data.get("source_name", "")
                    event_id = event_data.get("event_identifier", "")
                    message = f"EventLog: [{source}] ID {event_id}"
                elif data_type == "fs:stat":
                    filename = event_data.get("filename", "")
                    message = f"File Stat: {filename}"
                elif data_type == "windows:prefetch:execution":
                    executable = event_data.get("executable", "")
                    run_count = event_data.get("run_count", "")
                    message = f"Prefetch: {executable} executed {run_count} times"
                elif data_type == "windows:volume:creation":
                    device_path = event_data.get("device_path", "")
                    serial_number = event_data.get("serial_number", "")
                    message = f"Volume Created: {device_path} (S/N: {serial_number})"
                else:
                    message = display_name or "N/A"

            # 3. File Name Lower
            filename = event_data.get("filename")
            file_name_lower = (filename or display_name or "").lower()

            # 4. Tags (Plaso stores tags in separate tables, usually 'event_tag')
            # For simplicity in this standalone version, we'll skip tags unless we want more queries
            tag_str = ""

            # 5. Details (JSON) - Everything else
            excluded = {
                "timestamp",
                "data_type",
                "_parser_chain",
                "message",
                "filename",
                "display_name",
                "parser",
                "tag",
                "__type__",
                "__container_type__",
            }

            details_dict = {
                k: str(v)
                for k, v in event_data.items()
                if k not in excluded and not k.startswith("_")
            }
            details_dict["timestamp_desc"] = row["timestamp_desc"]
            details_json = json.dumps(details_dict)

            # 6. Timestamp
            # event.timestamp is in microseconds (Unix Epoch)
            try:
                # Convert to UTC and then remove timezone info to match requested format
                ts = datetime.fromtimestamp(
                    row["timestamp"] / 1000000, tz=timezone.utc
                ).replace(tzinfo=None)
            except (ValueError, OSError, OverflowError):
                ts = datetime(1970, 1, 1)

            batch.append(
                {
                    "timestamp": ts,
                    "data_type": data_type,
                    "parser": parser,
                    "message": message,
                    "display_name": display_name,
                    "file_name_lower": file_name_lower,
                    "tag": tag_str,
                    "details": details_json,
                }
            )

            count += 1
            if len(batch) >= batch_size:
                table = pa.Table.from_pylist(batch, schema=schema)
                writer.write_table(table)
                batch = []
                print(f"Processed {count} events...")

        if batch:
            table = pa.Table.from_pylist(batch, schema=schema)
            writer.write_table(table)
            print(f"Processed {count} events total.")

    finally:
        conn.close()
        writer.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Convert .plaso to .parquet (Standalone version)"
    )
    parser.add_argument("plaso_file", help="Input .plaso file")
    parser.add_argument("parquet_file", help="Output .parquet file")
    parser.add_argument(
        "--batch-size", type=int, default=50000, help="Batch size for writing"
    )

    args = parser.parse_args()

    if not os.path.exists(args.plaso_file):
        print(f"Error: {args.plaso_file} not found.")
        sys.exit(1)

    convert_plaso_to_parquet(args.plaso_file, args.parquet_file, args.batch_size)
