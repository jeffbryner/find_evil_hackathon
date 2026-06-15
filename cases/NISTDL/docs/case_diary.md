> **🚨 CURRENT INVESTIGATIVE STATE:** Investigation completed. Successfully reconstructed the wiped `[QAT` folder, analyzed Google Drive Sync logs, and carved/analyzed 16 exfiltrated documents from Removable Media 2 (USB) which were masqueraded with decoy extensions.

# NISTDL Case Diary

## 1. Executive Summary
The forensic investigation into the NISTDL case has successfully reconstructed the timeline and mechanism of a major data leakage event. The primary user `informant` on host `INFORMANT-PC` exfiltrated 16 highly sensitive corporate documents regarding a confidential project labeled **`[secret_project]`** using **Removable Media 2 (USB)**. 

To evade detection, the user employed sophisticated anti-forensics and defense evasion techniques:
1. **File Masquerading:** Every exfiltrated document on the USB drive was renamed with a decoy extension (e.g., `.txt`, `.zip`, `.db`, `.png`, `.gif`, `.amr`, `.svg`, `.one`, `.jpg`, `.avi`) to conceal its true identity as a Microsoft Office document (Word, PowerPoint, Excel).
2. **File Wiping:** The user used **Eraser** (`ERASER.EXE`) to securely wipe files in the Recycle Bin and a desktop folder named `C:\Users\informant\Desktop\[QAT`. Our reconstruction of this folder using the NTFS Change Journal (`$UsnJrnl`) revealed it contained only standard Windows 7 sample pictures and an IE11 installer, indicating it was likely a decoy/distraction or used to test the wiping software.
3. **System Cleaning:** The user ran **CCleaner** (`CCLEANER64.EXE`) to clean system and browser traces, then immediately uninstalled it to hide its presence.
4. **Decoy Sync Session:** The user ran **Google Drive Sync** (`GOOGLEDRIVESYNC.EXE`) and accessed their personal Google storage settings via Chrome (`iaman.informant.personal@gmail.com`). However, our analysis of the Google Drive sync logs confirmed that **0 local or cloud changes were synced on 2015-03-25**, proving no data leakage occurred via Google Drive Sync on that day.

All 16 sensitive documents have been successfully carved, extracted, and identified, confirming the full scope of the exfiltrated intellectual property.

## 2. Timeline of Events
| Timestamp | MITRE ATT&CK Category | Event Details |
| --- | --- | --- |
| 2015-03-22 14:34:26 UTC | Initial Setup | OS Installation on host `INFORMANT-PC` (Windows 7 Ultimate SP1) with primary user `informant`. |
| 2015-03-23 11:31:11 UTC | Reconnaissance / Initial Access | SanDisk Cruzer Fit USB device (Serial: `4C530012450531101593`) first connected to the host. |
| 2015-03-24 06:58:33 UTC | Reconnaissance / Initial Access | SanDisk Cruzer Fit USB device (Serial: `4C530012550531106501`) first connected to the host. |
| 2015-03-24 11:48:40 UTC | Collection | File `Resignation_Letter_(Iaman_Informant).docx` created on Desktop. |
| 2015-03-25 14:47:34 UTC | Defense Evasion | User `informant` searched Bing for "eraser" and downloaded `Eraser 6.2.0.2962.exe` to Desktop/Download (Local: 07:47:34 Pacific). |
| 2015-03-25 14:47:51 UTC | Defense Evasion | User `informant` searched Bing for "ccleaner" and downloaded `ccsetup504.exe` to Desktop/Download (Local: 07:47:51 Pacific). |
| 2015-03-25 14:57:56 UTC | Defense Evasion | CCleaner installer `CCSETUP504.EXE` executed (Local: 07:57:56 Pacific). |
| 2015-03-25 15:13:30 UTC | Defense Evasion | **Eraser** executed (`ERASER.EXE`), wiping files in Recycle Bin and the folder `C:\Users\informant\Desktop\[QAT`. (Wiped files carry corrupted MFT timestamps of `2076-11-29`) (Local: 08:13:30 Pacific). |
| 2015-03-25 15:15:50 UTC | Defense Evasion | **CCleaner** executed (`CCLEANER64.EXE`) to clean browser history and system traces (Local: 08:15:50 Pacific). |
| 2015-03-25 15:18:29 UTC | Defense Evasion | CCleaner uninstaller `UNINST.EXE` executed to hide traces of CCleaner (Local: 08:18:29 Pacific). |
| 2015-03-25 15:21:31 UTC | Exfiltration | Google Drive Sync executed (`GOOGLEDRIVESYNC.EXE`) (Local: 08:21:31 Pacific). |
| 2015-03-25 15:21:34 UTC | Exfiltration | Google Drive Sync log (`sync_log.log`) confirms session started; both local and cloud scanners reported `0 changes found`. No files were synced (Local: 11:21:34 Eastern/08:21:34 Pacific). |
| 2015-03-25 15:22:08 UTC | Exfiltration | Chrome used to log into personal Google account `iaman.informant.personal@gmail.com` and access Google storage settings (`/settings/storage`) (Local: 08:22:08 Pacific). |
| 2015-03-25 15:28:33 UTC | Collection | Opened and viewed `Resignation_Letter_(Iaman_Informant).xps` on Desktop (Local: 08:28:33 Pacific). |
| 2015-03-25 15:29:08 UTC | Collection | Opened and viewed `Resignation_Letter_(Iaman_Informant).docx` on Desktop (Local: 08:29:08 Pacific). |

## 3. Findings & Analysis
- **Anti-Forensics & File Masquerading:** The user `informant` copied 16 highly sensitive corporate files regarding `[secret_project]` to Removable Media 2 (USB) and renamed them with decoy extensions (e.g., `.txt`, `.zip`, `.db`, `.png`, `.gif`, `.amr`, `.svg`, `.one`, `.jpg`, `.avi`) to bypass extension-based security filters. We successfully carved and extracted all 16 files, verifying their true identity as Word, Excel, and PowerPoint documents.
- **Wiped Decoy Directory:** Eraser was used to wipe the folder `C:\Users\informant\Desktop\[QAT`. By parsing the NTFS Change Journal (`$UsnJrnl:$J`) and tracing the `RENAME_OLD_NAME` events, we reconstructed the folder contents: it contained only standard Windows 7 sample pictures and an Internet Explorer 11 installer. This indicates the folder was a decoy or used to test the wiping utility before execution.
- **Google Drive Sync Analysis:** While `GOOGLEDRIVESYNC.EXE` was executed and Chrome was used to log into `iaman.informant.personal@gmail.com`, analysis of `sync_log.log` confirms that no files were synced or uploaded on **2015-03-25**.
- **USB Storage Device Use:** Two SanDisk Cruzer Fit USB drives were connected. Removable Media 2 (`rm2.dd`) was used to store the masqueraded, deleted/orphaned files under `/$OrphanFiles/`.

## 4. Confirmed Exfiltrated/Accessed Data
- **Confidential Project Documents:** 16 Microsoft Office documents (Word, Excel, PowerPoint) related to `[secret_project]` were exfiltrated via the USB drive. These documents contain detailed designs, proposals, market shares, price analyses, progress reports, and technical reviews.
- **Resignation Letter:** `Resignation_Letter_(Iaman_Informant).docx` and `.xps` were accessed on the desktop.

## 5. MITRE ATT&CK Mapping
- **T1027.005 (Indicator Removal on Host: Masquerading):** Renaming sensitive Office documents with decoy extensions (like `.txt`, `.png`, `.avi`) to evade detection.
- **T1070.004 (Indicator Removal on Host: File Deletion):** Securely wiping decoy files using Eraser and deleting exfiltrated files on the USB.
- **T1070.006 (Indicator Removal on Host: Timestomp):** Eraser timestomping wiped files to `2076-11-29`.
- **T1052.001 (Exfiltration Over Physical Medium: Exfiltration over USB):** Copying sensitive documents to the USB drive.
- **T1071.001 (Application Layer Protocol: Web Protocols):** Personal Google Drive access via Chrome.
- **T1567.002 (Exfiltration Over Web Service: Exfiltration to Cloud Storage):** Use of Google Drive Sync.

## 6. Recommendations
- **Impact Assessment:** Immediately assess the impact of the leak of `[secret_project]` intellectual property (including designs, proposals, and pricing).
- **Endpoint DLP Implementation:** Deploy robust DLP solutions to block unauthorized USB mass storage devices and alert on the execution of anti-forensics tools (like Eraser and CCleaner).
- **MIME-Type Verification:** Implement file scanning solutions that verify file headers (magic bytes) rather than relying solely on file extensions.
- **Access Control:** Restrict local administrator privileges (the user had access to run installers and wipe tools) and monitor system uninstallation events.

## 7. Evidence
- **Host Image:** `cfreds_2015_data_leakage_pc.dd`
- **USB Image:** `cfreds_2015_data_leakage_rm2.dd` / `cfreds_2015_data_leakage_rm2.E01`
- **Mission Cards:**
  - `001-mission-data-analyst-inventory-and-triage.md` (Initial inventory and triage)
  - `002-mission-data-analyst-google-drive-and-ntfs-reconstruction.md` (Google Drive and NTFS Reconstruction)
  - `003-mission-sniper-forensics-rm2-carving.md` (Removable Media 2 File Carving and Extraction)
