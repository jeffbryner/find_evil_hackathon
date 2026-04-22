# Forensic Querying & Data Analysis

This skill provides the technical documentation and SQL recipes for analyzing forensic artifacts using the DuckDB/Parquet pipeline via the `query_parquet.py` utility.

## Core Utility: query_parquet.py

Use this utility to perform high-speed SQL analysis on artifacts extracted from the SIFT environment.

### Basic Usage
```bash
./helpers/query_parquet.py --case <case_name> --query "<SQL>"
```

### Key Flags
- `--case <name>`: **(Required)** Specifies the case folder in `scratch/`.
- `--evidence <name>|all`: Targets a specific host or aggregates all hosts in the case (Default: `all`).
- `--schema`: Displays available tables and columns for the case. **Always run this first if you are unsure of the schema.**
- `--limit <N>`: Limits output to N rows (Default: 1000).

## Table & Column Aliases
The utility automatically provides aliases to make SQL easier to write:
- **fs_timeline**:
    - `file_name`: Alias for `"File Name"` (removes space).
    - `filename_path`: Full path to the source parquet (useful for identifying the host when using `--evidence all`).
- **artifacts_timeline**:
    - `timestamp_utc`: Converts Plaso microseconds to a standard DuckDB timestamp.

## Investigative Recipes

Refer to the [Query Cookbook](references/recipes.md) for pre-written SQL snippets for:
1. Time-bucketed clustering.
2. MACB flag analysis.
3. Cross-host lateral movement detection.
4. Correlating process execution with file activity.

## Workflow Strategy
1. **Discover**: Run with `--schema` to see what artifacts were successfully extracted.
2. **Filter**: Use SQL to narrow down to a specific time window or artifact type (e.g., `WHERE parser LIKE '%Registry%'`).
3. **Correlate**: JOIN `fs_timeline` and `artifacts_timeline` to see what the system was doing when a specific file was created.
