# Forensic Querying Cookbook

Use these SQL recipes as templates for common investigative tasks.

## 1. Time-Window Clustering
Find bursts of activity (e.g., more than 20 events per minute) to identify periods of intense attacker activity.
```sql
SELECT 
    date_trunc('minute', timestamp_utc) as minute_bucket, 
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
SELECT timestamp_utc, file_name, "Type" as macb
FROM fs_timeline
WHERE "Type" LIKE '%B%' 
  AND file_name LIKE '/Windows/System32/%'
ORDER BY timestamp_utc DESC;
```

## 3. Lateral Movement Detection (Cross-Host)
Find the same suspicious file name appearing across multiple hosts in the case.
```sql
SELECT 
    file_name, 
    count(DISTINCT filename_path) as host_count,
    string_agg(filename_path, ', ') as host_paths
FROM fs_timeline
WHERE file_name LIKE '%evil.exe' OR file_name LIKE '%psexec%'
GROUP BY file_name
HAVING host_count > 1;
```

## 4. Correlating Execution with File Activity
See what Registry or Event Log entries occurred within 10 seconds of a specific file being created.
```sql
SELECT 
    art.timestamp_utc, 
    art.message, 
    fs.file_name
FROM artifacts_timeline art
JOIN fs_timeline fs 
  ON art.timestamp_utc BETWEEN fs.timestamp_utc - INTERVAL '10 seconds' 
                          AND fs.timestamp_utc + INTERVAL '10 seconds'
WHERE fs.file_name LIKE '%.ps1';
```

## 5. Persistence Hunting
Quickly query the Registry 'Run' keys across all hosts.
```sql
SELECT filename_path, timestamp_utc, message
FROM artifacts_timeline
WHERE parser = 'winreg/run'
ORDER BY timestamp_utc DESC;
```
