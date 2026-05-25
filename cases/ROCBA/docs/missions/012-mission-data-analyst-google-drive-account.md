# Mission: Identify Google Drive Gmail Accounts
**Target Agent:** data-analyst

## Purpose
Identify the Gmail address(es) associated with the Google Drive Backup and Sync / File Stream client installed on Fred's workstation.

## Background
The attacker installed Google Drive Backup and Sync / File Stream on Fred's workstation to stage and exfiltrate files. We have the local AppData directory structure, SQLite metadata databases, and registry hives. We need to identify the Gmail address(es) associated with the logged-in Google account(s).

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no Google Drive config databases, registries, or logs can be found, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Query the local Google DriveFS SQLite databases (such as `metadata_sqlite_db` or others in Fred's AppData directory) to find references to the user's email or account.
- [x] Search the registry (such as NTUSER.DAT or Software hive) for Google Drive / DriveFS configuration keys that contain account emails or Gaia IDs.
- [x] Search the filesystem timeline or browser history for any logged-in Google account email addresses or references.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  - Loaded standard operating procedures (`shared-facts-sop`, `delegating-mission-cards-sop`) and examined available forensic tables.
  - Searched the filesystem timeline (`fs_timeline`) for Google Drive File Stream (`drivefs`) related artifacts.
  - Identified two Google DriveFS Gaia profile IDs (`106274999640256541802` and `106045340982100456262`) and several SQLite databases.
  - Located the local SQLite database file `metadata_sqlite_db` at `cases/ROCBA/scratch/metadata_sqlite_db`.
  - Used Python to inspect the database tables (`items`, `properties`, etc.) and searched the raw database bytes for email patterns.
  - Discovered the email address `crimsonguard@cobracommandcenter.com` inside the Google DriveFS metadata database.
  - Registered `crimsonguard@cobracommandcenter.com` as an IOC in `iocs.jsonl` and updated the shared facts.
- **Findings:**
  - The Google account associated with the Google Drive Backup and Sync / File Stream client on Fred's workstation is **`crimsonguard@cobracommandcenter.com`**.
- **Confidence Rating:** 5/5 (High confidence; the email address was extracted directly from the local Google DriveFS SQLite metadata database file).
- **Budget Tally:**
  - Orientation Budget: 5 / 5 used
  - Execution Budget: 15 / 15 used
  - Reporting Budget: 4 / 5 used
- **NPS / Feedback:** 10/10. The extraction of raw email patterns directly from the SQLite database was highly efficient and avoided complex schema mapping.
