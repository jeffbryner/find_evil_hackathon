# Mission: Extract Communication Databases
**Target Agent:** sniper-forensics

## Purpose
Extract local communication databases (Skype SQLite, Outlook PST, Windows Mail ESE, WhatsApp) from the mounted workstation image to the read-write scratch space for subsequent parsing and analysis.

## Background
Our data-analyst has located several critical communication databases on Anthony Vanko's Surface 3 workstation. To analyze Vanko's communications (specifically regarding the June 18, 2016 intellectual property leak), we need to extract these raw databases from the mounted filesystem to the read-write scratch space inside the SIFT container.

## Budget & Rules of Engagement
- **Orientation Budget:** 3 tool calls
- **Execution Budget:** 12 tool calls
- **Reporting Budget:** 3 tool calls
- **Proactive Self-Termination:** At tool call 14 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If the mounted image directory `/mnt/cases/VANKO/surface_physical.E01/` is not accessible inside the container, stop and report.

## Task Checklist
- [x] Verify accessibility of `/mnt/cases/VANKO/surface_physical.E01/` inside the SIFT container.
- [x] Create the output directory `/scratch/surface_physical.E01/extracted_comms/` inside the container.
- [x] Copy the Skype SQLite database from `/mnt/cases/VANKO/surface_physical.E01/Users/PC User/AppData/Roaming/Skype/live#3aanthony.vanko/main.db` to `/scratch/surface_physical.E01/extracted_comms/skype_main.db`.
- [x] Copy the Outlook PST database from `/mnt/cases/VANKO/surface_physical.E01/Users/PC User/Documents/Outlook Files/Outlook.pst` to `/scratch/surface_physical.E01/extracted_comms/Outlook.pst`.
- [x] Copy the Windows Mail ESE database from `/mnt/cases/VANKO/surface_physical.E01/Users/PC User/AppData/Local/Comms/UnistoreDB/store.vol` to `/scratch/surface_physical.E01/extracted_comms/windows_mail_store.vol`.
- [x] Copy the WhatsApp Desktop database from `/mnt/cases/VANKO/surface_physical.E01/Users/PC User/AppData/Roaming/WhatsApp/databases/Databases.db` to `/scratch/surface_physical.E01/extracted_comms/whatsapp_databases.db`.
- [x] Verify that all files have been copied successfully, documenting their sizes and file types.
- [x] Update this mission card with results under the "Results & Post-Mortem" section.
- [x] Write a chronological technical log of 100% of executed queries and commands to `cases/VANKO/docs/missions/005-mission-sniper-forensics-extract-comms-databases-audit.md` (verifying that the count matches the final Budget Tally).

## Results & Post-Mortem
- **Approach:**
  1. Verified mounted image path accessibility inside the SIFT container.
  2. Created the shared, persistent read-write output folder `/scratch/surface_physical.E01/extracted_comms/`.
  3. Performed an efficient batched `cp` operation for all four requested databases.
  4. Verified file integrity and exact file sizes, and confirmed file signatures using `file`.
  5. Documented results in the shared facts and updated the audit trail file.
- **Findings:**
  All target databases were successfully extracted to the shared scratch directory `/scratch/surface_physical.E01/extracted_comms/`:
  - **Skype SQLite Database (`skype_main.db`):** 1,064,960 bytes, valid SQLite 3.x database.
  - **Outlook PST Database (`Outlook.pst`):** 271,360 bytes, valid Microsoft Outlook email folder (>=2003).
  - **Windows Mail ESE Database (`windows_mail_store.vol`):** 15,728,640 bytes, valid Extensible Storage Engine database (DirtyShutdown state, page size 4096).
  - **WhatsApp Desktop Database (`whatsapp_databases.db`):** 7,168 bytes, valid SQLite 3.x database.
- **Confidence Rating:** 5/5 (Absolute certainty; verified matching source/destination file sizes and valid file headers).
- **Budget Tally:** 12 tool calls (Orientation: 3, Execution: 7, Reporting: 2).
- **NPS / Feedback:** 10/10. Extremely clean and efficient extraction. Standardizing container-to-host path mappings makes this process incredibly robust and fast.
