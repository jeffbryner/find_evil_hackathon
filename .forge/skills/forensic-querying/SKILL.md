---
name: forensic-querying
description: Using the querying utilities and the prepared duckDB instance for querying/analyzing forensic artifacts.
---
# Forensic Querying & Data Analysis

This skill provides the technical documentation and SQL recipes for analyzing forensic artifacts using the DuckDB/Parquet pipeline via the `query_parquet.py` utility.

## Core Utility: query_parquet.py

Use this utility to perform high-speed SQL analysis on artifacts extracted from the SIFT environment.

### Basic Usage
```bash
uv run ./helpers/query_parquet.py --case <case_name> --query "<SQL>"
```

### Key Flags
- `--case <name>`: **(Required)** Specifies the case folder in `scratch/`.
- `--evidence <name>|all`: Targets a specific host or aggregates all hosts in the case (Default: `all`).
- `--schema`: Displays available tables and columns for the case. **Always run this first if you are unsure of the schema.**
- `--limit <N>`: Limits output to N rows (Default: 50).
- `--jsonl`: Outputs results as JSON Lines (.jsonl). **Preferred for programmatic parsing by agents**, especially when dealing with long strings or complex data. (Note: status/info messages will go to stderr when --jsonl is chosen)

## Core Schema
Filesystem timelines (`fs_timeline`, `artifacts_timeline`) share a standardized core schema for easy correlation:

| Column | Type | Description |
| --- | --- | --- |
| `timestamp` | TIMESTAMP | UTC event time. Primary sort/filter key. |
| `data_type` | VARCHAR | High-level artifact type (e.g., `windows:registry:run`, `fs:mactime`). |
| `parser` | VARCHAR | The tool/parser that extracted the event (e.g., `mactime`, `winreg/run`). |
| `message` | VARCHAR | Primary human-readable summary. |
| `file_name_lower` | VARCHAR | Lowercased path/filename for case-insensitive searching. |
| `details` | JSON | A JSON blob containing all other artifact-specific fields. |
| `filename_path` | VARCHAR | (Only when using `--evidence all`) Path to the source host's parquet. |


Memory artifacts from volatility will reside in `memory_` tables like memory_pslist, memory_netscan, memory_timeliner and each carry their own schema. 

The `imagename` column in every table can be used to join tables together to find evidence from a forensic image (disk/memory).
```
uv run ./helpers/query_parquet.py --case <CASEID> --query "SELECT * from memory_pslist p join memory_netscan n on p.imagename=p.imagename " --limit 2 --jsonl
```


## Querying JSON Details
To extract specific fields from the `details` column, use the DuckDB JSON operator `->>`:
```sql
SELECT message, details->>'key_path' as key_path 
FROM artifacts_timeline 
WHERE data_type LIKE 'windows:registry%';
```

## Tracking and Querying IOCs

You can share Indicators of Compromise (IOCs) between agents using `ioc_tracker.py` and query them alongside your forensic data.

### Adding an IOC
To track a new IOC (e.g., an IP found in memory or a malicious hash), use the tracker helper:
```bash
# Example: uv run helpers/ioc_tracker.py --case SRL --add ip --value 199.73.28.114 --source memory_netscan
uv run helpers/ioc_tracker.py --case <case_name> --add <type> --value <ioc_value> --source <context>

```

### Querying IOCs
If IOCs have been added for a case, a special `iocs` view is automatically available in DuckDB. You can query it directly or join it with your artifact tables:

```sql
-- View all tracked IOCs
SELECT * FROM iocs;

-- Find filesystem activity related to known IOCs
SELECT f.timestamp, f.message, i.type, i.value as matched_ioc
FROM fs_timeline f
JOIN iocs i ON f.message LIKE '%' || i.value || '%';
```

## Investigative Recipes

Refer to the [Query Cookbook](references/recipes.md) for pre-written SQL snippets for:
1. Time-bucketed clustering.
2. MACB flag analysis.
3. Cross-host lateral movement detection.
4. Correlating process execution with file activity.
5. Joining dynamic IOCs with static timelines.
6. JSONL and Structured Output handling.
7. Advanced DuckDB querying (Base64 decoding, JSON parsing).

## Workflow Strategy
- **Discover**: Run with `--schema` to see what artifacts were successfully extracted. Tables with 'memory' in the name are from volatility and will not include a json/details column.
- **Filter**: Use SQL to narrow down to a specific time window or artifact type (e.g., `WHERE parser LIKE '%Registry%'`).
- **Correlate**: JOIN `fs_timeline` and `artifacts_timeline` on `timestamp` to see what the system was doing when a specific file was created.
- **Unified View**: Using --evidence all (or omitting evidence) will include all evidence from all hosts. This coupled with targeted queries for filenames, or other features will show you correlated entries across all hosts in question. 
- **Forbid Inline Scripting for Output Parsing**: NEVER use inline Python (`python3 -c "..."`) and Regex to scrape or parse truncated terminal output. If a query returns long strings (like Base64 PowerShell commands or JSON blobs) that get truncated, you MUST use structured output formats (like JSONL) or DuckDB's native export functions to save the full results to a file in the `scratch/` directory for analysis.
- **Maximize Native SQL**: Leverage DuckDB's native string manipulation, regex extraction (`regexp_extract`), and decoding functions (`from_base64`) directly within your SQL queries to process data efficiently, rather than pulling raw data into Python for processing.