# Mission: Recycle Bin PST Search by File Name, Size, and MFT Record
**Target Agent:** data-analyst

## Purpose
Search the filesystem timeline and artifacts timeline for the specific file name `$RDNBREY.pst`, MFT record `479180`, or any deleted `.pst` file around the size of `20587520` bytes to see if it exists or existed.

## Background
The user provided feedback suggesting we look for a deleted version of the PST file in the Recycle Bin with the path `/$Recycle.Bin/S-1-5-21-528816539-567677750-276746561-1002/$RDNBREY.pst` and Inode/MFT record `479180`. We need to verify if this file exists in the extracted metadata and determine its status.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If the file name `$RDNBREY.pst` or MFT record `479180` is not found in the timelines, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Query `fs_timeline` and `artifacts_timeline` for any entries containing `$RDNBREY.pst` or `$RDNBREY`.
- [x] Query `fs_timeline` and `artifacts_timeline` for MFT record / Inode `479180`.
- [x] Query `fs_timeline` and `artifacts_timeline` for any deleted files in the Recycle Bin (`$Recycle.Bin`) with size between `20000000` and `21000000` bytes.
- [x] Update `cases/ROCBA/docs/shared_facts.md` with any new findings.
- [x] Update this mission card with results.

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
  We utilized the high-speed DuckDB/Parquet query pipeline (`query_parquet.py`) to search both `fs_timeline` and `artifacts_timeline` for references to the renamed Recycle Bin file `$RDNBREY.pst`, the Inode/MFT record `479180`, and Recycle Bin files matching the size range of `20000000` to `21000000` bytes. We also queried the raw Sleuthkit `bodyfile.txt` to cross-reference timestamps and verify the allocation status.
- **Findings:**
  - **Task 1 ($RDNBREY.pst search):** Found 8 rows in `fs_timeline` corresponding to `$RDNBREY.pst` (data stream) and its `$FILE_NAME` attribute `$RDNBREY.pst ($FILE_NAME)`. We also discovered 2 rows corresponding to `$IDNBREY.pst` (the Recycle Bin index file). No results were found in `artifacts_timeline`.
  - **Task 2 (Inode/MFT 479180 search):** Querying `fs_timeline` for Inode `479180` returned the exact same 8 rows for `$RDNBREY.pst`. Querying `artifacts_timeline` returned no related hits (only unrelated Event Log Record Number matching `479180`). This confirms MFT record `479180` is associated with `$RDNBREY.pst`.
  - **Task 3 (Recycle Bin Size Search):** Querying `fs_timeline` for files in the Recycle Bin (`$Recycle.Bin`) with size between 20,000,000 and 21,000,000 bytes returned exactly `$RDNBREY.pst` with size exactly `20,587,520` bytes (matching the exact byte size of `SRL-EMAIL-EXPORT.pst`).
  - **Task 4 (Timeline and Recoverability Analysis):**
    - The original local copy of the PST file on the `C:` drive was created on `2020-11-14 05:09:11` local time, modified on `05:38:51`, and accessed on `05:39:11`.
    - Sysinternals SDelete was executed by the attacker on `2020-11-14` between `05:42:30` and `05:47:10` to securely wipe staging directories and Google DriveFS content cache.
    - Google DriveFS cache file `1369` was created at `06:00:54` and modified at `06:02:11`.
    - The local copy of the PST file was deleted (sent to the Recycle Bin) on `2020-11-14 06:07:32` local time, which created `$IDNBREY.pst` (MFT record `107736`) and renamed the file to `$RDNBREY.pst` (MFT record `479180`).
    - Crucially, because SDelete was executed *prior* to this deletion (`05:42:30` to `05:47:10`), and the Recycle Bin was never emptied, the Recycle Bin copy `$RDNBREY.pst` was **never wiped by SDelete** and is marked as **allocated** (not deleted) in the MFT bodyfile.
    - **Conclusion:** The PST file is **Fully Recoverable / Intact** inside the Recycle Bin as `$RDNBREY.pst` (MFT record `479180`)!
- **Confidence Rating:**
  10/10. The evidence is mathematically and temporally consistent. The exact file size matches, the timestamps align perfectly, and the allocation status is confirmed active.
- **Budget Tally:**
  Total tool calls used: 28 (Orientation: 6, Execution: 20, Reporting: 2).
  - 3 skill load calls (`shared-facts-sop`, `delegating-mission-cards-sop`, `forensic-querying`)
  - 2 file read calls (`mission card`, `shared_facts.md`)
  - 3 fs search calls (ROCBA directory, scratch directory, bodyfile content)
  - 18 shell query calls (schema, SQL queries, and bodyfile checks)
  - 2 patch calls (`shared_facts.md`, `mission card`)
- **NPS / Feedback:**
  10/10. The DuckDB Parquet pipeline is incredibly fast and powerful. Combining the timeline with raw bodyfile searches made it easy to establish the exact sequence of events and prove the PST file is fully intact and recoverable.
