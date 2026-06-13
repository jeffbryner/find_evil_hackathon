# Forensic Querying Cookbook

Use these SQL recipes as templates for common investigative tasks.

## Case insensitive querying
ALWAYS use the `ILIKE` SQL statement instead of simply using `LIKE` and having to worry about case sensitivity.
```sql
SELECT timestamp, message as file_name, details->>'Type' as macb from fs_timeline where message ILIKE '%.zip'
```

## Time-Window Clustering
Find bursts of activity (e.g., more than X events per minute) to identify periods of intense attacker activity.
```sql
SELECT 
    date_trunc('hour', timestamp) as hour_bucket, 
    count(*) as event_count,
    string_agg(DISTINCT parser, ', ') as artifact_types
FROM artifacts_timeline
GROUP BY 1
HAVING event_count > 1000
ORDER BY event_count DESC;
```

## MACB Flag Filtering (Filesystem)
Find files that were "Created" (b) or "Modified" (m) in a specific directory.
```sql
SELECT timestamp, message as file_name, details->>'Type' as macb
FROM fs_timeline
WHERE details->>'Type' ILIKE '%b%' 
  AND file_name_lower ILIKE '/windows/system32/%'
ORDER BY timestamp DESC;
```

## Lateral Movement Detection (Cross-Host)
Find the same suspicious file name appearing across multiple evidence images from hosts in the case.
```sql
SELECT 
    file_name_lower, 
    count(DISTINCT imagename) as image_count,
    string_agg(imagename, ', ') as image_names
FROM fs_timeline
WHERE file_name_lower ILIKE '%powershell.exe' OR file_name_lower ILIKE '%psexec%'
GROUP BY 1
HAVING image_count > 1;
```

## Correlating Execution with File Activity
See what Registry or Event Log entries occurred within 10 seconds of a specific file being created.
```sql
SELECT 
    art.timestamp, 
    art.message, 
    fs.message as file_name,
    fs.details->>'Type' as macb
FROM artifacts_timeline art
JOIN fs_timeline fs 
  ON art.timestamp BETWEEN fs.timestamp - INTERVAL '10 seconds' 
                       AND fs.timestamp + INTERVAL '10 seconds'
WHERE fs.file_name_lower ILIKE '%.ps1'
AND macb Ilike '%c%';
```

## Persistence Hunting
Quickly query the Registry 'Run' keys across all hosts.
```sql
SELECT filename_path, timestamp, message, details->>'key_path' as registry_key
FROM artifacts_timeline
WHERE parser = 'winreg/run'
ORDER BY timestamp DESC;
```

## Inventory of data
Quick inventory of what artifact data is available
```sql 
SELECT parser, count(*) FROM artifacts_timeline GROUP BY parser;
SELECT Plugin, count(*) from memory_timeliner group by Plugin;
SELECT ImageFileName, count(*) from memory_pslist group by ImageFileName;
```

## JSON access
The details column will contain JSON representation of the source data. 

You can use either of two methods to access individual fields: 
- arrow syntax: `SELECT details->>'$.event_identifier' as event_id`
- json_extract: `SELECT json_extract_string(details, '$.event_identifier') as event_id`

List values can be access by their array position using either method: 
- `SELECT timestamp, filename_path, details->>'$.strings[0]' as service_name FROM artifacts_timeline WHERE parser = 'winevtx'`
- `SELECT timestamp, filename_path, json_extract_string(details,'$.strings[0]') as service_name FROM artifacts_timeline WHERE parser = 'winevtx'`

## Decoding Base64 in SQL
Use DuckDB's native functions to extract and decode Base64 strings directly in your query, avoiding the need for external Python scripts.
```sql
SELECT
    timestamp,
    decode(from_base64(regexp_extract(message, 'EncodedCommand "([^"]+)"', 1)),'ignore') as decoded_command
from artifacts_timeline 
WHERE parser = 'winevtx' AND message ILIKE '%EncodedCommand%'
```
If executing via the command line utility `query_parquet.py` you'll need to escape the double quotes: 

```shell 
uv run helpers/query_parquet.py --case <CASEID> "SELECT
    timestamp,
    decode(from_base64(regexp_extract(message, 'EncodedCommand \"([^\"]+)\"', 1)),'ignore') as decoded_command
from artifacts_timeline WHERE parser = 'winevtx' AND message ILIKE '%EncodedCommand%'"
```

## Exporting Long Data with JSONL
When queries return long strings that get truncated in terminal output, use the `--jsonl` flag and redirect to a file in the `scratch` directory.

```shell
uv run helpers/query_parquet.py --case <CASEID>  "SELECT timestamp, message FROM artifacts_timeline WHERE parser = 'winevtx' AND message ILIKE '%powershell%';" --jsonl > /path/to/case/scratch/powershell_events.jsonl
```

Then, you can use `read` or `fs_search` tools to examine the complete JSON objects.
