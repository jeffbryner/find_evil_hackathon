# Audit Trail: June 30 Staging and USB Activity Investigation

This document tracks all queries and commands executed during the investigation of Vanko's workstation activity on and around June 30, 2016.

## Budget Tally
- **Total Tool Calls Allowed:** 21
- **Actual Tool Calls Executed:** 21 (upon final response)

## Query & Command History

### Query 1: Connection Test
- **Tool Call #6**
- **Query:**
  ```sql
  SELECT * FROM fs_timeline LIMIT 1;
  ```
- **Result:** Successfully returned the first row of `fs_timeline`, confirming DuckDB connectivity and schema.

### Query 2: Search for Classified or StarkResearch files
- **Tool Call #7**
- **Query:**
  ```sql
  SELECT timestamp, data_type, message, details 
  FROM fs_timeline 
  WHERE message ILIKE '%Classified%' OR message ILIKE '%StarkResearch%' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Identified `/Users/PC User/OneDrive/Documents/Level_8/Stark-Policy-Manual-Classified-version-NOTFORRELEASE.docx` accessed on June 30, 2016.

### Query 3: Search for archives around June 30, 2016
- **Tool Call #8**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE (message ILIKE '%.zip%' OR message ILIKE '%.rar%' OR message ILIKE '%.7z%' OR message ILIKE '%.cab%' OR message ILIKE '%.tar%' OR message ILIKE '%.tgz%') 
    AND timestamp >= '2016-06-30 00:00:00' AND timestamp <= '2016-07-01 23:59:59' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Returned system-related app tiles and news assets, but no obvious user-created archives in system folders.

### Query 4: Search for user-created archives around June 30, 2016
- **Tool Call #9**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE (message ILIKE '%.zip%' OR message ILIKE '%.rar%' OR message ILIKE '%.7z%' OR message ILIKE '%.cab%' OR message ILIKE '%.tar%' OR message ILIKE '%.tgz%') 
    AND timestamp >= '2016-06-30 00:00:00' AND timestamp <= '2016-07-01 23:59:59' 
    AND message ILIKE '%/Users/%' 
  ORDER BY timestamp ASC;
  ```
- **Result:** No results returned in that specific strict date range.

### Query 5: General PC User activity on June 30, 2016
- **Tool Call #10**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE timestamp >= '2016-06-30 00:00:00' AND timestamp <= '2016-06-30 23:59:59' 
    AND message ILIKE '%/Users/PC User/%' 
    AND NOT (message ILIKE '%AppData/Local/Google/Chrome%' OR message ILIKE '%AppData/Local/Microsoft/Windows%') 
  ORDER BY timestamp ASC;
  ```
- **Result:** Showed standard Windows Apps/Cortana activity starting around 07:20 UTC.

### Query 6: LNK files pointing to external drives
- **Tool Call #11**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE message ILIKE '%.lnk%' 
    AND (message ILIKE '%(D)%' OR message ILIKE '%(E)%' OR message ILIKE '%(F)%' OR message ILIKE '%(G)%') 
  ORDER BY timestamp ASC;
  ```
- **Result:** Found `StarkResrch (D).lnk` on June 29, 2016 at 18:55:31 UTC and `Stark-IR (D).lnk` on July 1, 2016 at 16:27:02 UTC.

### Query 7: Search for all LNK files around June 30, 2016
- **Tool Call #12**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE message ILIKE '%.lnk%' 
    AND timestamp >= '2016-06-29 00:00:00' AND timestamp <= '2016-07-02 23:59:59' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Found numerous LNK files indicating access to biochemical and armament files, as well as `vacation photos.7z.lnk`.

### Query 8: LNK files June 29 evening to July 2
- **Tool Call #13**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE message ILIKE '%.lnk%' 
    AND timestamp >= '2016-06-29 18:00:00' AND timestamp <= '2016-07-02 23:59:59' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Revealed staging of `vacation photos.7z.lnk` on June 29 at 18:45:20 UTC, and `StarkResrch (D).lnk` on June 29 at 18:55:31 UTC.

### Query 9: Search for vacation photos.7z files
- **Tool Call #14**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM fs_timeline 
  WHERE message ILIKE '%vacation%' OR message ILIKE '%photos.7z%' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Confirmed creation of `/Users/PC User/Downloads/vacation photos.7z` (35,008,256 bytes) on June 29 at 18:28:25 UTC. Copied to `/Users/PC User/Dropbox/vacation photos.7z` on June 29 at 18:46:06 UTC, which has alternate data stream `:com.dropbox.attributes` indicating Dropbox sync.

### Query 10: Search for StarkResrch or Stark-IR in artifacts_timeline
- **Tool Call #15**
- **Query:**
  ```sql
  SELECT timestamp, data_type, message, details 
  FROM artifacts_timeline 
  WHERE message ILIKE '%StarkResrch%' OR message ILIKE '%Stark-IR%' OR details ILIKE '%StarkResrch%' OR details ILIKE '%Stark-IR%' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Mapped Volume `StarkResrch` to Serial Number `0x5650959f` (Decimal: `1448121759`) and `Stark-IR` to Serial Number `0xc83a6c7b` (Decimal: `3359272059`). Showed files inside `D:\vacation photos\vacation photos\Level 8 Classified\BioChemical\`.

### Query 11: Search for USBSTOR in artifacts_timeline
- **Tool Call #16**
- **Query:**
  ```sql
  SELECT timestamp, message, details 
  FROM artifacts_timeline 
  WHERE message ILIKE '%USBSTOR%' OR details ILIKE '%USBSTOR%' 
  ORDER BY timestamp ASC;
  ```
- **Result:** Identified device registration records.

### Query 12: Search browser history for Dropbox/OneDrive
- **Tool Call #17**
- **Query:**
  ```sql
  SELECT ts, url, title, browser 
  FROM browser_history 
  WHERE url ILIKE '%dropbox%' OR url ILIKE '%onedrive%' OR title ILIKE '%dropbox%' OR title ILIKE '%onedrive%' 
  ORDER BY ts ASC;
  ```
- **Result:** Showed extensive OneDrive browser activity but no Dropbox browser activity, reinforcing that Dropbox was run as a desktop client (as confirmed by `:com.dropbox.attributes`).
