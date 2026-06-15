# Forensic Audit Trail: Initial Data Inventory and Triage (Mission 001)

## Initial Prompt & Parameters
- **Target Agent:** data-analyst
- **Mission Card:** cases/NISTDL/docs/missions/001-mission-data-analyst-inventory-and-triage.md
- **Budgets:**
  - Orientation Budget: 5 tool calls
  - Execution Budget: 25 tool calls
  - Reporting Budget: 5 tool calls
- **Fail-Fast:** If no parquet files or timeline data can be found after 5 queries, stop and report.

## Chronological Log of Tool Calls

1. **Skill (shared-facts-sop)**: Loaded SOP for shared facts. (Useful)
2. **Skill (delegating-mission-cards-sop)**: Loaded SOP for mission cards. (Useful)
3. **Read (cases/NISTDL/docs/missions/001-mission-data-analyst-inventory-and-triage.md)**: Retrieved mission card details. (Useful)
4. **Read (cases/NISTDL/docs/shared_facts.md)**: Retrieved current shared facts. (Useful)
5. **Skill (forensic-querying)**: Loaded forensic querying recipes. (Useful)
6. **Shell (query_parquet.py --schema)**: Discovered tables: `fs_timeline`, `artifacts_timeline`, `browser_history`. (Useful)
7. **Shell (query_parquet.py "SELECT DISTINCT imagename...")**: Found images: `cfreds_2015_data_leakage_pc.dd`, `cfreds_2015_data_leakage_rm2.dd`, `cfreds_2015_data_leakage_rm2.E01`. (Useful)
8. **Shell (python os.listdir)**: Listed directories in `scratch`: `cfreds_2015_data_leakage_rm3_type1.iso`, `cfreds_2015_data_leakage_rm2.E01`, `cfreds_2015_data_leakage_pc.dd`, `cfreds_2015_data_leakage_rm2.dd`, `cfreds_2015_data_leakage_rm3_type2.dd`, `cfreds_2015_data_leakage_rm3_type3.E01`. (Useful)
9. **Shell (python glob parquet)**: Listed parquet files in `scratch`. (Useful)
10. **Shell (python glob recursive parquet)**: Verified all parquet files. (Useful)
11. **Shell (query_parquet.py SELECT data_type, COUNT(*))**: Found data types in `artifacts_timeline` on the primary host. (Useful)
12. **Shell (query_parquet.py SELECT ... windows:registry:installation)**: Identified OS: Windows 7 Ultimate SP1, Registered Owner: informant, Installation Time: 2015-03-22 07:34:26-07:00. (Useful)
13. **Shell (query_parquet.py SELECT ... ComputerName)**: Searched for computer name. (Too broad)
14. **Shell (query_parquet.py SELECT ... Control\ComputerName\ComputerName)**: Searched for computer name with specific path. (No results due to escaping)
15. **Shell (query_parquet.py SELECT ... ComputerName NOT Software\Classes)**: Searched for computer name excluding Classes. (Too broad due to escaping)
16. **Shell (query_parquet.py SELECT ... key_path ILIKE '%ComputerName')**: Error: key_path column doesn't exist in `artifacts_timeline`. (Useful error)
17. **Shell (query_parquet.py SELECT ... ComputerName NOT Classes)**: Found Hostname: `INFORMANT-PC`. (Useful)
18. **Shell (query_parquet.py SELECT ... windows:registry:sam_users)**: Identified users: Administrator (RID 500), Guest (RID 501), informant (RID 1000), admin11 (RID 1001), ITechTeam (RID 1002), temporary (RID 1003). (Useful)
19. **Skill (hunt-execution-sop)**: Loaded process execution hunting SOP. (Useful)
20. **Skill (hunt-exfiltration-sop)**: Loaded exfiltration hunting SOP. (Useful)
21. **Shell (query_parquet.py SELECT ... prefetch execution)**: Found execution of `ERASER.EXE`, `CCLEANER64.EXE`, `GOOGLEDRIVESYNC.EXE`, and others on 2015-03-25. (Useful)
22. **Shell (query_parquet.py SELECT ... browser_history)**: Found search and download of Eraser and CCleaner, Google storage access with `iaman.informant.personal@gmail.com`, and viewing of resignation letter on 2015-03-25. (Useful)
23. **Shell (query_parquet.py SELECT ... Resignation_Letter)**: Found `Resignation_Letter_(Iaman_Informant).docx` created on 2015-03-24, and `.xps` viewed on 2015-03-25. (Useful)
24. **Shell (query_parquet.py SELECT ... informant Desktop)**: Found downloads of Eraser and CCleaner setup files, both deleted. (Useful)
25. **Shell (query_parquet.py SELECT ... 08:10:00 to 08:20:00)**: Found file deletions in Recycle Bin and Desktop `[QAT` during Eraser execution. (Useful)
26. **Shell (query_parquet.py SELECT ... Recycle.Bin $I)**: Searched for Recycle Bin index files. (No results)
27. **Shell (query_parquet.py SELECT ... future timestamps)**: Found future timestamps `2076-11-29` for deleted Recycle Bin files and `[QAT`. (Useful)
28. **Shell (query_parquet.py SELECT ... GROUP BY imagename)**: Found file counts per image in `fs_timeline`. (Useful)
29. **Read (helpers/query_parquet.py)**: Reviewed query_parquet.py implementation. (Useful)
30. **Shell (query_parquet.py SELECT ... filename_path counts)**: Verified which parquet files contain data. (Useful)
31-33. **Shell (query_parquet.py ... rm3 counts)**: Confirmed `rm3_type1`, `rm3_type2`, and `rm3_type3` timelines are empty. (Useful)
34. **Shell (query_parquet.py ... rm2.dd)**: Found deleted files on `rm2.dd` (USB drive) under `/$OrphanFiles/`. (Useful)
35. **Shell (query_parquet.py ... USBSTOR)**: Found connection history for two SanDisk Cruzer Fit USB devices on primary host. (Useful)
36. **Shell (ioc_tracker.py ... email)**: Registered email IOC. (Useful)
37. **Shell (ioc_tracker.py --help)**: Verified allowed types. (Useful)
38. **Shell (ioc_tracker.py ... multiple)**: Registered filenames and USB serials. (Useful)

## Internal Reasoning & Key SQL Queries
- Discovered distinct images in the case:
  ```sql
  SELECT DISTINCT imagename FROM fs_timeline UNION SELECT DISTINCT imagename FROM artifacts_timeline UNION SELECT DISTINCT imagename FROM browser_history;
  ```
- Discovered OS installation details using:
  ```sql
  SELECT timestamp, message, details FROM artifacts_timeline WHERE data_type = 'windows:registry:installation' AND imagename = 'cfreds_2015_data_leakage_pc.dd';
  ```
- Discovered hostname using:
  ```sql
  SELECT message FROM artifacts_timeline WHERE data_type = 'windows:registry:key_value' AND message ILIKE '%ComputerName%' AND message NOT ILIKE '%Classes%' AND imagename = 'cfreds_2015_data_leakage_pc.dd';
  ```
- Discovered local users using:
  ```sql
  SELECT timestamp, message, details FROM artifacts_timeline WHERE data_type = 'windows:registry:sam_users' AND imagename = 'cfreds_2015_data_leakage_pc.dd';
  ```
- Discovered connected USB devices using:
  ```sql
  SELECT timestamp, message FROM artifacts_timeline WHERE data_type = 'windows:registry:usbstor:instance' AND imagename = 'cfreds_2015_data_leakage_pc.dd';
  ```
- Queried counts of data types in `artifacts_timeline` on the primary host:
  ```sql
  SELECT data_type, COUNT(*) FROM artifacts_timeline WHERE imagename = 'cfreds_2015_data_leakage_pc.dd' GROUP BY data_type ORDER BY COUNT(*) DESC;
  ```
- Queried recent prefetch execution history:
  ```sql
  SELECT timestamp, message FROM artifacts_timeline WHERE data_type = 'windows:prefetch:execution' AND imagename = 'cfreds_2015_data_leakage_pc.dd' ORDER BY timestamp DESC LIMIT 50;
  ```
- Queried browser history on the primary host:
  ```sql
  SELECT ts, url, title, visit_count FROM browser_history WHERE imagename = 'cfreds_2015_data_leakage_pc.dd' ORDER BY ts DESC LIMIT 50;
  ```
- Queried filesystem timeline for resignation letter artifacts:
  ```sql
  SELECT timestamp, message FROM fs_timeline WHERE message ILIKE '%Resignation_Letter%' ORDER BY timestamp DESC;
  ```
- Queried filesystem timeline for informant's Desktop activity on 2015-03-25:
  ```sql
  SELECT timestamp, message FROM fs_timeline WHERE message ILIKE '%/Users/informant/Desktop%' AND timestamp BETWEEN '2015-03-25 00:00:00' AND '2015-03-25 23:59:59' ORDER BY timestamp ASC;
  ```
- Queried filesystem timeline for activity during anti-forensics execution window (08:10 to 08:20):
  ```sql
  SELECT timestamp, message FROM fs_timeline WHERE timestamp BETWEEN '2015-03-25 08:10:00' AND '2015-03-25 08:20:00' ORDER BY timestamp ASC LIMIT 100;
  ```
- Queried filesystem timeline for Recycle Bin index ($I) files:
  ```sql
  SELECT timestamp, message FROM fs_timeline WHERE message ILIKE '%Recycle.Bin%' AND message ILIKE '%$I%' ORDER BY timestamp DESC LIMIT 20;
  ```
- Queried filesystem timeline for corrupted/future timestamps:
  ```sql
  SELECT timestamp, message FROM fs_timeline WHERE timestamp BETWEEN '2076-01-01' AND '2077-01-01' ORDER BY timestamp ASC;
  ```
- Queried file counts per image in `fs_timeline`:
  ```sql
  SELECT imagename, COUNT(*) FROM fs_timeline GROUP BY imagename;
  ```
- Queried file counts per `filename_path` in `fs_timeline`:
  ```sql
  SELECT filename_path, COUNT(*) FROM fs_timeline GROUP BY filename_path;
  ```
- Queried files present on removable media `rm2`:
  ```sql
  SELECT timestamp, message FROM fs_timeline LIMIT 50;
  ```
