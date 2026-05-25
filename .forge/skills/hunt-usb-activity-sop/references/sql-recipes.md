# USB Investigation SQL Recipes

Use these queries with `uv run helpers/query_parquet.py` to execute the USB hunting workflow.

## 1. Finding Drive Letter Indicators
Search for LNK files pointing to non-C: drives.

```sql
SELECT timestamp, message, details 
FROM 'fs_timeline.parquet' 
WHERE message LIKE '%.lnk%' AND (message LIKE '%(D)%' OR message LIKE '%(E)%' OR message LIKE '%(F)%' OR message LIKE '%(G)%')
ORDER BY timestamp ASC;
```

## 2. Differentiating Drive Types (RDP Redirect vs. Cloud vs. USB)

### Check for RDP Redirected Drives (TSClient)
Search for references to `\\tsclient` in LNK files, shell items, or other artifacts to identify drive redirection over RDP.

```sql
SELECT timestamp, parser, message 
FROM 'artifacts_timeline.parquet' 
WHERE message LIKE '%tsclient%' OR details LIKE '%tsclient%'
ORDER BY timestamp ASC;
```

### Check for Cloud Drives (e.g., Google Drive File Stream)
Look for cloud storage volume labels and their unique volume serial numbers.

```sql
SELECT timestamp, parser, message 
FROM 'artifacts_timeline.parquet' 
WHERE message LIKE '%Google Drive%' OR message LIKE '%File Stream%'
ORDER BY timestamp ASC;
```

## 3. Mapping Drive Letter to Serial Number
Query ShellBags for the identified drive letter.

```sql
SELECT timestamp, message, details 
FROM 'artifacts_timeline.parquet' 
WHERE data_type = 'windows:shell_items' 
  AND (message LIKE '%[My Computer]\E:\%' OR details LIKE '%E:\%')
ORDER BY timestamp ASC;
```

## 4. Searching for Serial Number Details
Once a serial number (e.g., `AAZ62W7KENRSJLHY`) is found, search for all occurrences.

```sql
SELECT timestamp, data_type, message, details 
FROM 'artifacts_timeline.parquet' 
WHERE message LIKE '%SERIAL_NUMBER%' OR details LIKE '%SERIAL_NUMBER%'
ORDER BY timestamp ASC;
```

## 5. Identifying Vendor Info in USBSTOR
```sql
SELECT timestamp, message, details 
FROM 'artifacts_timeline.parquet' 
WHERE message LIKE '%USBSTOR%' OR details LIKE '%USBSTOR%'
ORDER BY timestamp ASC;
```

## 6. Timeline of Access
Find the first and last time the drive was accessed.

```sql
SELECT MIN(timestamp) as first_access, MAX(timestamp) as last_access
FROM 'artifacts_timeline.parquet'
WHERE message LIKE '%E:\%' OR details LIKE '%E:\%'
```
