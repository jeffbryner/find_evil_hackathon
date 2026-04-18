---
name: analyze_artifacts
description: "Use DuckDB to run SQL queries against the extracted file metadata to find forensic anomalies."
--- 

# Command: Analyze Artifacts
# Description: Use DuckDB to run SQL queries against the extracted file metadata to find forensic anomalies.

## Prerequisites
- `scratch/file_metadata.parquet` must have been generated.

## Steps
1. Use `query_parquet.py` to run SQL queries. The table name is `file_metadata`.
2. Investigate common persistence locations:
   ```bash
   ./helpers/query_parquet.py "SELECT file_path, mtime FROM file_metadata WHERE file_path ILIKE '%CurrentVersion/Run%' LIMIT 10"
   ```
3. Look for suspicious executables in Temp or AppData:
   ```bash
   ./helpers/query_parquet.py "SELECT file_path, size, crtime FROM file_metadata WHERE file_path ILIKE '%/Temp/%.exe' ORDER BY crtime DESC LIMIT 10"
   ```
4. Perform ad-hoc queries based on findings to follow investigative leads.

## Table Schema: file_metadata
| Column | Description |
|---|---|
| md5 | File MD5 hash |
| file_path | Full path |
| inode | Filesystem inode |
| mode | Permissions/Type |
| size | File size in bytes |
| atime | Access time |
| mtime | Modification time |
| ctime | Change time |
| crtime | Creation time |
