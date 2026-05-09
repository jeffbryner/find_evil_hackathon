---
name: query_parquet
description: uv run ./helpers/query_parquet.py executes a SQL query against the Parquet forensic artifact data using DuckDB.
---

# Command: Query Parquet
# Description: Queries forensic artifacts and timeline data using DuckDB.


## Prerequisites
- The query_parquet.py utility uses duckDB to gather all .parquet files in the scratch folder and presents them as queryable tables: `scratch/<CASEID>/**.parquet` files must have been generated.
   ```bash
   find ./scratch -type f | grep ".parquet" | wc -l 
   ```

## Steps
1. Take the provided SQL query and case name.
2. Execute `uv run helpers/query_parquet.py --case <case_name> --query "<query>"`
3. Review the output. If the output is large, suggest using the `--jsonl` option and piping to a JSONL file.


## Table Schemas:
View all available tables and their column schema via: 

```bash
uv run ./helpers/query_parquet.py --case <CASEID> --schema
```

## Basic Usage Examples

- Basic query
    ```bash
    uv run helpers/query_parquet.py --case <CASEID> --query "SELECT timestamp, imagename, message FROM artifacts_timeline"
    ```

- Output as jsonl
    ```bash
    uv run helpers/query_parquet.py --case <CASEID> --query "SELECT timestamp, imagename, message FROM artifacts_timeline" --jsonl
    ```

See `recipies.md` for more SQL examples.