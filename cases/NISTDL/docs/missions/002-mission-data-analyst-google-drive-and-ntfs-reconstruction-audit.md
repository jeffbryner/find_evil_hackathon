# Forensic Audit Trail: Google Drive and NTFS Reconstruction

**Case ID:** NISTDL  
**Investigator:** data-analyst  
**Date:** 2026-06-03  

## Objective
To determine what files were exfiltrated via Google Drive Sync, and reconstruct the contents of the wiped `C:\Users\informant\Desktop\[QAT` folder using NTFS artifacts (such as `$UsnJrnl`).

---

## Technical Actions & SQL Queries

### 1. Google Drive Sync Configuration & Database Analysis
- **Query 1:** Searched the filesystem timeline (`fs_timeline`) for paths related to Google Drive user configurations.
  ```sql
  SELECT timestamp, data_type, parser, message, file_name_lower 
  FROM fs_timeline 
  WHERE file_name_lower ILIKE '%/users/informant/%/google/drive/%' 
  LIMIT 100;
  ```
  *Result:* Identified active log files and deleted databases under `/Users/informant/AppData/Local/Google/Drive/user_default/`, including `sync_log.log`, `snapshot.db`, and `sync_config.db`.
  
- **Action:** Read and analyzed `sync_log.log` from the mounted filesystem of the primary host:
  - Located the local Google Drive folder path: `C:\Users\informant\Google Drive`.
  - Analyzed the sync session on `2015-03-25` starting at `11:21:34 -0400` (15:21:34 UTC).
  - *Findings:* The log confirmed that **0 changes** were detected and **no files were synced or uploaded** during this session.
  - *Historical Findings:* On `2015-03-23`, the user synced (uploaded) and subsequently deleted two files: `happy_holiday.jpg` and `do_u_wanna_build_a_snow_man.mp3`.

---

### 2. NTFS Journal ($UsnJrnl) Extraction & Reconstruction
- **Action:** Located and extracted the NTFS change journal data stream (`$UsnJrnl:$J`, inode `59016-128-3`) from the primary host partition starting at sector `206848`:
  ```bash
  icat -o 206848 /tmp/image_mounter_s_6rh09o/cfreds_2015_data_leakage_pc.dd 59016-128-3 > /scratch/UsnJrnl_J
  ```
- **Action:** Parsed the raw `$UsnJrnl:$J` stream into a CSV format inside the SIFT workstation container:
  ```bash
  usnparser -f /scratch/UsnJrnl_J -o /scratch/usn_parsed.csv -c
  ```
- **Query 2:** Queried the parsed USN journal to identify files renamed and deleted by Eraser (`ERASER.EXE`) around `15:13 UTC` (08:13 local time) on `2015-03-25`:
  ```sql
  SELECT DISTINCT filename 
  FROM read_csv_auto('cases/NISTDL/scratch/usn_parsed.csv', ignore_errors=true) 
  WHERE timestamp >= '2015-03-25 15:13:30' 
    AND timestamp <= '2015-03-25 15:14:00' 
    AND reason ILIKE '%RENAME_OLD_NAME%' 
  ORDER BY filename;
  ```
  *Result:* Identified the original filenames of the files inside `C:\Users\informant\Desktop\[QAT` before they were renamed to random characters and wiped by Eraser:
  - `Chrysanthemum.jpg`
  - `Desert.jpg`
  - `Hydrangeas.jpg`
  - `IE11-Windows6.1-x64-en-us.exe` (Internet Explorer 11 Installer)
  - `Jellyfish.jpg`
  - `Koala.jpg`
  - `Lighthouse.jpg`
  - `Penguins.jpg`
  - `Tulips.jpg`

---

## Conclusion & Evidence Summary
1. **No Cloud Exfiltration via Google Drive Sync on 2015-03-25:** Although `GOOGLEDRIVESYNC.EXE` was executed on `2015-03-25 15:21:31 UTC`, the `sync_log.log` confirms that the local disk scan found 0 changes and no files were uploaded or downloaded.
2. **Reconstructed [QAT Folder Contents:** The folder `C:\Users\informant\Desktop\[QAT` contained standard Windows sample pictures and an Internet Explorer 11 installer, which were securely wiped by Eraser on `2015-03-25 15:13:49 UTC` (08:13:49 local time).
