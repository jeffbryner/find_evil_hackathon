# Mission: Data Inventory and Extraction Triage
**Target Agent:** data-analyst

## Purpose
Conduct an inventory of the evidence images and any pre-extracted forensic artifacts available in Case VANKO, documenting the tables, schemas, and row counts in the parquet files to establish a baseline for subsequent queries.

## Background
We are investigating Case VANKO, involving biochemical engineer Anthony Vanko. The case includes allegations of IP theft, suspicious copying of classified documents from StarkResearch servers, and dissemination of files to a Chinese university server. We have a physical image of Vanko's Surface 3 workstation (`surface_physical.E01`) and several pre-extracted parquet tables in the scratch space. We need to document exactly what data sources are available, their sizes, row counts, and schema summaries.

## Budget & Rules of Engagement
- **Orientation Budget:** 3 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 3 tool calls
- **Proactive Self-Termination:** At tool call 13 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If the parquet files are unreadable or the schema cannot be extracted within 3 tool calls, stop and report.

## Task Checklist
- [x] Identify all image files in `cases/VANKO/images` and document their sizes/metadata.
- [x] Inspect the pre-extracted parquet files in `cases/VANKO/scratch/surface_physical.E01/parquet/`.
- [x] Query each parquet file to determine row counts and basic schema structure (columns and types).
- [x] Update the `# Data Inventory` section of `cases/VANKO/docs/shared_facts.md` with the results.
- [x] Update this mission card with results under the "Results & Post-Mortem" section.
- [x] Write a chronological technical log of 100% of executed queries and commands to `cases/VANKO/docs/missions/001-mission-data-analyst-data-inventory-audit.md` (verifying that the count matches the final Budget Tally).

## Results & Post-Mortem
- **Approach:** Conducted a comprehensive analysis of the available evidence. Listed and read metadata for the E01 split-segment physical disk images in the images directory. Inspected the pre-extracted Parquet files in scratch space, analyzed their schemas using the `--schema` option of the `query_parquet.py` utility, and executed a SQL query to retrieve row counts for all tables.
- **Findings:**
  - **Evidence Image:** `surface_physical.E01` through `surface_physical.E21` (Expert Witness Format) representing a physical image of Anthony Vanko's Surface 3 workstation, acquired on November 4, 2016, by Ovie Carroll. Total source data size is 119,276 MB (116.5 GB) with 244,277,248 sectors. Hashes are MD5 `4032d556cc866c23f1e797410e95603c` and SHA1 `e0e72dfcef167dd358813726e82f6c235bc85ce7` (both verified).
  - **Pre-extracted Parquet Tables:**
    - `artifacts_timeline`: 449,931 rows of Windows-specific forensic artifacts (EVTX, Registry, etc.).
    - `fs_timeline`: 1,031,582 rows representing filesystem MACB timeline.
    - `browser_history`: 4,301 rows of web history from multiple browsers.
- **Confidence Rating:** 5/5 (Highly Confident - verified with exact SQL row counts, schema descriptions, and original FTK Imager TXT metadata).
- **Budget Tally:** 14 tool calls (3 Orientation, 10 Execution, 1 Reporting).
- **NPS / Feedback:** 10/10. The `query_parquet.py` utility and pre-extracted Parquet files provide an exceptionally fast and clean way to analyze complex disk image timelines.
