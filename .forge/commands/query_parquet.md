---
name: query_parquet
description: Executes a SQL query against the Parquet forensic timeline data using DuckDB. Automatically uses uv and handles output properly.
---

# Command: Query Parquet
# Description: Queries forensic artifacts and timeline data using DuckDB.

## Steps
1. Take the provided SQL query and case name.
2. Execute `uv run python3 helpers/query_parquet.py --case <case_name> --query "<query>"`
3. Review the output. If the output is large, suggest using an export flag or writing to a JSONL file.

## Usage Examples
```bash
uv run helpers/query_parquet.py --case SRL2018 --query "SELECT timestamp, imagename, message FROM artifacts_timeline LIMIT 10"
```
