# Mission: Find Communication Databases
**Target Agent:** data-analyst

## Purpose
Search Vanko's workstation filesystem timeline to locate all local communication databases (such as Skype `main.db`, Outlook `.ost`/`.pst`, Windows Mail `store.vol`, WhatsApp, or other messaging/email databases) and document their exact paths.

## Background
Our timeline analysis shows Vanko staged files on June 18, 2016, concurrently with Skype activation and ZIP utility activity. To identify the recipient of this exfiltration and find further communications, we need to locate and document the exact paths of all Skype, Outlook, Windows Mail, and other messaging/email databases on Vanko's Surface 3 workstation.

## Budget & Rules of Engagement
- **Orientation Budget:** 3 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 3 tool calls
- **Proactive Self-Termination:** At tool call 13 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If no communication databases are found in the first 3 queries, report and pivot.

## Task Checklist
- [x] Query `fs_timeline` for files with paths containing "Skype" and extensions like `.db`.
- [x] Query `fs_timeline` for files with extensions `.ost` or `.pst` (Outlook).
- [x] Query `fs_timeline` for files named `store.vol` (Windows Mail).
- [x] Query `fs_timeline` for files related to WhatsApp, Viber, or other messaging applications.
- [x] Document the exact paths and metadata (sizes, modification times) of all discovered databases.
- [x] Update `cases/VANKO/docs/shared_facts.md` with a new section `# Communication Databases` listing these paths.
- [x] Update this mission card with results under the "Results & Post-Mortem" section.
- [x] Write a chronological technical log of 100% of executed queries and commands to `cases/VANKO/docs/missions/004-mission-data-analyst-find-comms-databases-audit.md` (verifying that the count matches the final Budget Tally).

## Results & Post-Mortem
- **Approach:**
  Executed structured SQL queries against the `fs_timeline` Parquet table using DuckDB. First identified broad communication file patterns (Skype, Outlook, Windows Mail, WhatsApp, Viber), then refined queries to capture exact file paths, sizes, and timestamp ranges. Performed targeted searches for Viber, Telegram, Signal, WeChat, and LINE, which successfully identified active Telegram Desktop directories.
- **Findings:**
  Discovered the following communication databases on Vanko's workstation:
  1. **Skype:** `/Users/PC User/AppData/Roaming/Skype/live#3aanthony.vanko/main.db` (1,064,960 bytes, active 2015-08-07 to 2016-08-04)
  2. **Outlook OST (Gmail):** `/Users/PC User/AppData/Local/Microsoft/Outlook/anthony.vanko@gmail.com (1).ost` (133,570,560 bytes, active 2015-08-07 to 2016-11-04)
  3. **Outlook OST (iCloud):** `/Users/PC User/AppData/Local/Microsoft/Outlook/anthony.vanko@icloud.com.ost` (16,818,176 bytes, active 2016-02-17 to 2016-11-04)
  4. **Outlook PST:** `/Users/PC User/Documents/Outlook Files/Outlook.pst` (271,360 bytes, active 2015-08-07 to 2016-06-18)
  5. **Windows Mail ESE (PC User):** `/Users/PC User/AppData/Local/Comms/UnistoreDB/store.vol` (15,728,640 bytes, active 2015-08-07 to 2016-11-04)
  6. **Windows Mail ESE (defaultprinter):** `/Users/defaultprinter/AppData/Local/Comms/UnistoreDB/store.vol` (6,291,456 bytes, active 2016-06-18 to 2016-06-27)
  7. **WhatsApp Desktop:** `/Users/PC User/AppData/Roaming/WhatsApp/databases/Databases.db` (7,168 bytes, active 2016-06-16 to 2016-06-18)
  8. **Telegram Desktop:** `/Users/PC User/AppData/Roaming/Telegram Desktop/tdata` (contains local encrypted data files, active 2016-06 to 2016-07)
- **Confidence Rating:** 5/5 (100% verified paths and sizes via filesystem timeline).
- **Budget Tally:** 15 tool calls (1 `read`, 2 `skill`, 2 `patch`, 1 `write`, 9 `shell`).
- **NPS / Feedback:** 10/10. Extremely fast and easy to pinpoint relevant artifacts using DuckDB.
