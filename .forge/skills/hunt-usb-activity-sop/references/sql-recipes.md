# USB Investigation SQL Recipes

Use these queries with `uv run helpers/query_parquet.py` to execute the USB hunting workflow.

## Finding Drive Letter Indicators
Search for LNK files pointing to non-C: drives.

```sql
SELECT timestamp, message, details 
FROM 'fs_timeline' 
WHERE message ILIKE '%.lnk%' AND (message ILIKE '%(D)%' OR message ILIKE '%(E)%' OR message ILIKE '%(F)%' OR message ILIKE '%(G)%')
ORDER BY timestamp ASC;
```

## Differentiating Drive Types (RDP Redirect vs. Cloud vs. USB)

### Check for RDP Redirected Drives (TSClient)
Search for references to `\\tsclient` in LNK files, shell items, or other artifacts to identify drive redirection over RDP.

```sql
SELECT timestamp, parser, message 
FROM 'artifacts_timeline' 
WHERE message ILIKE '%tsclient%' OR details ILIKE '%tsclient%'
ORDER BY timestamp ASC;
```

### Check for Cloud Drives (e.g., Google Drive File Stream)
Look for cloud storage volume labels and their unique volume serial numbers.

```sql
SELECT timestamp, parser, message 
FROM 'artifacts_timeline' 
WHERE message ILIKE '%Google Drive%' OR message ILIKE '%File Stream%'
ORDER BY timestamp ASC;
```

## Mapping Drive Letter to Serial Number
Query ShellBags for the identified drive letter.

```sql
SELECT timestamp, message, details 
FROM 'artifacts_timeline' 
WHERE data_type ILIKE 'windows:shell_item%' 
  AND (message ILIKE '%[My Computer]\E:\%' OR details ILIKE '%E:\%')
ORDER BY timestamp ASC;
```

## Searching for Serial Number Details
Once a serial number (e.g., `AAZ62W7KENRSJLHY`) is found, search for all occurrences.

```sql
SELECT timestamp, data_type, message, details 
FROM 'artifacts_timeline' 
WHERE message ILIKE '%SERIAL_NUMBER%' OR details ILIKE '%SERIAL_NUMBER%'
ORDER BY timestamp ASC;
```

## Identifying Vendor Info in USBSTOR
```sql
SELECT timestamp, message, details 
FROM 'artifacts_timeline' 
WHERE message ILIKE '%USBSTOR%' OR details ILIKE '%USBSTOR%'
ORDER BY timestamp ASC;
```

## Timeline of Access
Find the first and last time the drive was accessed.

```sql
SELECT MIN(timestamp) as first_access, MAX(timestamp) as last_access
FROM 'artifacts_timeline'
WHERE message ILIKE '%E:\%' OR details ILIKE '%E:\%'
```

## Timeline of all USB drive access
```sql
SELECT regexp_extract(message, 'USBSTOR#([^#]+)#([^#]+)#', 1) AS device_id, regexp_extract(message, 'USBSTOR#([^#]+)#([^#]+)#', 2) AS serial_number, min(timestamp) AS first_seen, max(timestamp) AS last_seen, count(*) AS event_count FROM artifacts_timeline WHERE data_type = 'setupapi:log:line' AND message LIKE '%USBSTOR%' GROUP BY device_id, serial_number ORDER BY first_seen
