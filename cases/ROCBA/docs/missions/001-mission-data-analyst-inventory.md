# Mission: Inventory Extracted Forensic Data
**Target Agent:** data-analyst

## Purpose
Inventory all available parquet tables, their schemas, and get a high-level overview of the event counts, time ranges, and available evidence in the ROCBA case.

## Background
Fred Rocba's system was compromised/targeted around November 2020. We have extracted disk and memory forensic artifacts in parquet format under the `cases/ROCBA/scratch/` directory. Before doing deep-dive hunting, we need to know what tables are available, their column structures, the time ranges covered by the events, and the number of records in each.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If the `query_parquet.py` utility fails or if no tables are found, stop immediately and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Run `query_parquet.py` with `--schema` to discover all available tables and columns.
- [x] Query the record count and min/max timestamp for each table (e.g. `fs_timeline`, `artifacts_timeline`, `browser_history`, and memory tables).
- [x] Identify the hostnames/images represented in the data.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  1. Conducted schema discovery using `query_parquet.py --case ROCBA --schema` to list all available tables, columns, and types.
  2. Wrote and executed a unified `UNION ALL` SQL query to retrieve row counts, minimum timestamps, maximum timestamps, and associated image names across all six tables in parallel.
  3. Queried distinct hostnames in the `browser_history` table and verified the system hostname (`SRL-FORGE`) by querying the active Windows registry computer name key (`HKLM\System\ControlSet001\Control\ComputerName\ComputerName`) in the `artifacts_timeline` table.
- **Findings:**
  - **Available Parquet Tables & Metrics:**
    | Table Name | Record Count | Min Timestamp | Max Timestamp | Image Name |
    | --- | --- | --- | --- | --- |
    | `memory_pslist` | 2,186 | 2020-11-11 08:12:57 | 2020-11-16 02:32:35 | `rocba-memory.raw` |
    | `memory_netscan` | 430 | 2020-11-11 08:13:14 | 2020-11-16 02:36:42 | `rocba-memory.raw` |
    | `memory_timeliner` | 9,968,767 | 1600-09-30 19:15:02 | 8907-12-12 16:13:52 | `rocba-memory.raw` |
    | `artifacts_timeline` | 6,589,000 | 1969-12-31 16:00:00-08 | 2104-01-09 23:54:37-08 | `rocba-cdrive.e01` |
    | `fs_timeline` | 2,345,972 | 1970-01-01 16:00:00 | 2020-11-15 19:05:45 | `rocba-cdrive.e01` |
    | `browser_history` | 2,651 | 2020-06-24 17:58:22.923-07 | 2020-11-15 18:32:19.619198-08 | `rocba-cdrive.e01` |
  - **Hostnames and Images:**
    - Hostname: `SRL-FORGE` (Confirmed via browser history and registry computer name `HKLM\System\ControlSet001\Control\ComputerName\ComputerName`).
    - Images:
      - Disk: `rocba-cdrive.e01`
      - Memory: `rocba-memory.raw`
- **Confidence Rating:** 5/5. The schema and data structures are fully populated, and the hostname was verified using multiple distinct sources (browser history and SYSTEM registry hive).
- **Budget Tally:**
  - Orientation: 4 tool calls (Budget: 5)
  - Execution: 5 tool calls (Budget: 15)
  - Reporting: 2 tool calls (Budget: 5)
  - Total: 11 tool calls
- **NPS / Feedback:** The DuckDB/Parquet integration via `query_parquet.py` is extremely fast and robust, allowing us to perform schema discovery and multi-million row queries in milliseconds.
