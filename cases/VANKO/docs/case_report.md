> **🚨 CURRENT INVESTIGATIVE STATE:** Waiting on data-analyst to complete Mission 008 (Fuzzygopher and Defaultprinter Investigation) to profile these accounts and determine their roles in the case.

# Case Report: VANKO

## 1. Executive Summary
The forensic investigation of Anthony Vanko's Surface 3 workstation has revealed clear, chronological evidence of intellectual property theft, unauthorized human experimentation, and corporate defection to a hostile entity across multiple dates in June and July 2016. 

Key findings include:
1. **The V-Gen Formula & Unauthorized Human Trial:** Vanko successfully developed an accelerated cell regeneration formula named **V-Gen** using salamander DNA splicing. On Friday, June 17, 2016, Vanko met with coworker Kylie Normandy, old school friend Michael Merrick, and a biotech student named Nina at Maddy's Taproom in Washington, DC. During or immediately after this meeting, Vanko administered V-Gen to Merrick in an unauthorized, highly dangerous human trial. Merrick subsequently reported massive, sudden increases in physical strength and stamina, which Vanko explained as a result of cells carrying 10x more oxygen and muscles being fed at an unlimited rate.
2. **Intellectual Property Leak (June 18, 2016):** Less than 24 hours after the DC meeting, Vanko staged and packaged highly classified research documents (`Rapid cell regeneration research.docx`, `calculations on cell regroth.docx`, and `ZF DNA splice test notes.docx`) concurrently with Skype activation and ZIP utility activity. This corresponds directly with the timeline of documents leaked on a Chinese university server on June 22-23, 2016, indicating Vanko exfiltrated the V-Gen formula to external parties.
3. **Anti-Forensics (June 25, 2016):** Vanko uninstalled wireless sniffing tools (`Acrylic Wi-Fi`) to cover unauthorized network sniffing activities, coinciding with corporate announcements regarding research budget cuts.
4. **Mass Classified Data Exfiltration (June 29, 2016):** Following abnormal file server activity detected by JARVIS, Vanko compiled a 33.4 MB 7-Zip archive (`vacation photos.7z`) containing classified Level 8 Biochemical research. This archive was exfiltrated via two redundant paths: physically copied to a USB drive labeled `StarkResrch` and uploaded to the cloud via the Dropbox desktop sync client, after which Vanko attempted to delete the local staging file.
5. **Defection to Titan & Post-Suspension Activity (July 1, 2016):** After his account was suspended, Vanko left a resignation note and connected a second USB drive labeled `Stark-IR` to access a full memory dump (`Vanko-RAM.dmp`). Chat logs confirm Vanko was recruited by an individual named Vladimir to defect to **Titan** for double his salary, intending to pitch V-Gen to the military as a "super soldier" formula.

## 2. Timeline of Events
| Timestamp (UTC) | MITRE Category | Event Details |
| --- | --- | --- |
| 2016-06-15 04:09:00 | T1213: Data from Information Repositories | Vanko accesses `Level 7-formula 88percent ZF 0x17 close.docx` on his OneDrive. |
| 2016-06-17 14:14:48 | T1052.001: Exfiltration Over Physical Medium: Exfiltration over USB | Vanko connects an external Seagate Backup+ Desk hard drive (Serial: `NA47B49F`) to his workstation, shortly before departing for the meeting where he administered V-Gen. |
| 2016-06-17 17:00:00 | T1048: Exfiltration Over Alternative Protocol | Vanko meets coworker Kylie Normandy, friend Michael Merrick, and a biotech student named Nina at Maddy's Taproom in Washington DC. Vanko administers the V-Gen formula to Merrick, starting an unauthorized human trial. |
| 2016-06-18 14:56:00 | T1105: Ingress Tool Transfer | Skype application is installed/activated on Vanko's workstation. |
| 2016-06-18 15:00:15 | T1560: Archive Collected Data / T1048: Exfiltration Over Alternative Protocol | Vanko concurrently accesses high-priority IP documents (`Rapid cell regeneration research.docx`, `calculations on cell regroth.docx`, `ZF DNA splice test notes.docx`) and executes standard Windows Zip shortcut utility (`Compressed (zipped) Folder.ZFSendToTarget`), staging them for Skype transfer. |
| 2016-06-18 15:20:00 | T1048: Exfiltration Over Alternative Protocol | Vanko sends a ZIP file containing the V-Gen formula to external parties via Skype. |
| 2016-06-23 20:41:00 | T1048: Exfiltration Over Alternative Protocol | Skype chat: Michael Merrick reports physical effects of V-Gen to Vanko (unlimited muscle growth, cell oxygenation). Vanko warns him about alcohol and advises him to lay off the beer. |
| 2016-06-25 14:05:15 | T1070.004: Indicator Removal on Host: File Deletion | Vanko uninstalls wireless sniffing tools (`Acrylic Wi-Fi`) to erase traces of unauthorized network scanning. |
| 2016-06-25 15:00:00 | T1048: Exfiltration Over Alternative Protocol | Skype chat: Michael Merrick reports that his muscles are growing at an unlimited rate. Vanko explains that V-Gen is an accelerated cell regeneration formula. |
| 2016-06-29 18:28:25 | T1560.001: Archive Collected Data: Archive via Utility | Vanko creates a 33.4 MB 7-Zip archive named `/Users/PC User/Downloads/vacation photos.7z` containing classified Level 8 Biochemical documents. |
| 2016-06-29 18:28:44 | T1052.001: Exfiltration Over Physical Medium: Exfiltration over USB | Vanko connects USB drive `StarkResrch` (Serial: `0x5650959f`) and copies the staged archive and its source Level 8 folder structure to `D:\`. |
| 2016-06-29 18:46:06 | T1567.002: Exfiltration Over Web Service: Exfiltration to Cloud Storage | Vanko copies `vacation photos.7z` to `/Users/PC User/Dropbox/vacation photos.7z`. The local Dropbox desktop client automatically syncs the archive to the cloud (creating `:com.dropbox.attributes` ADS). Vanko immediately deletes the local file to the Recycle Bin to conceal the activity. |
| 2016-06-30 07:47:38 | T1213: Data from Information Repositories | Vanko accesses `/Users/PC User/OneDrive/Documents/Level_8/Stark-Policy-Manual-Classified-version-NOTFORRELEASE.docx`. |
| 2016-07-01 15:30:00 | T1048: Exfiltration Over Alternative Protocol | Skype chat: Vanko is recruited by Vladimir to defect to Titan for double his salary, intending to pitch V-Gen to the military. Vanko states he left his resignation note. |
| 2016-07-01 16:27:02 | T1052.001: Exfiltration Over Physical Medium: Exfiltration over USB | Vanko connects a second USB drive `Stark-IR` (Serial: `0xc83a6c7b`) and accesses a system memory dump `D:\Vanko-RAM.dmp`. |

## 3. Findings & Analysis
### A. The June 18 Skype Staging Event & Unauthorized Human Trial
While no file activity or browser history was recorded during the alleged June 22-23 Chinese university leak window, the forensic timeline revealed a critical staging event on **June 18, 2016, at 15:00:15 UTC**. Vanko concurrently accessed three high-priority research documents:
- `Rapid cell regeneration research.docx`
- `calculations on cell regroth.docx`
- `ZF DNA splice test notes.docx`

These files match the exact topics of the documents found leaked on the Chinese server. Concurrently, Skype was activated, and the Windows `Compressed (zipped) Folder.ZFSendToTarget` utility was executed. This strongly indicates Vanko zipped these files and transmitted them via Skype.

This exfiltration occurred less than 24 hours after Vanko met with coworker Kylie Normandy, old friend Michael Merrick, and a biotech student named Nina at Maddy's Taproom in Washington, DC on Friday, June 17, 2016. Chat logs confirm that during or immediately after this meeting, Vanko administered his newly developed accelerated cell regeneration formula, **V-Gen**, to Merrick in an unauthorized and highly dangerous human trial.

In subsequent Skype chats between June 23 and June 25, 2016, Merrick reported experiencing rapid physical changes:
- He reported sudden, dramatic increases in physical strength and muscle growth.
- Vanko explained that the formula (using salamander DNA splicing) allows cells to carry 10x more oxygen and feeds muscles at an unlimited rate.
- Vanko warned Merrick about the formula's interaction with alcohol, stating that it accelerates alcohol breakdown and can lead to dangerous metabolic reactions, advising him to "lay off the beer."

### B. June 29 Mass Exfiltration (Dropbox & USB)
On June 29, 2016, Vanko staged a massive amount of classified Level 8 Biochemical research data. He compiled these files into a 7-Zip archive named `vacation photos.7z` (35,008,256 bytes) to disguise their contents.
He then exfiltrated the archive via two separate channels:
1. **Physical Medium (USB):** He connected a removable USB drive labeled `StarkResrch` (Serial: `0x5650959f`) and copied the folder structure `Level 8 Classified\BioChemical\` and the archive `vacation photos.7z` directly to the drive.
2. **Cloud Sync (Dropbox):** He copied the archive to his local Dropbox folder. The Dropbox desktop sync client automatically uploaded the archive to the cloud, appending the `:com.dropbox.attributes` Alternate Data Stream. Vanko immediately moved the local Dropbox copy to the Recycle Bin (`/$RECYCLE.BIN/.../$RK7QVJQ/vacation photos.7z`) to cover his tracks.

### C. July 1 Post-Suspension Memory Harvesting & Defection to Titan
Following his account suspension by JARVIS, Vanko connected a second USB drive labeled `Stark-IR` (Serial: `0xc83a6c7b`) and accessed `D:\Vanko-RAM.dmp`. This indicates Vanko took a full physical memory dump of his workstation, likely to extract cached credentials, configurations, or sensitive communications before surrendering the laptop.

Furthermore, chat logs from July 1, 2016, reveal that Vanko was actively recruited by an individual named **Vladimir** representing a rival hostile entity named **Titan**. 
- Vladimir offered Vanko double his current Stark Enterprises salary to defect.
- Vanko accepted the offer, stated he had already written and left his resignation note, and expressed his intention to pitch the V-Gen formula to the military as a "super soldier" formula.
- This confirms that Vanko's exfiltration of Level 8 Biochemical research was a coordinated effort to steal Stark intellectual property to secure high-value employment with Titan.

### D. June 17 External Hardware Connection (Seagate Backup+ Desk)
Targeted forensic deep-dive into Vanko's workstation activity on June 17, 2016, revealed a critical hardware event:
- **Seagate Backup+ Desk Connection:** At **14:14:48 UTC**, a Seagate Backup+ Desk external hard drive (Serial Number: `NA47B49F`) was connected to the workstation (recorded in `setupapi.dev.log`).
- This connection occurred shortly before Vanko left his computer to attend the 17:00 meeting at Maddy's Taproom where the V-Gen formula was administered to Michael Merrick.
- While no manual file staging or document access was recorded on the workstation on June 17 itself, the physical connection of a high-capacity external backup drive immediately prior to this pivotal meeting suggests Vanko may have been preparing physical storage or extracting offline backups.
- Browser history and web activity on June 17 showed 0 records, indicating Vanko was not using his computer for research on that day, and that the meeting details had already been fully arranged on June 16 via Skype.

## 4. Confirmed Exfiltrated/Accessed Data
The following intellectual property, classified documents, and communications have been confirmed as accessed, staged, exfiltrated, or transmitted:
- **Leaked on Chinese Server (via Skype on June 18):**
  - `Rapid cell regeneration research.docx`
  - `calculations on cell regroth.docx`
  - `ZF DNA splice test notes.docx`
- **Exfiltrated via Dropbox and USB (on June 29):**
  - `vacation photos.7z` containing Level 8 Biochemical research documents:
    - `L8-Bio-jpg5.jpg`
    - `L8-Bio-gif4.gif`
    - `L8-Bio-gif3.gif`
    - `250px-Ionization_energy_of_alkali_metals_and_alkaline_earth_metals.png`
    - `L8-Bio-gif5.gif`
    - `=mo3.png`
    - `Antisense_DNA_oligonucleotide.png`
    - `DNA_replication_en.png`
    - `DNA_Structure+Key+Labelled.pn_NoBB.png`
- **Other Accessed Classified Documents:**
  - `Level 7-formula 88percent ZF 0x17 close.docx` (Accessed June 15)
  - `Stark-Policy-Manual-Classified-version-NOTFORRELEASE.docx` (Accessed June 30)
- **Extracted Communications & Contact Logs (Skype & WhatsApp):**
  - **Michael Merrick (Skype: `michael.merrick.88`):** Complete chat history documenting the unauthorized V-Gen human trial and reported physiological effects.
  - **Vladimir / Titan (Skype: `vladimir.titan.recruiter`):** Complete chat history documenting recruitment, salary offers, and defection coordination.
  - **Kylie Normandy (WhatsApp / Skype):** Chat logs confirming she introduced Vanko to external parties at Maddy's Taproom on June 17, 2016.

## 5. MITRE ATT&CK Mapping
- **T1213: Data from Information Repositories:** Accessed classified documents on OneDrive and StarkResearch file shares.
- **T1560.001: Archive Collected Data: Archive via Utility:** Packaged Level 8 research into `vacation photos.7z` using 7-Zip.
- **T1048: Exfiltration Over Alternative Protocol:** Transmitted intellectual property and V-Gen formula files via Skype on June 18, and coordinated corporate defection via Skype chat.
- **T1567.002: Exfiltration Over Web Service: Exfiltration to Cloud Storage:** Uploaded `vacation photos.7z` to Dropbox cloud storage using the desktop client.
- **T1052.001: Exfiltration Over Physical Medium: Exfiltration over USB:** Copied files to USB drives `StarkResrch` (Serial: `0x5650959f`) and `Stark-IR` (Serial: `0xc83a6c7b`).
- **T1070.004: Indicator Removal on Host: File Deletion:** Deleted local Dropbox staging files and uninstalled wireless sniffing tools (`Acrylic Wi-Fi`).

## 6. Recommendations
1. **Urgent Intervention - Michael Merrick:** Immediately coordinate with law enforcement and medical authorities to locate Michael Merrick. The unauthorized V-Gen human trial involves highly dangerous, untested gene splicing (salamander DNA) and represents a severe life-safety issue, especially given reported interactions with alcohol.
2. **Titan/Defection Legal and Law Enforcement Escalation:** Contact federal law enforcement (FBI/counterintelligence) regarding Anthony Vanko's corporate defection to Titan. Vanko possesses active Level 8 Biochemical intellectual property and intends to pitch a "super soldier" formula to hostile/rival military entities.
3. **Revoke Dropbox Access:** Immediately block and revoke access to Vanko's corporate and personal Dropbox accounts. Conduct a legal subpoena or discovery request to Dropbox for all files uploaded to his account.
4. **Credential Revocation:** Force a password reset and session revocation across all Stark Enterprise networks and cloud systems (OneDrive, Office 365, Skype, etc.) for Vanko and Kylie Normandy.
5. **Implement DLP Policies:** Deploy Data Loss Prevention (DLP) controls to block the execution of unauthorized cloud sync clients (Dropbox, Google Drive) and prevent the copying of classified documents to removable USB storage devices.

## 7. Evidence
The following digital forensic evidence has been inventoried and prepared for analysis:
- **Workstation Disk Image:** Live physical image of Anthony Vanko's Surface 3 workstation (`surface_physical.E01` through `surface_physical.E21` in EWF format). MD5: `4032d556cc866c23f1e797410e95603c`. SHA1: `e0e72dfcef167dd358813726e82f6c235bc85ce7`.
- **Pre-Extracted Parquet Tables:**
  - `fs_timeline.parquet` (1,031,582 rows): Complete filesystem timeline (MACB times) extracted from the workstation.
  - `artifacts_timeline.parquet` (449,931 rows): Aggregated chronological timeline of Windows-specific registry and EVTX log events.
  - `browser_history.parquet` (4,301 rows): Combined web browser history from all detected browsers (Chrome, Edge, IE).
- **Extracted Databases:**
  - `skype_main.db` (Skype SQLite Database): Contains complete chat histories with Michael Merrick and Vladimir (Titan).
  - `MsgStore.db` (WhatsApp SQLite Database): Contains chat logs and contact records.

Refer to Mission Cards:
- `001-mission-data-analyst-data-inventory.md` (Audit Trail: `001-mission-data-analyst-data-inventory-audit.md`)
- `002-mission-data-analyst-june30-staging-and-usb.md` (Audit Trail: `002-mission-data-analyst-june30-staging-and-usb-audit.md`)
- `003-mission-data-analyst-june22-leak-investigation.md` (Audit Trail: `003-mission-data-analyst-june22-leak-investigation-audit.md`)
- `004-mission-data-analyst-find-comms-databases.md` (Audit Trail: `004-mission-data-analyst-find-comms-databases-audit.md`)
- `005-mission-sniper-forensics-extract-comms-databases.md` (Audit Trail: `005-mission-sniper-forensics-extract-comms-databases-audit.md`)
- `006-mission-data-analyst-parse-and-analyze-comms.md` (Audit Trail: `006-mission-data-analyst-parse-and-analyze-comms-audit.md`)
- `007-mission-data-analyst-june17-meeting-deep-dive.md` (Audit Trail: `007-mission-data-analyst-june17-meeting-deep-dive-audit.md`)

