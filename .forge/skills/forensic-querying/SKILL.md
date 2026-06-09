---
name: forensic-querying
description: This skill provides the technical documentation and SQL recipes for analyzing forensic artifacts using the DuckDB/Parquet pipeline via the `query_parquet.py` utility. Use this if asked to analyze forensic data, parquet files, or to perform SQL queries on forensic information including SQLite databases.
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
- `--query "<SQL>"`: **(Required)** The SQL query to execute.
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
| `filename_path` | VARCHAR | Path to the source host's parquet. |
| `imagename` | VARCHAR | Name of the forensic image file (disk/memory). Useful for joining tables. |

The `message` column is the primary way to communicate the essence of each event in a human-readable format. 
For the `fs_timeline` table, the `message` column will include filenames.
For the `artifacts_timeline` table the message column will include details about the artifact event such as:
```[HKEY_LOCAL_MACHINE\System\ControlSet002\Control\Session Manager\AppCompatCache] Cached entry: 415 Path: C:\Windows\WinSxS\x86_netfx35linq-linqwebconfig_31bf3856ad364e35_10.0.14393.0_none_286285a0465d978a\LinqWebConfig.exe```
For the log2timeline artifacts in the `artifacts_timeline` table, the `details` column contains a wealth of information that can be queried and analyzed such as sha hashes, registry key paths and other artifact-specific data.

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
WHERE data_type ILIKE 'windows:registry%';
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
JOIN iocs i ON f.message ILIKE '%' || i.value || '%';
```

## Querying SQLite Databases Natively in DuckDB

DuckDB has a built-in `sqlite_scan` function that allows querying SQLite database files directly without any conversion. This is extremely powerful for analyzing communication databases (like Skype `main.db`), browser databases, or other application SQLite files:

### ⚠️ MANDATORY INTEGRATION RULE: SQLite Scanning over Standalone CLI
Whenever analyzing SQLite databases (such as communication logs, or mail databases), **ALWAYS prefer using DuckDB's native SQLite scanning capabilities** (via the `sqlite` extension or `sqlite_scan`) over standalone SQLite command-line utilities.

**Why?**
1. **Timeline Synchronization:** It allows you to immediately correlate application-specific SQLite records (like chat messages or web visits) with system-wide timelines (`fs_timeline`, `artifacts_timeline`) in a single query.
2. **Unified Filtering:** You can apply case-insensitive `ILIKE` filters and regex extractions across both SQLite tables and Parquet files simultaneously.
3. **No Conversion Overhead:** You query the raw SQLite file in-place without needing to export or convert the data.

### Basic Syntax
```sql
SELECT * FROM sqlite_scan('path/to/database.db', 'table_name');
```

### Joining SQLite Data with Parquet Timelines
You can seamlessly join data from a local SQLite database with your Parquet-based filesystem timelines:
```sql
SELECT f.timestamp, f.message, s.author, s.body_xml
FROM fs_timeline f
JOIN sqlite_scan('cases/<CASEID>/scratch/skype/main.db', 'Messages') s 
  ON f.timestamp = epoch_to_timestamp(s.timestamp)
WHERE s.body_xml ILIKE '%secret%';
```

### Time-Window Correlation Query Example
Correlating a Skype message with a filesystem file creation within a 60-second window is extremely useful for proving exfiltration or malware execution timelines:
```sql
SELECT 
  f.timestamp AS file_event_time, 
  f.message AS file_action,
  s.message_time, 
  s.author, 
  s.body_xml 
FROM fs_timeline f
JOIN (
  SELECT 
    epoch_to_timestamp(timestamp) AS message_time, 
    author, 
    body_xml 
  FROM sqlite_scan('cases/<CASEID>/scratch/skype/main.db', 'Messages')
) s ON abs(epoch(f.timestamp) - epoch(s.message_time)) <= 60
WHERE f.file_name_lower ILIKE '%zip%' OR f.file_name_lower ILIKE '%exe%';
```



## Custom Event Schema Contract

When sub-agents parse custom databases or non-standard logs (such as a recovered Outlook PST email archive), they should format their extracted events to match the standardized timeline schema so they can be merged or queried alongside `fs_timeline` and `artifacts_timeline`.

| Column | Type | Description |
| --- | --- | --- |
| `timestamp` | TIMESTAMP | UTC event time (primary key for sorting/timeline reconstruction). |
| `source` | VARCHAR | Name of the custom parser or source (e.g., `pst_email_archive`). |
| `message` | VARCHAR | Primary human-readable summary (e.g., `Email from Maria Hill regarding Project ADAMANTIUM`). |
| `details` | JSON | JSON blob containing all other raw metadata (e.g., sender, recipient, attachments). |

By conforming to this schema and outputting to a Parquet file, you can easily perform `UNION ALL` or `JOIN` operations against other system timelines.

## End-to-End Pipeline Quick-Reference
Use this table to map common forensic objectives to Dissect target-query modules, their corresponding Parquet outputs, and the standard SQL queries to analyze them:

| Forensic Objective | Dissect Plugin | Target Parquet File | Recommended Query |
| --- | --- | --- | --- |
| **Browser History** | `browser.history` | `browser_history.parquet` | `SELECT url, title, visit_count FROM browser_history ORDER BY visit_count DESC;` |
| **User Accounts** | `users` | `users.parquet` | `SELECT name, sid, home, shell FROM users;` |
| **Installed Apps** | `apps` | `installed_apps.parquet` | `SELECT name, version, install_date FROM installed_apps;` |
| **LSA Secrets** | `lsa.secrets` | `lsa_secrets.parquet` | `SELECT name, secret_type, value FROM lsa_secrets;` |
| **Browser Logins** | `browser.passwords` | `browser_passwords.parquet` | `SELECT url, username, password FROM browser_passwords;` |
| **Run Keys** | `registry.run` | `run_keys.parquet` | `SELECT key_path, name, value FROM run_keys;` |

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
- **Discover**: Run  `uv run helpers/query_parquet.py --case <CASEID> --schema` to see what artifacts were successfully extracted. Tables with 'memory' in the name are from volatility and will not include a json/details column.
- **Filter**: Use SQL to narrow down to a specific time window or artifact type (e.g., `WHERE parser ILIKE '%Registry%'`).
- **Mandatory Case-Insensitive Queries (ILIKE)**: ALWAYS use `ILIKE` instead of `LIKE` when searching for file paths, names, extensions, registry keys, URLs, or other text strings to prevent missing critical evidence due to case mismatch. NEVER use `lower(field) LIKE '%value%'` as it is inefficient, verbose, and unnecessary in DuckDB.
- **Correlate**: JOIN `fs_timeline` and `artifacts_timeline` on `timestamp` to see what the system was doing when a specific file was created.
- **Treat Raw SQLite as Tables**: Do not isolate SQLite databases. Use `sqlite_scan('path/to/db', 'table')` directly in your DuckDB queries to keep your investigation unified and synchronize chat/browser databases with system timelines.
- **Unified View**: Using `--evidence all` (or omitting `--evidence`) will include all evidence from all hosts. This coupled with targeted queries for filenames, or other features will show you correlated entries across all hosts in question. 
- **Forbid Inline Scripting for Output Parsing**: NEVER use inline Python (`python3 -c "..."`) and Regex to scrape or parse truncated terminal output. If a query returns long strings (like Base64 PowerShell commands or JSON blobs) that get truncated, you MUST use structured output formats (like JSONL) or DuckDB's native export functions to save the full results to a file in the `scratch/` directory for analysis.
- **Maximize Native SQL**: Leverage DuckDB's native string manipulation, regex extraction (`regexp_extract`), and decoding functions (`from_base64`) directly within your SQL queries to process data efficiently, rather than pulling raw data into Python for processing.
- **Avoid Rabbit Holes (Fail-Fast)**: If a query returns no results after initial attempts, or if the required table/evidence does not exist, stop querying. Do not blindly guess table names or run unconstrained wildcard searches across the entire database. Return a concise report stating that the artifact was not found, what you tried and move on. Respect any "max attempts" or "time-box" constraints given to you in your task description.
