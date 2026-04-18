#!/usr/bin/env uv run python
# Description: Run a DuckDB SQL query against the generated Parquet metadata.
# The table name is 'file_metadata'.
# Usage: query_parquet "<SQL_QUERY>"
# Example: query_parquet "SELECT count(*) FROM file_metadata"

import duckdb
import sys
import os
import pandas as pd


def main():
    if len(sys.argv) < 2:
        print('Usage: query_parquet "<SQL_QUERY>"')
        print('Example: query_parquet "SELECT * FROM file_metadata LIMIT 5"')
        sys.exit(1)

    query = sys.argv[1]
    parquet_path = "scratch/file_metadata.parquet"

    if not os.path.exists(parquet_path):
        print(
            f"[-] Error: Parquet file not found at {parquet_path}. Did you run 'convert_bodyfile'?"
        )
        sys.exit(1)

    try:
        # Connect to an in-memory database
        con = duckdb.connect(":memory:")

        # Register the parquet file as a view
        con.execute(
            f"CREATE VIEW file_metadata AS SELECT * FROM read_parquet('{parquet_path}')"
        )

        # Execute the agent's query
        print(f"[*] Executing DuckDB Query: {query}")
        df = con.execute(query).fetchdf()

        # Output results
        if df.empty:
            print("[+] Query returned no results.")
        else:
            print(df.to_string(index=False))

    except Exception as e:
        print(f"[-] DuckDB Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
