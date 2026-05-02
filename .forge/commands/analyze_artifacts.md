---
name: analyze_artifacts
description: "Use DuckDB to run SQL queries against the extracted file metadata to find forensic anomalies."
--- 

# Command: Analyze Artifacts
# Description: Uses query_parquet.py and duckDB to run SQL queries against the extracted forensic data to find forensic anomalies.

Perform ad-hoc queries based on findings to follow investigative leads.

## Prerequisites
- The query_parquet.py utility uses duckDB to gather all .parquet files in the scratch folder and presents them as queryable tables: `scratch/<CASEID>/**.parquet` files must have been generated.
   ```bash
   find ./scratch -type f | grep ".parquet" | wc -l 
   ```


## Examples
- Use `query_parquet.py` to run SQL queries via uv
   ```bash
   uv run ./helpers/query_parquet.py --help
   ```
- Examine the schemas availble to you from previous forensic artifact recovery:
   ```bash
   uv run ./helpers/query_parquet.py --case <CASEID> --schema
   ```
- Investigate common persistence locations:
   ```bash
   uv run ./helpers/query_parquet.py --case <CASEID> "SELECT file_path, mtime FROM file_metadata WHERE file_path ILIKE '%CurrentVersion/Run%' LIMIT 10"
   ```
- Look for suspicious executables in Temp or AppData:
   ```bash
   uv run ./helpers/query_parquet.py --case <CASEID> "SELECT file_path, size, crtime FROM file_metadata WHERE file_path ILIKE '%/Temp/%.exe' ORDER BY crtime DESC LIMIT 10"
   ```

## Table Schemas:
View all available tables via: 
```bash
   uv run ./helpers/query_parquet.py --case <CASEID> --schema
```