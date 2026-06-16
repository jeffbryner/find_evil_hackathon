# Mission: Initial Data Inventory
**Target Agent:** data-analyst

## Purpose
Inventory the forensic images and extracted Parquet tables for the ROCBA case to establish a baseline for our investigation.

## Background
We have a Microsoft Surface disk image (`rocba-cdrive.e01`) and a memory dump (`rocba-memory.raw`). Extracted Parquet tables exist in the scratch directory. We need to document exactly what tables are available, their row counts, and their temporal ranges.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If parquet files cannot be queried or found within 3 tool calls, stop and report.

## Task Checklist
- [x] Inspect the parquet tables available in `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/` and `cases/ROCBA/scratch/rocba-memory.raw/parquet/`
- [x] Query each table to find its row count and min/max timestamp (if applicable)
- [x] Update `cases/ROCBA/docs/shared_facts.md` under `# Data Inventory` with the inventory of available tables, row counts, and time ranges
- [x] Update this mission card with results
- [x] Write a chronological technical log of 100% of executed queries and commands to the `001-mission-data-analyst-data-inventory-audit.md` file

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
  1. Performed a directory listing of the scratch space to locate available Parquet folders and tables.
  2. Displayed the schema of all available tables using the `query_parquet.py` tool.
  3. Formulated a unified DuckDB query to extract row counts and absolute temporal ranges for all 6 tables.
  4. Formulated a secondary query to filter out outlier/epoch/future timestamps and isolate the active 2020 investigation window.
  5. Documented the inventory in `shared_facts.md` and compiled the audit log.
- **Findings:**
  - **Memory Image (`rocba-memory.raw`):**
    - `memory_pslist`: 2,186 rows, active range `2020-11-11 08:12:57` to `2020-11-16 02:32:35`
    - `memory_netscan`: 430 rows, active range `2020-11-11 08:13:14` to `2020-11-16 02:36:42`
    - `memory_timeliner`: 36,012 rows (32,368 rows in active range `2020-09-27 14:37:51` to `2020-11-16 02:36:42`; contains outlier timestamps as early as `1600` and as late as `7225`)
  - **Disk Image (`rocba-cdrive.e01`):**
    - `fs_timeline`: 2,345,972 rows (1,987,075 rows in active range `2020-01-02 17:05:48` to `2020-11-15 19:05:45`; contains epoch `1970` outliers)
    - `artifacts_timeline`: 409,130 rows (201,180 rows in active range `2020-06-23 15:32:06` to `2020-11-15 19:05:14.205449`; contains epoch `1969` outliers)
    - `browser_history`: 2,651 rows, active range `2020-06-24 17:58:22.923000` to `2020-11-15 18:32:19.619198`
- **Confidence Rating:** 5/5 (High confidence. Data extracted directly from verified forensic Parquet tables using DuckDB, and temporal outliers were cleanly isolated and identified.)
- **Budget Tally:**
  - Orientation Budget: 3 / 5 tool calls used
  - Execution Budget: 9 / 10 tool calls used
  - Reporting Budget: 2 / 5 tool calls used (excluding final updates per the SOP)
  - Total Active Tool Calls: 14 / 20
- **NPS / Feedback:** 10/10. The `query_parquet.py` utility is extremely fast and robust. Combining multiple queries using UNION ALL worked flawlessly to quickly inventory millions of rows.

## Discovered Leads (For Followup)
- **Lead 1:** [Details]
