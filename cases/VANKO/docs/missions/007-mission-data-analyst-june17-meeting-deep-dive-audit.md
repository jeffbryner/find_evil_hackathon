# Technical Audit Log - June 17 Meeting Deep Dive
**Target Agent:** data-analyst
**Case:** VANKO
**Mission:** 007-mission-data-analyst-june17-meeting-deep-dive

## Chronological Command & Query History

### Tool Call 1: Read Mission Card
- **Tool:** `read`
- **Path:** `/Users/jeffbryner/development/find_evil_hackathon/cases/VANKO/docs/missions/007-mission-data-analyst-june17-meeting-deep-dive.md`
- **Purpose:** Understand the mission requirements, objectives, budget constraints, and checklist.

### Tool Call 2: Skill Load
- **Tool:** `skill`
- **Name:** `shared-facts-sop`
- **Purpose:** Ingest standard operating procedures for sharing findings and maintaining centralized knowledge.

### Tool Call 3: File Search (Shared Facts)
- **Tool:** `fs_search`
- **Path:** `cases/VANKO`
- **Pattern:** `shared_facts.md`
- **Purpose:** Find the centralized case knowledge base.

### Tool Call 4: Content Search (Data Inventory)
- **Tool:** `fs_search`
- **Path:** `cases/VANKO/docs`
- **Pattern:** `# Data Inventory`
- **Purpose:** Locate the exact path of the shared facts document.

### Tool Call 5: Read Shared Facts
- **Tool:** `read`
- **Path:** `/Users/jeffbryner/development/find_evil_hackathon/cases/VANKO/docs/shared_facts.md`
- **Purpose:** Review existing knowledge, schemas, and findings to avoid duplication.

### Tool Call 6: Read Query Utility
- **Tool:** `read`
- **Path:** `/Users/jeffbryner/development/find_evil_hackathon/helpers/query_parquet.py`
- **Purpose:** Review the arguments and structure of the Parquet query helper.

### Tool Call 7: Schema Discovery
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --schema`
- **Purpose:** Verify schemas of `fs_timeline`, `artifacts_timeline`, and `browser_history` in the VANKO case.

### Tool Call 8: Count Filesystem Events
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT count(*) FROM fs_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00'"`
- **Result:** 17,574 events found.

### Tool Call 9: Group Filesystem Events
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT data_type, parser, count(*) FROM fs_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00' GROUP BY data_type, parser ORDER BY count(*) DESC"`
- **Result:** All 17,574 events are of type `fs:mactime` parsed by `mactime`.

### Tool Call 10: Sample Filesystem Records
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT timestamp, message, file_name_lower FROM fs_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00' LIMIT 5"`
- **Purpose:** Inspect sample mactime paths to design a noise filter.

### Tool Call 11: Filtered Filesystem Event Count
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT count(*) FROM fs_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00' AND message LIKE '/Users/PC User/%' AND message NOT LIKE '%/AppData/Local/Temp/%' AND message NOT LIKE '%/AppData/Local/Microsoft/Windows/%' AND message NOT LIKE '%/AppData/Local/Packages/%' AND message NOT LIKE '%/AppData/Roaming/Microsoft/Windows/Recent/%'"`
- **Result:** 3,325 filtered user events.

### Tool Call 12: Hourly Time Distribution of User Activity
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT date_trunc('hour', timestamp) AS hr, count(*) FROM fs_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00' AND message LIKE '/Users/PC User/%' AND message NOT LIKE '%/AppData/Local/Temp/%' AND message NOT LIKE '%/AppData/Local/Microsoft/Windows/%' AND message NOT LIKE '%/AppData/Local/Packages/%' AND message NOT LIKE '%/AppData/Roaming/Microsoft/Windows/Recent/%' GROUP BY hr ORDER BY hr"`
- **Result:** Revealed two main spikes of user filesystem activity: 03:00-04:00 (local) and 14:00-15:00 (local).

### Tool Call 13: Filesystem Activity during 14:00-16:00
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT timestamp, message FROM fs_timeline WHERE timestamp >= '2016-06-17 14:00:00' AND timestamp < '2016-06-17 16:00:00' AND message LIKE '/Users/PC User/%' AND message NOT LIKE '%/AppData/Local/Temp/%' AND message NOT LIKE '%/AppData/Local/Microsoft/Windows/%' AND message NOT LIKE '%/AppData/Local/Packages/%' AND message NOT LIKE '%/AppData/Roaming/Microsoft/Windows/Recent/%'"`
- **Result:** Skype chatsync dat files and media cache updates around 14:10-14:17 and 15:10.

### Tool Call 14: Count Artifacts Timeline Events
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT count(*) FROM artifacts_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00'"`
- **Result:** 8,031 events found.

### Tool Call 15: Group Artifacts Timeline Events
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT data_type, parser, count(*) FROM artifacts_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00' GROUP BY data_type, parser ORDER BY count(*) DESC"`
- **Result:** Breakdown of registry, EVTX, prefetch, lnk, and setupapi events.

### Tool Call 16: SetupAPI Log Query
- **Tool:** `shell`
- **Command:** `uv run helpers/query_parquet.py --case VANKO --query "SELECT timestamp, message FROM artifacts_timeline WHERE timestamp >= '2016-06-17 00:00:00' AND timestamp < '2016-06-18 00:00:00' AND data_type = 'setupapi:log:line'"`
- **Result:** Showed device installation of network UPnP storage device with a UUID containing `73656761-7465-7375-636b` (decoding to `segatesuck`) at 10:11 AM local (17:11 UTC).

### Tool Call 17: Comprehensive Deep Dive Chained Query
- **Tool:** `shell`
- **Command:** Executed chained Queries A through F using `&&` and output redirection to dump the full structured results into `cases/VANKO/scratch/june17_analysis.txt` to maximize execution efficiency.
- **Queries Executed:**
  - **Query A (Interesting Files):** Files under Documents, OneDrive, Downloads, and extensions/keywords related to Nina Lam, sturgeon research, and formula.
  - **Query B (Prefetch):** Program execution history (e.g., `TASKMGR.EXE`, `SOFTWAREUPDATE.EXE`, `MMC.EXE`, `SYSTEMPROPERTIESPROTECTION.EXE`, `FILEHISTORY.EXE`, `CMD.EXE`).
  - **Query C (USB/SetupAPI):** SetupAPI logs and event logs for USB/external storage connections (e.g., iPhone "Dr. Vanko" connected at 03:43, WD UPnP storage at 10:11).
  - **Query D (Browser History):** Browsing activity (e.g., Google News, Daily Mail, Bing search for WhatsApp Web).
  - **Query E (Network/Logon Events):** Network connections (SSID `snap  2` at 06:53, SSID `Maddy's Tap Room's Wi-Fi Network` at 10:09) and logons for `anthony.vanko@gmail.com`.
  - **Query F (Comms Files):** Skype and WhatsApp file system activity.

### Tool Call 18: Read Combined Analysis Results
- **Tool:** `read`
- **Path:** `/Users/jeffbryner/development/find_evil_hackathon/cases/VANKO/scratch/june17_analysis.txt`
- **Purpose:** Analyze the combined outputs of the chained queries to synthesize the technical findings.

### Tool Call 19: Write Audit Log (This File)
- **Tool:** `write`
- **Path:** `/Users/jeffbryner/development/find_evil_hackathon/cases/VANKO/docs/missions/007-mission-data-analyst-june17-meeting-deep-dive-audit.md`
- **Purpose:** Record the exact sequence of commands and tool calls for forensic reproducibility.

---

## Budget Tally

| Phase | Budgeted | Expended | Remaining |
| --- | --- | --- | --- |
| **Orientation** | 3 | 6 | -3 |
| **Execution** | 15 | 11 | +4 |
| **Reporting** | 3 | 2 | +1 |
| **Total** | **21** | **19** | **+2** |

*Note: In accordance with the Rules of Engagement, active forensics ceased at Tool Call 17 (the chained query execution). The remaining calls (18-19) were dedicated strictly to reporting, reading intermediate files, and writing logs on disk.*
