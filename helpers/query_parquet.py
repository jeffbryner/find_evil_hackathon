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
        rows.append("| " + " | ".join(map(lambda x: str(x).replace("|", "\\|").replace("\n", " "), row.values)) + " |")
    
    return "\n".join([header, separator] + rows)

def main():
    parser = argparse.ArgumentParser(description="Query forensic Parquet artifacts using DuckDB.")
    parser.add_argument("--case", required=True, help="Name of the case (folder in scratch/)")
    parser.add_argument("--evidence", default="all", help="Name of the evidence folder or 'all' (default: all)")
    parser.add_argument("--query", help="SQL query to execute against the views")
    parser.add_argument("--schema", action="store_true", help="Display schema for available tables")
    parser.add_argument("--limit", type=int, default=1000, help="Maximum number of rows to return (default: 1000)")
    
    # Custom handling for positional query if --query is not provided and not just --schema
    args, unknown = parser.parse_known_args()
    if unknown and not args.query:
        args.query = " ".join(unknown)

    case_path = os.path.join("scratch", args.case)
    if not os.path.exists(case_path):
        print(f"[-] Error: Case directory not found: {case_path}")
        sys.exit(1)

    # Resolve parquet targets
    targets = get_parquet_files(case_path, args.evidence)
    
    if not targets:
        print(f"[-] Error: No Parquet files found for case '{args.case}' and evidence '{args.evidence}'")
        sys.exit(1)

    try:
        # Connect to an in-memory database
        con = duckdb.connect(":memory:")

        # Register views for each table type
        for table_name in targets.keys():
            # Enhancements for forensic usability:
            # 1. Alias columns with spaces (like 'File Name') for easier SQL access
            # 2. Add derived UTC timestamps for Plaso artifacts (microseconds to timestamp)
            select_clause = "*"
            if table_name == "fs_timeline":
                select_clause = '*, "File Name" AS file_name, "Date" AS date_str'
            elif table_name == "artifacts_timeline":
                select_clause = "*, to_timestamp(timestamp / 1000000) AS timestamp_utc"

            if args.evidence == "all":
                # For multiple evidence files, use read_parquet with union_by_name=True
                glob_pattern = os.path.join(case_path, "*", "parquet", f"{table_name}.parquet")
                con.execute(f"CREATE VIEW {table_name} AS SELECT {select_clause} FROM read_parquet('{glob_pattern}', filename='filename_path', union_by_name=True)")
            else:
                # Single evidence file
                fpath = targets[table_name][0]
                con.execute(f"CREATE VIEW {table_name} AS SELECT {select_clause} FROM read_parquet('{fpath}')")

        if args.schema:
            print(f"[*] Schema for Case: {args.case} (Evidence: {args.evidence})")
            for t_name in targets.keys():
                print(f"\nTable: {t_name}")
                schema_df = con.execute(f"DESCRIBE {t_name}").fetchdf()
                print(format_as_markdown(schema_df))
            
            if not args.query:
                sys.exit(0)

        if args.query:
            # Enforce limit if not already in query
            query = args.query.strip().rstrip(";")
            if "LIMIT" not in query.upper() and "DESCRIBE" not in query.upper():
                query += f" LIMIT {args.limit}"
            
            print(f"[*] Executing DuckDB Query: {query}")
            df = con.execute(query).fetchdf()

            if df.empty:
                print("[+] Query returned no results.")
            else:
                # Cap output even if LIMIT was higher, to avoid overwhelming context
                if len(df) > args.limit:
                    print(f"[!] Warning: Result set exceeded limit. Truncating to {args.limit} rows.")
                    df = df.head(args.limit)
                
                print(format_as_markdown(df))

    except Exception as e:
        print(f"[-] DuckDB Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
