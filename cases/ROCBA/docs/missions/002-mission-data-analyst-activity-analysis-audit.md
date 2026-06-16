# Audit Log: Activity Analysis Forensic Queries

This log documents 100% of the SQL queries and commands executed during the Activity Analysis mission for Fred Rocba's system (Case: ROCBA).

## Case Information
- **Case ID:** ROCBA
- **Target Host:** SRL-FORGE
- **Investigator:** Data Analyst Specialist Agent

---

## Chronological Log of Queries

### 1. Initial Database Schema & Tables Exploration
To understand the available tables and columns, the schema was explored first.

```sql
-- Query 1: Show all tables in the database
SHOW TABLES;

-- Query 2: Get schema of all tables
-- Executed via --schema helper option
```

### 2. Browser History Analysis
To identify Fred's project access and search terms, the browser history database was queried.

```sql
-- Query 3: Group browser history by domain to see top visited sites
SELECT domain, count(*) as cnt 
FROM browser_history 
GROUP BY domain 
ORDER BY cnt DESC 
LIMIT 100;

-- Query 4: Group browser history by hostname/host to find internal/external hosts
SELECT hostname, host, count(*) as cnt 
FROM browser_history 
GROUP BY hostname, host 
ORDER BY cnt DESC 
LIMIT 50;

-- Query 5: Query browser history where host is null or 'nan' (local files accessed via browser)
SELECT url, title, ts 
FROM browser_history 
WHERE host IS NULL OR host = 'nan' 
LIMIT 20;

-- Query 6: Query browser history for project or repository keywords
SELECT url, title, ts 
FROM browser_history 
WHERE url LIKE '%git%' 
   OR url LIKE '%sharepoint%' 
   OR url LIKE '%onedrive%' 
   OR url LIKE '%dev.azure%' 
   OR url LIKE '%github%' 
   OR url LIKE '%srl%' 
   OR url LIKE '%project%' 
   OR url LIKE '%mega%' 
   OR url LIKE '%dropbox%' 
   OR url LIKE '%ftp%' 
   OR url LIKE '%upload%'
LIMIT 50;

-- Query 7: Query browser history for specific corporate project names
SELECT url, title, ts 
FROM browser_history 
WHERE url LIKE '%starkresearchlabs%' 
   OR title LIKE '%Vibranium%' 
   OR title LIKE '%Megaforce%'
LIMIT 50;

-- Query 8: Query browser history for generic research keywords
SELECT url, title, ts 
FROM browser_history 
WHERE url LIKE '%research%' 
   OR title LIKE '%research%'
LIMIT 50;

-- Query 9: Query browser history for all project keywords across all periods
SELECT url, title, visit_count, ts 
FROM browser_history 
WHERE url LIKE '%stark%' 
   OR url LIKE '%git%' 
   OR url LIKE '%azure%' 
   OR url LIKE '%github%' 
   OR url LIKE '%project%' 
   OR title LIKE '%Vibranium%' 
   OR title LIKE '%Megaforce%'
LIMIT 100;

-- Query 10: Query browser history chronologically from Nov 1, 2020 onwards
SELECT url, title, ts 
FROM browser_history 
WHERE ts >= '2020-11-01' 
ORDER BY ts ASC 
LIMIT 100;

-- Query 11: Query browser history during Fred's vacation window (Nov 10 to Nov 16)
SELECT url, title, ts 
FROM browser_history 
WHERE ts >= '2020-11-10' AND ts <= '2020-11-16' 
ORDER BY ts ASC 
LIMIT 100;

-- Query 12: Query browser history after the main file access event (19:57 Nov 13)
SELECT url, title, ts 
FROM browser_history 
WHERE ts >= '2020-11-13 19:57:00' AND ts <= '2020-11-16' 
ORDER BY ts ASC 
LIMIT 100;

-- Query 13: Query browser history on Nov 13 and Nov 14 (reconstructing detailed timeline)
SELECT ts, url, title 
FROM browser_history 
WHERE ts >= '2020-11-13' AND ts <= '2020-11-15' 
ORDER BY ts ASC 
LIMIT 150;
```

### 3. File System Timeline (fs_timeline) Analysis
To trace file creations, deletions, and modifications in Fred's profile and staging areas.

```sql
-- Query 14: Search for files containing specific project names (Vibranium, Megaforce)
SELECT timestamp, data_type, parser, message, file_name_lower 
FROM fs_timeline 
WHERE file_name_lower LIKE '%vibrainium%' 
   OR file_name_lower LIKE '%vibranium%' 
   OR file_name_lower LIKE '%megaforce%'
LIMIT 100;

-- Query 15: Query fs_timeline for events around the home burglary window (19:00 to 21:00 Nov 13)
SELECT timestamp, data_type, parser, message, file_name_lower 
FROM fs_timeline 
WHERE timestamp >= '2020-11-13 19:00:00' 
  AND timestamp <= '2020-11-13 21:00:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 16: Query fs_timeline for events during the specific remote RDP session (19:43 to 20:10 Nov 13)
SELECT timestamp, data_type, parser, message, file_name_lower 
FROM fs_timeline 
WHERE timestamp >= '2020-11-13 19:43:00' 
  AND timestamp <= '2020-11-13 20:10:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 17: Search fs_timeline for archive/staging/leak keywords
SELECT timestamp, data_type, parser, message, file_name_lower 
FROM fs_timeline 
WHERE file_name_lower LIKE '%.zip' 
   OR file_name_lower LIKE '%.rar' 
   OR file_name_lower LIKE '%.7z' 
   OR file_name_lower LIKE '%staged%' 
   OR file_name_lower LIKE '%exfil%' 
   OR file_name_lower LIKE '%leak%'
LIMIT 100;

-- Query 18: Query fs_timeline on Nov 13 for events in Fred's user profile
SELECT timestamp, data_type, parser, message 
FROM fs_timeline 
WHERE timestamp >= '2020-11-13 19:43:00' 
  AND timestamp <= '2020-11-13 20:00:00' 
  AND message LIKE '%/Users/fredr/%' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 19: Query fs_timeline on Nov 13 filtering for cloud and external drive activity
SELECT timestamp, data_type, message 
FROM fs_timeline 
WHERE timestamp >= '2020-11-13 19:00:00' 
  AND timestamp <= '2020-11-13 21:00:00' 
  AND (message LIKE '%Google Drive%' 
    OR message LIKE '%My Drive%' 
    OR message LIKE '%F:%' 
    OR message LIKE '%Stark Research Labs%') 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 20: Query fs_timeline on Nov 13 filtering out Minecraft (noise reduction)
SELECT timestamp, data_type, message 
FROM fs_timeline 
WHERE timestamp >= '2020-11-13 19:40:00' 
  AND timestamp <= '2020-11-13 20:45:00' 
  AND message NOT LIKE '%New World%' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 21: Query fs_timeline for BitLocker Recovery Key files
SELECT timestamp, data_type, message 
FROM fs_timeline 
WHERE message LIKE '%BitLocker Recovery Key%' 
   OR message LIKE '%1694D560%' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 22: Query fs_timeline for actual BitLocker Recovery Key .txt files
SELECT timestamp, data_type, message 
FROM fs_timeline 
WHERE message LIKE '%BitLocker Recovery Key%txt%' 
   OR message LIKE '%BitLocker Recovery Key%TXT%' 
   OR message LIKE '%1694D560%txt%' 
   OR message LIKE '%1694D560%TXT%' 
ORDER BY timestamp ASC 
LIMIT 100;
```

### 4. Process Execution & Artifacts Timeline Analysis
To trace what programs were executed (via Prefetch, BAM, AppCompatCache) and what files were opened (via LNK files, Jump Lists, BagMRU).

```sql
-- Query 23: Query artifacts_timeline around the RDP logon event (19:20 to 20:10 Nov 13)
SELECT timestamp, parser, message, details 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-13 19:20:00' 
  AND timestamp <= '2020-11-13 20:10:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 24: Query artifacts_timeline for RDP logon event logs
SELECT timestamp, message 
FROM artifacts_timeline 
WHERE parser = 'winevtx' 
  AND message LIKE '%TerminalServices%' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 25: Query artifacts_timeline for RDP logons during vacation (Nov 10 onwards)
SELECT timestamp, message 
FROM artifacts_timeline 
WHERE parser = 'winevtx' 
  AND message LIKE '%TerminalServices%' 
  AND timestamp >= '2020-11-10 00:00:00-08:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 26: Query artifacts_timeline for specific RDP logon types (Logon Type 10)
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE parser = 'winevtx' 
  AND (message LIKE '%1149%' 
    OR message LIKE '%4624%' 
    OR message LIKE '%Logon Type: 10%' 
    OR message LIKE '%TerminalServices%') 
  AND timestamp >= '2020-11-13 19:30:00' 
  AND timestamp <= '2020-11-13 19:50:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 27: Query artifacts_timeline for RDP Local Session Manager events
SELECT timestamp, message 
FROM artifacts_timeline 
WHERE parser = 'winevtx' 
  AND message LIKE '%TerminalServices-LocalSessionManager%' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 28: Query artifacts_timeline for RDP Local Session Manager events after Nov 13 19:00
SELECT timestamp, message 
FROM artifacts_timeline 
WHERE parser = 'winevtx' 
  AND message LIKE '%TerminalServices-LocalSessionManager%' 
  AND timestamp >= '2020-11-13 19:00:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 29: Query process execution on Nov 13 during intrusion session (Prefetch/AppCompatCache)
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE (parser = 'prefetch' 
    OR parser = 'appcompatcache' 
    OR message LIKE '%Prefetch%' 
    OR message LIKE '%executed%') 
  AND timestamp >= '2020-11-13 19:40:00' 
  AND timestamp <= '2020-11-13 21:20:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 30: Get distinct parsers in artifacts_timeline to find specific forensic artifacts
SELECT DISTINCT parser FROM artifacts_timeline;

-- Query 31: Query artifacts_timeline for LNK, Jump Lists, BagMRU, UserAssist, and BAM on Nov 13
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-13 19:40:00' 
  AND timestamp <= '2020-11-13 21:20:00' 
  AND (parser LIKE '%lnk%' 
    OR parser LIKE '%destinations%' 
    OR parser LIKE '%bagmru%' 
    OR parser LIKE '%mrulist%' 
    OR parser LIKE '%userassist%' 
    OR parser LIKE '%bam%') 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 32: Query artifacts_timeline for specific files and projects on Nov 13
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-13 19:40:00' 
  AND timestamp <= '2020-11-13 21:20:00' 
  AND (message LIKE '%F:%' 
    OR message LIKE '%CRIMSON2%' 
    OR message LIKE '%Files from SRL%' 
    OR message LIKE '%Files of interest%' 
    OR message LIKE '%Vibranium%' 
    OR message LIKE '%Megaforce%' 
    OR message LIKE '%KITT%' 
    OR message LIKE '%Maria Hill%' 
    OR message LIKE '%secretweapon%' 
    OR message LIKE '%Hydrogen%' 
    OR message LIKE '%TIVO%') 
ORDER BY timestamp ASC 
LIMIT 150;

-- Query 33: Query artifacts_timeline for files copied/accessed from 19:51 to 21:20 Nov 13
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-13 19:51:15' 
  AND timestamp <= '2020-11-13 21:20:00' 
  AND (message LIKE '%F:%' 
    OR message LIKE '%CRIMSON2%' 
    OR message LIKE '%Files from SRL%' 
    OR message LIKE '%Files of interest%' 
    OR message LIKE '%Vibranium%' 
    OR message LIKE '%Megaforce%' 
    OR message LIKE '%KITT%' 
    OR message LIKE '%Maria Hill%' 
    OR message LIKE '%secretweapon%' 
    OR message LIKE '%Hydrogen%' 
    OR message LIKE '%TIVO%') 
ORDER BY timestamp ASC 
LIMIT 150;

-- Query 34: Query all TerminalServices-LocalSessionManager events from Nov 10 to Nov 15 (Vacation window)
SELECT timestamp, message 
FROM artifacts_timeline 
WHERE parser = 'winevtx' 
  AND message LIKE '%TerminalServices-LocalSessionManager%' 
  AND timestamp >= '2020-11-10 00:00:00-08:00' 
  AND timestamp <= '2020-11-16 00:00:00-08:00' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 35: Query process execution and file access on Nov 14 during RDP sessions (04:30 to 06:30)
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-14 04:30:00-08:00' 
  AND timestamp <= '2020-11-14 06:30:00-08:00' 
  AND (parser = 'prefetch' 
    OR parser = 'appcompatcache' 
    OR parser LIKE '%lnk%' 
    OR parser LIKE '%destinations%' 
    OR message LIKE '%Prefetch%' 
    OR message LIKE '%executed%' 
    OR message LIKE '%F:%' 
    OR message LIKE '%CRIMSON2%') 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 36: Query process execution and file access during the second RDP session on Nov 14 (04:52 to 06:30)
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-14 04:52:00-08:00' 
  AND timestamp <= '2020-11-14 06:30:00-08:00' 
  AND (parser = 'prefetch' 
    OR parser = 'appcompatcache' 
    OR parser LIKE '%lnk%' 
    OR parser LIKE '%destinations%' 
    OR message LIKE '%Prefetch%' 
    OR message LIKE '%executed%' 
    OR message LIKE '%F:%' 
    OR message LIKE '%CRIMSON2%') 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 37: Query artifacts_timeline specifically for Sysinternals SDelete execution on Nov 14
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE timestamp >= '2020-11-14 05:30:00-08:00' 
  AND timestamp <= '2020-11-14 06:30:00-08:00' 
  AND (message LIKE '%sdelete%' OR message LIKE '%SDelete%') 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 38: Query connected USB devices in artifacts_timeline
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE parser LIKE '%usbstor%' 
   OR parser LIKE '%usb_devices%' 
   OR message LIKE '%USB%' 
   OR message LIKE '%usbstor%' 
ORDER BY timestamp ASC 
LIMIT 100;

-- Query 39: Query USB devices sorted by timestamp to find connection times
SELECT timestamp, parser, message 
FROM artifacts_timeline 
WHERE parser = 'winreg/windows_usbstor_devices' 
   OR parser = 'winreg/windows_usb_devices' 
ORDER BY timestamp DESC 
LIMIT 100;
```

### 5. Memory Forensics (memory_netscan) Analysis
To check for network connections from RDP or exfiltration tools.

```sql
-- Query 40: Query netscan for RDP port 3389 and the malicious Azure IP
SELECT * 
FROM memory_netscan 
WHERE ForeignAddr LIKE '%52.249.%' 
   OR LocalAddr LIKE '%52.249.%' 
   OR ForeignPort = 3389 
   OR LocalPort = 3389 
LIMIT 100;

-- Query 41: Query netscan for non-RDP connections
SELECT * 
FROM memory_netscan 
WHERE LocalPort != 3389 
  AND ForeignPort != 3389 
LIMIT 100;
```

---

## Conclusion

All queries executed successfully. Multi-artifact timeline reconstruction was fully completed using the database queries listed above, ensuring forensic integrity and data accuracy.