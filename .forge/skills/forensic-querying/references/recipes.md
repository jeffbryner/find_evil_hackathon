# Forensic Querying Cookbook

Use these SQL recipes as templates for common investigative tasks.

## 1. Time-Window Clustering
Find bursts of activity (e.g., more than 20 events per minute) to identify periods of intense attacker activity.
```sql
SELECT 
    date_trunc('minute', timestamp) as minute_bucket, 
    count(*) as event_count,
    string_agg(DISTINCT parser, ', ') as artifact_types
FROM artifacts_timeline
GROUP BY 1
HAVING event_count > 20
ORDER BY minute_bucket ASC;
```

## 2. MACB Flag Filtering (Filesystem)
Find files that were "Created" (B) or "Modified" (M) in a specific directory.
```sql
SELECT timestamp, message as file_name, details->>'Type' as macb
FROM fs_timeline
WHERE details->>'Type' LIKE '%B%' 
  AND file_name_lower LIKE '/windows/system32/%'
ORDER BY timestamp DESC;
```

## 3. Lateral Movement Detection (Cross-Host)
Find the same suspicious file name appearing across multiple hosts in the case.
```sql
SELECT 
    file_name_lower, 
    count(DISTINCT filename_path) as host_count,
    string_agg(filename_path, ', ') as host_paths
FROM fs_timeline
WHERE file_name_lower LIKE '%evil.exe' OR file_name_lower LIKE '%psexec%'
GROUP BY 1
HAVING host_count > 1;
```

## 4. Correlating Execution with File Activity
See what Registry or Event Log entries occurred within 10 seconds of a specific file being created.
```sql
SELECT 
    art.timestamp, 
    art.message, 
    fs.message as file_name
FROM artifacts_timeline art
JOIN fs_timeline fs 
  ON art.timestamp BETWEEN fs.timestamp - INTERVAL '10 seconds' 
                       AND fs.timestamp + INTERVAL '10 seconds'
WHERE fs.file_name_lower LIKE '%.ps1';
```

## 5. Persistence Hunting
Quickly query the Registry 'Run' keys across all hosts.
```sql
SELECT filename_path, timestamp, message, details->>'key_path' as registry_key
FROM artifacts_timeline
WHERE parser = 'winreg/run'
ORDER BY timestamp DESC;
```

## 6. Inventory of data
Quick inventory of what artifact data is available
```sql 
SELECT parser, count(*) FROM artifacts_timeline GROUP BY parser;

```

## 7. JSON access
The details column will contain JSON representation of the source data. 

You can use either of two methods to access individual fields: 
- arrow syntax: SELECT details->>'$.event_identifier' as event_id
- json_extract: SELECT json_extract_string(details, '$.event_identifier') as event_id,

List values can be access by their array position using either method: 
- SELECT timestamp, filename_path, details->>'$.strings[0]' as service_name FROM artifacts_timeline WHERE parser = 'winevtx'
- SELECT timestamp, filename_path, json_extract_string(details,'$.strings[0]') as service_name FROM artifacts_timeline WHERE parser = 'winevtx'

## 8. Decoding Base64 in SQL
Use DuckDB's native functions to extract and decode Base64 strings directly in your query, avoiding the need for external Python scripts.
```sql
SELECT 
    timestamp,
    convert_from(from_base64(regexp_extract(message, 'EncodedCommand "([^"]+)"', 1)), 'utf-16le') as decoded_command
FROM artifacts_timeline
WHERE parser = 'winevtx' AND message LIKE '%EncodedCommand%'
LIMIT 10;
```

## 9. Exporting Long Data with JSONL
When queries return long strings that get truncated in terminal output, use the `--jsonl` flag and redirect to a file in the `scratch/` directory.
```bash
uv run helpers/query_parquet.py --case SRL2018 --query "SELECT timestamp, message FROM artifacts_timeline WHERE parser = 'winevtx' AND message LIKE '%powershell%';" --jsonl > scratch/SRL2018/powershell_events.jsonl
```
Then, you can use `read` or `fs_search` tools to examine the complete JSON objects.

