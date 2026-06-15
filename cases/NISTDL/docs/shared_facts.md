# Data Inventory
- **Primary Host:** `cfreds_2015_data_leakage_pc.dd`
  - Hostname: `INFORMANT-PC`
  - OS: Windows 7 Ultimate SP1 (Build 7601)
  - Installation Date: 2015-03-22 14:34:26 UTC (2015-03-22 07:34:26-07:00)
  - Registered Owner: `informant`
  - Users: `Administrator` (RID 500, Login Count 6), `Guest` (RID 501, Login Count 0), `informant` (RID 1000, Login Count 10), `admin11` (RID 1001, Login Count 2), `ITechTeam` (RID 1002, Login Count 0), `temporary` (RID 1003, Login Count 1)
  - Parquet Tables: `fs_timeline` (344,088 records), `artifacts_timeline` (229,562 records), `browser_history` (1,234 records)
- **Removable Media 2 (USB Drive):** `cfreds_2015_data_leakage_rm2.dd` / `cfreds_2015_data_leakage_rm2.E01`
  - Parquet Tables: `fs_timeline` (139 records, contains deleted files under `/$OrphanFiles/`)
  - **Carved & Extracted Files:** All 16 files from `/$OrphanFiles/` have been carved and analyzed.
  - **Masquerading/Anti-Forensics:** Every file was renamed with a decoy extension to conceal its true identity as a Microsoft Office document associated with `[secret_project]`.
    - `diary_#1d.txt` (119K) -> Word 2007+ (.docx) `[Secret Project]Technical Review #1.docx`
    - `diary_#1p.txt` (448K) -> PowerPoint 2007+ (.pptx) `[Secret Project]technical_review_#1.pptx`
    - `diary_#2d.txt` (643K) -> Word 2007+ (.docx) `[Secret Project]Technical Review #2.docx`
    - `diary_#2p.txt` (1.1M) -> PowerPoint 97-2003 (.ppt) `[secret_project]_technical_review_#2`
    - `diary_#3d.txt` (2.3M) -> Word 97-2003 (.doc) `[secret_project]_technical_review_#3`
    - `diary_#3p.txt` (318K) -> PowerPoint 97-2003 (.ppt) `[secret_project]_technical_review_#3`
    - `winter_whether_advisory.zip` (16M) -> PowerPoint 2007+ (.pptx) `[Secret Project]detailed_design.pptx`
    - `my_favorite_cars.db` -> Excel 97-2003 (.xls) `[secret_project]_price_analysis_#2`
    - `my_favorite_movies.7z` -> Excel 2007+ (.xlsx) (Nutrient constituents reference sample data)
    - `my_friends.svg` -> Word 97-2003 (.doc) `[secret_project]_progress_#3`
    - `my_smartphone.png` -> Word 2007+ (.docx) `[Secret Project]Progress #1.docx`
    - `new_year_calendar.one` -> Word 2007+ (.docx) `[Secret Project]Progress #2.docx`
    - `winter_storm.amr` -> PowerPoint 97-2003 (.ppt) `[Secret Project]revised_points.ppt`
    - `a_gift_from_you.gif` -> Word 2007+ (.docx) `[Secret Project]Detailed Proposal.docx`
    - `landscape.png` -> Word 2007+ (.docx) `[Secret Project]Proposal.docx`
    - `new_years_day.jpg` -> Excel 2007+ (.xlsx)
    - `super_bowl.avi` -> Excel 97-2003 (.xls) `[secret_project]_market_shares`
- **Removable Media 3 (USB/ISO):** `cfreds_2015_data_leakage_rm3_type1.iso` / `cfreds_2015_data_leakage_rm3_type2.dd` / `cfreds_2015_data_leakage_rm3_type3.E01`
  - Parquet Tables: `fs_timeline` (0 records, empty)

# Compromised Accounts
- **informant** (RID 1000) - Personal email: `iaman.informant.personal@gmail.com`. Used to access personal Google storage and viewed/edited resignation letter on the primary host.

# Known Malicious IPs & Domains
*None identified yet.*

# Suspicious Files & Staging Directories
- `C:\Users\informant\Desktop\Resignation_Letter_(Iaman_Informant).docx` (Created: 2015-03-24 11:48:40, accessed 2015-03-25 08:29:08)
- `C:\Users\informant\Desktop\Resignation_Letter_(Iaman_Informant).xps` (Created/Accessed: 2015-03-25 08:28:33)
- `C:\Users\informant\Desktop\Download\Eraser 6.2.0.2962.exe` (Downloaded: 2015-03-25 07:47:40, deleted)
- `C:\Users\informant\Desktop\Download\ccsetup504.exe` (Downloaded: 2015-03-25 07:48:28, deleted)
- `C:\Users\informant\Desktop\[QAT` (Deleted/Wiped by Eraser on 2015-03-25 08:13:49)

# Decoded Payloads & Scripts
*None identified yet.*

# Confirmed Exfiltrated/Accessed Data
- **Google Drive Sync:** `GOOGLEDRIVESYNC.EXE` executed on 2015-03-25 08:21:31. Personal Google account storage was accessed via Chrome around 2015-03-25 08:22:08.
- **USB Devices Connected:**
  - SanDisk Cruzer Fit (Serial: `4C530012450531101593`, First Connected: 2015-03-23 11:31:11)
  - SanDisk Cruzer Fit (Serial: `4C530012550531106501`, First Connected: 2015-03-24 06:58:33)
- **Removable Media 2 Wiped/Orphaned Data:**
  - 16 files were deleted/orphaned on the USB drive, grouped in folders `design`, `PRICIN~1`, `progress`, `proposal`, and `TECHNI~1`.
  - The files contain design documents, price analyses, progress reports, proposals, and technical reviews for a confidential project (`[secret_project]`).
  - These files were masqueraded with decoy names and extensions (e.g. `.txt`, `.7z`, `.zip`, `.db`, `.png`, `.gif`, `.amr`, `.svg`, `.one`, `.jpg`, `.avi`) to evade standard forensic detection.
  - The files were successfully carved/extracted from the `cfreds_2015_data_leakage_rm2.dd` image under `/$OrphanFiles/`.

# Known Forensic Artifacts (IGNORE)
*None identified yet.*
