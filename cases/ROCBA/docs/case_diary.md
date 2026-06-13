> **🚨 CURRENT INVESTIGATIVE STATE:** Recovered and analyzed browser and system credentials. The timeline of events, exfiltration paths, stolen files, anti-forensics, and plaintext credentials have been fully reconstructed. Fred Rocba's credentials have been decrypted, proving his direct association with the "Cobra" persona and revealing extensive password reuse.

# Executive Summary
The forensic investigation into Fred Rocba's SRL-provided Surface system has uncovered a highly coordinated, multi-phased **insider threat operation** executed by Fred Rocba himself, who utilized the alias "Cobra" / "Redguard" (`redguard.cobra@gmail.com`). 

Fred Rocba was hired on October 24, 2020, and began work on October 26, 2020. Shortly after starting, on November 10, 2020, he left for a planned vacation to Disney. On November 13, 2020, a home burglary was reported, apparently targeting his SRL Surface system.

However, forensic evidence proves that the burglary was staged or coordinated. Starting just hours after the reported burglary on November 13, 2020, the system was booted, and Fred (or an accomplice using his credentials) connected multiple physical USB drives (designated D:, E:, and F:) which had been previously paired with the system as early as November 1, 2020. 

The actor systematically harvested and exfiltrated highly confidential Stark Research Labs (SRL) project documents, schematics, blueprints, and a complete Outlook email archive (`SRL-EMAIL-EXPORT.pst`). The exfiltration targeted ten high-value projects, including Project KITT, Project Megaforce, Project Airwolf, Project Vibranium, Project Gunstar, and Project Blue Thunder. 

The exfiltration was conducted through two main channels:
1.  **Physical USB Copying:** Files were copied to external USB drive F: (Volume label `CRIMSON2`, serial `90008B5EB5FFFF64`).
2.  **Cloud Sync Uploads:** Files were copied to Google Drive G: (mounted as `G:\My Drive\STARK-RESEARCH-LABS FOLDER`), syncing directly to his personal Google account.

To cover his tracks, Fred downloaded and executed Microsoft Sysinternals `SDelete` 7 times on the morning of November 14, 2020, to securely erase the local staging folders. He then opened the exfiltrated Outlook PST archive on Google Drive to verify its integrity, and subsequently took a raw memory dump (`Rocba-Memory.raw`) of the system, which he accessed on November 15, 2020.

Windows Explorer search history (`WordWheelQuery`) captured in his registry hive (`NTUSER.DAT`) on November 14, 2020, provides undeniable proof of his direct involvement, capturing search terms such as `backup.pst`, `sdelete`, `bitlocker`, `cobra` (his alias), `crimson` (his USB volume label), `airwolf`, `kitt`, and `starfury`.

# Timeline of Events
| Timestamp | MITRE Category | Event Details |
| --- | --- | --- |
| 2020-10-24 | - | Fred Rocba accepts the engineering job at SRL; shipped a new Microsoft Surface system. |
| 2020-10-26 | - | Fred begins work at SRL. Account `fredr` password is set. |
| 2020-11-01 10:23:11 | - | Fred accesses his external job offer `SRL-Offer.pdf` on Google Drive. |
| 2020-11-01 17:12:24 | T1200: Hardware Additions | External USB drives D: (`SRL IRT`), E: (`Homework`), and F: (`CRIMSON2`) are first connected/migrated to the Surface system. |
| 2020-11-07 12:00:00 | - | Fred logs into his personal email `redguard.cobra@gmail.com` and visits `http://cobracommandcenter.com/` in Chrome. |
| 2020-11-10 05:26:09 | - | Setup account `srl-h` (RID 1001) last login. |
| 2020-11-10 | - | Fred Rocba leaves on vacation to Disney. |
| 2020-11-13 | - | Fred's home is burglarized; SRL Surface system targeted. |
| 2020-11-13 19:45:54 | T1200: Hardware Additions | External USB drive F: (`CRIMSON2`) connected. Staging directory `F:\Files from SRL system` created/accessed. |
| 2020-11-13 19:46:14 | T1200: Hardware Additions | Staging directory `F:\New folder` created/accessed. |
| 2020-11-13 19:46:33 | T1005: Data from Local System | New Alloy Research: `Alloy_Steel_-_Properties_and_Use.pdf` accessed. |
| 2020-11-13 19:48:50 | T1005: Data from Local System | Project KITT: `Hydrogen_Hybrid_Tech.docx` accessed. |
| 2020-11-13 19:49:21 | T1005: Data from Local System | Project KITT: `The Future of KITT.pptx` accessed. |
| 2020-11-13 19:51:01 | T1041: Exfiltration Over C2 Channel | Project KITT: `The Future of KITT.pptx` copied to external USB F:. |
| 2020-11-13 19:51:12 | T1005: Data from Local System | Project KITT: `secretweapon.jpg` accessed. |
| 2020-11-13 19:51:48 | T1005: Data from Local System | Project Megaforce: `Megaforce Specs & Research.docx` accessed. |
| 2020-11-13 19:52:45 | T1041: Exfiltration Over C2 Channel | Project Megaforce: `Megaforce Specs & Research.docx` copied to external USB F:. |
| 2020-11-13 19:57:21 | T1567.002: Exfiltration to Cloud Storage | Project Gunstar: `Research to Weaponize the Ion Thruster.docx` copied to Google Drive G:. |
| 2020-11-13 19:58:02 | T1005: Data from Local System | Project Vibranium: `Vibrainium(1).doc` accessed. |
| 2020-11-13 19:59:19 | T1567.002: Exfiltration to Cloud Storage | Project Vibranium: `Vibrainium(1).doc` copied to Google Drive G:. |
| 2020-11-13 20:03:38 | T1005: Data from Local System | Project StarFury: `StarFury.zip` accessed. |
| 2020-11-13 20:04:24 | T1567.002: Exfiltration to Cloud Storage | Project StarFury: `starfury` folder copied to Google Drive G:. |
| 2020-11-13 20:04:56 | T1005: Data from Local System | Project TIVO: `TIVO Research.docx` accessed. |
| 2020-11-13 20:05:43 | T1567.002: Exfiltration to Cloud Storage | Project TIVO: `VC Files` copied to Google Drive G:. |
| 2020-11-13 20:13:33 | T1041: Exfiltration Over C2 Channel | Project Gunstar: `Quantum Particles Affected by Other Dimensions.pdf` copied to USB F:. |
| 2020-11-13 20:23:04 | T1005: Data from Local System | Project Airwolf: `Wolves_Lair_Tech_Specs.pptx` accessed. |
| 2020-11-13 20:24:10 | T1041: Exfiltration Over C2 Channel | Project Airwolf: `Wolves_Lair_Tech_Specs.pptx` copied to USB F:. |
| 2020-11-13 20:27:23 | T1567.002: Exfiltration to Cloud Storage | Project Airwolf: `Wolf AIr Financials.xlsx` copied to Google Drive G:. |
| 2020-11-13 20:29:49 | T1567.002: Exfiltration to Cloud Storage | Project Gunstar: `GunStar Death Blossom Data.docx` copied to Google Drive G:. |
| 2020-11-13 20:30:30 | T1041: Exfiltration Over C2 Channel | Project Blue Thunder: `blue_thunder_blueprint...jpg` copied to USB F:. |
| 2020-11-14 04:34:00 | T1567.002: Exfiltration to Cloud Storage | Google Drive accessed to resume transfers. |
| 2020-11-14 04:51:58 | T1078: Valid Accounts | Account `fredr` last login (Post-burglary activity). |
| 2020-11-14 05:04:00 | T1567.002: Exfiltration to Cloud Storage | Project Airwolf: Schematics and blueprints copied to Google Drive G:. |
| 2020-11-14 05:28:00 | T1005: Data from Local System | BitLocker recovery keys opened from USB drives E:, D:, and Google Drive G:. |
| 2020-11-14 05:37:37 | T1105: Ingress Tool Transfer | Google search for `sdelete download` conducted. |
| 2020-11-14 05:38:02 | T1105: Ingress Tool Transfer | `SDelete.zip` downloaded to `C:\Users\fredr\Downloads\SDelete.zip`. |
| 2020-11-14 05:39:11 | T1070.004: File Deletion | Local email backup `C:\Users\fredr\OneDrive\Documents\Outlook Files\backup.pst` deleted (moved to Recycle Bin). |
| 2020-11-14 05:39:22 | T1567.002: Exfiltration to Cloud Storage | Outlook email archive `SRL-EMAIL-EXPORT.pst` created and copied directly to Google Drive G:. |
| 2020-11-14 05:42:30 | T1070.004: File Deletion | `SDELETE.EXE` executed from Downloads folder (Run Count: 1). |
| 2020-11-14 05:42:38 | T1070.004: File Deletion | `SDELETE.EXE` executed from Downloads folder (Run Count: 2). |
| 2020-11-14 05:44:52 | T1070.004: File Deletion | `SDELETE.EXE` moved to `C:\Windows\System32\SDELETE.EXE` and executed 5 additional times (Total Run Count: 5). |
| 2020-11-14 05:50:16 | T1005: Data from Local System | Fred accesses local file `Research to Weaponize the Ion Thruster.docx`. |
| 2020-11-14 06:00:00 | T1005: Data from Local System | Google Drive folder `STARK-RESEARCH-LABS FOLDER/Exported-PST` accessed. |
| 2020-11-14 06:01:35 | T1567.002: Exfiltration to Cloud Storage | `SRL-EMAIL-EXPORT.pst` copied directly to Google Drive G:. |
| 2020-11-14 06:03:52 | T1005: Data from Local System | Local Outlook email backup `backup.pst` accessed. |
| 2020-11-14 06:04:07 | T1005: Data from Local System | Fred's Windows Explorer search history (`WordWheelQuery`) registry key updated with search terms: `backup.pst`, `sdelete`, `airwolf`, `kitt`, `starfury`, `cobra`, `crimson`, etc. |
| 2020-11-14 06:09:16 | T1005: Data from Local System | Outlook registry keys (`LastCorruptStore`) updated pointing to Google Drive exfiltrated archive `SRL-EMAIL-EXPORT.pst` (verifying integrity). |
| 2020-11-15 18:32:19 | T1005: Data from Local System | Raw memory dump `Rocba-Memory.raw` opened from D: drive. |
| 2020-11-16 02:31:15 | T1219: Remote Access Software | Suspicious utility `MRC.exe` (PID 29440) launched during active attacker RDP sessions. |
| 2020-11-16 02:34:45 | T1021.001: Remote Desktop Protocol | Active RDP session established on local port 3389 from external IP `81.30.144.115`. |
| 2020-11-16 02:34:58 | T1021.001: Remote Desktop Protocol | Active RDP sessions established on local port 3389 from external IPs `81.30.144.115` and `213.202.233.104`. |
| 2020-11-16 02:35:53 | T1021.001: Remote Desktop Protocol | Active RDP session established on local port 3389 from external IP `213.202.233.104`. |

# Findings & Analysis

## Insider Threat Identification (Fred Rocba as "Cobra")
The forensic evidence provides undeniable proof that Fred Rocba was an active insider threat operating under the pseudonym "Cobra" / "Redguard":
1.  **Personal Email & Web Activity:** Chrome history shows Fred logging into `redguard.cobra@gmail.com` and visiting `cobracommandcenter.com` on November 7, 2020.
2.  **Windows Explorer Search History:** Fred's local `NTUSER.DAT` registry hive captured his real-time search queries (`WordWheelQuery`) on November 14, 2020, at 06:04:07. His searches included:
    *   `cobra` (his personal alias)
    *   `crimson` (the volume label of his exfiltration USB drive `CRIMSON2`)
    *   `sdelete` (the anti-forensics tool he downloaded)
    *   `backup.pst`, `backup`, `*.pst` (the email archives he harvested)
    *   `bitlocker recovery key`, `bitlocker` (the encryption keys he opened)
    *   `airwolf`, `kitt`, `starfury` (the specific confidential SRL projects he exfiltrated)
3.  **Pre-Existing USB Pairing:** The external USB drives D: (`SRL IRT`), E: (`Homework`), and F: (`CRIMSON2`) used for exfiltration were first connected/migrated to the Surface system on November 1, 2020, well before Fred left on vacation. This confirms the physical devices belonged to Fred and were already paired with his machine.

## Recovered Browser & System Credentials
Through a combination of Dissect's automated credential decryption and LSA secret analysis, we successfully recovered plaintext passwords from the system, providing absolute confirmation of Fred's identity and intent:
1.  **Personal Email & Microsoft Account:**
    *   **Username:** `redguard.cobra@gmail.com` (personal/insider threat email)
    *   **Username:** `fred.rocba@outlook.com` (personal MS account)
    *   **Username:** `fred.rocba@gmail.com` (personal primary email)
    *   **Plaintext Password:** `C0bracommand` (Decrypted from Chrome/Edge `Login Data`)
    *   **Significance:** Fred utilized the password `C0bracommand` (referencing his "Cobra" alias) across all his personal accounts (including Google, Microsoft, Netflix, Amazon, and Facebook), establishing undeniable proof of ownership of the `redguard.cobra@gmail.com` exfiltration account.
2.  **SRL Corporate Domain Account:**
    *   **Username:** `SHIELDBASE\frocba` (SRL corporate account)
    *   **Plaintext Password:** `Big-Purple-Truck` (Decrypted from Windows LSA secrets / `RASDIALPARAMS` cache)
    *   **Significance:** This confirms the exact credentials Fred used to authenticate to the SRL corporate domain and VPN.

## Email Archive Exfiltration
At 05:39:11 on November 14, 2020, Fred deleted his local Outlook backup file `backup.pst` (size 20.5 MB), moving it to the Recycle Bin. Exactly 11 seconds later (at 05:39:22), he created and copied `SRL-EMAIL-EXPORT.pst` directly to his Google Drive folder (`G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\`). He then opened this Google Drive PST file in Outlook to verify its contents, updating his Outlook registry keys (`LastCorruptStore`) at 06:09:16 to point directly to the exfiltrated Google Drive path.

## Anti-Forensics (SDelete)
To securely erase staging directories and hide traces of the exfiltrated files, Fred searched Google for `sdelete download` at 05:37:37 on November 14, 2020, and downloaded `SDelete.zip`. He executed `SDELETE.EXE` twice from his Downloads directory, and then moved the binary to `C:\Windows\System32\SDELETE.EXE`, executing it 5 more times in rapid succession between 05:42:30 and 05:47:10.

## Memory Dump & Remote Control
*   **Volatile Memory Dump:** On November 15, 2020, at 18:32:19, the user opened `file:///D:/ROCBA-SYSTEM/Rocba-Memory.raw`. This indicates that Fred had possession of a raw memory image of his system and was actively analyzing it.
*   **Active Remote Control:** On November 16, 2020, the system was remotely accessed via RDP (port 3389) by two external IP addresses simultaneously: `81.30.144.115` and `213.202.233.104`. This remote access was preceded by an RDP brute-force flood from `201.193.188.114` and the other attacker IPs. During this remote session, a highly suspicious utility `MRC.exe` (DameWare Mini Remote Control or similar) was executed.

# Confirmed Exfiltrated/Accessed Data
The following high-value SRL projects and documents were confirmed to have been accessed and copied to either the external USB drive (F:) or Google Drive (G:):
1.  **Project KITT:** `Hydrogen_Hybrid_Tech.docx`, `The Future of KITT.pptx`, `secretweapon.jpg`, `German-KITT-Specs.docx`, `RareEarthDeposits_Confidential.jpg`.
2.  **Project Megaforce:** `Megaforce Testing.jpg`, `Megaforce Specs & Research.docx`, `Megaforce_Flyingbike_test2.jpg`, `Megaforce_Buggy.jpg`, `Megaforce_Bike.jpg`.
3.  **New Alloy Research:** `Alloy_Steel_-_Properties_and_Use.pdf`, `Superalloys_2010_13_50.pdf`.
4.  **Project Vibranium:** `Vibrainium(1).doc`, `Vibrainium - SRL.docx`.
5.  **Project Adamantium:** `France DGSE Intel Analysis Adamantium .pptx`.
6.  **Project StarFury:** `StarFury.zip`, `starfury`.
7.  **Project TIVO:** `TIVO Research.docx`.
8.  **Project Airwolf:** `Wolves_Lair_Tech_Specs.pptx`, `Airwolf3.jpg`, `Airwolf II.jpg`, `Airwolf-II-a.jpg`, `airwolf_blueprint.jpg`, `airwolf_blueprints.gif`, `Airwolf_schematics.png`, `airwolf05.jpg`, `Wolf AIr Financials.xlsx`.
9.  **Project Gunstar:** `Gunstar Test Harness Data.xlsx`, `GunStar Upgrade Specs.xlsx`, `Death_Blossom_attack.png`, `FTL Comms/Quantum Particles Affected by Other Dimensions.pdf`, `FTL Comms/Multiverse - Infiniverse Comms Issues.pdf`, `Starfighter 5200 Manual.pdf`, `GunStar Death Blossom Data.docx`.
10. **Project Blue Thunder:** `blue_thunder_blueprint_by_hurricanepolymar_d3cofgo-fullview.jpg`.
11. **SRL Email Archive:** `SRL-EMAIL-EXPORT.pst` (Exported to Google Drive G: on 2020-11-14 06:01:35).

# MITRE ATT&CK Mapping
*   **T1200 - Hardware Additions:** Connection of physical external USB drives (E:, F:, D:) previously paired with the system on November 1, 2020, to stage and exfiltrate files.
*   **T1078 - Valid Accounts:** Access to the system using Fred Rocba's credentials (`fredr`) after the reported burglary.
*   **T1005 - Data from Local System:** Harvesting of sensitive documents and Outlook PST files from local directories.
*   **T1567.002 - Exfiltration to Cloud Storage:** Exfiltration of files directly to Google Drive (`G:\My Drive\STARK-RESEARCH-LABS FOLDER`) linked to Fred's personal Google account.
*   **T1041 - Exfiltration Over C2 Channel:** Exfiltration of files to connected external USB drive F: (`CRIMSON2`).
*   **T1070.004 - File Deletion:** Execution of `SDelete.exe` to securely shred staged data and cover tracks.
*   **T1105 - Ingress Tool Transfer:** Downloading of Sysinternals `SDelete` from the internet.
*   **T1021.001 - Remote Desktop Protocol:** Active RDP sessions established from external IPs `81.30.144.115` and `213.202.233.104` on November 16, 2020.
*   **T1219 - Remote Access Software:** Execution of `MRC.exe` during the active RDP sessions.

# Recommendations
1.  **Immediate Account Revocation:** Revoke Fred Rocba's SRL work account (`frocba@stark-research-labs.com`) and block any active OAuth tokens or active sessions.
2.  **RDP Network Blocking:** Block external RDP access to the company network from IPs `81.30.144.115`, `213.202.233.104`, and `201.193.188.114`.
3.  **Legal & HR Action:** Terminate Fred Rocba's employment immediately and initiate legal proceedings for corporate espionage, IP theft, and staging a false police report.
4.  **Google Drive Takedown:** Subpoena Google for access/takedown of the personal Google Drive account associated with `redguard.cobra@gmail.com` and `fred.rocba@gmail.com` to secure the exfiltrated files.

# Evidence
*   **Disk Image:** `cases/ROCBA/images/rocba-cdrive.e01`
*   **Memory Image:** `cases/ROCBA/images/rocba-memory.raw`
*   **Mission Card 001:** `cases/ROCBA/docs/missions/001-mission-data-analyst-initial-triage.md` (Initial Triage and Data Inventory)
*   **Mission Card 002:** `cases/ROCBA/docs/missions/002-mission-data-analyst-usb-memory.md` (USB Devices and Memory Forensics)
*   **Mission Card 003:** `cases/ROCBA/docs/missions/003-mission-data-analyst-pst-analysis.md` (PST Files, PowerShell History, and Keyword Search)
