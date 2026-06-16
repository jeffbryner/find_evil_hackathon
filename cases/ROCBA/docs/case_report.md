> **🚨 CURRENT INVESTIGATIVE STATE:** Investigation completed successfully. All objectives achieved and case report fully updated.

# Case Report: ROCBA

## 1. Executive Summary
Stark Research Labs (SRL) employee Fred Rocba, a new engineering hire (hired Oct 24, 2020), was the victim of a residential break-in on November 13, 2020. During Fred's planned vacation to Disney (Nov 10 to Nov 15), an intruder targeted and accessed his corporate Microsoft Surface system.

This investigation confirmed that the attacker did not physically steal the Surface laptop itself, but rather used Fred's compromised corporate credentials (`SRL-FORGE\fredr`) to log in remotely via RDP from a Microsoft Azure host (`52.249.198.56`). The physical break-in at Fred's home was coordinated with the remote digital intrusion: a physical accomplice inside Fred's home connected and mounted an external BitLocker To Go USB drive named `CRIMSON2` (Drive `F:`, Volume Serial Number `0xca659866`) on the Surface, which was then unlocked remotely by the RDP attacker using `BDEUNLOCK.EXE`.

The attacker systematically exfiltrated highly sensitive data across multiple Stark Research Labs proprietary projects (KITT, Megaforce, Airwolf, Gunstar, Blue Thunder, Timothy Dungan, Wolves Lair, Vibranium, Adamantium, and Ion Thruster). The data was exfiltrated physically to the `CRIMSON2` USB drive and digitally by syncing folders to Google Drive via Google Drive File Stream (`G:`). Additionally, the attacker exported Fred's entire corporate Outlook email database to a PST archive (`SRL-EMAIL-EXPORT.pst`) and synced it to Google Drive. Finally, the attacker executed Sysinternals `SDelete` to securely wipe staging directories and cover their tracks.

**Critical Pre-Compromise Findings & Implications:**
Crucially, browser history analysis of Fred's personal Chrome profile (which was synced to the corporate Surface) revealed that Fred's account accessed the threat actor's domain `cobracommandcenter.com` and a threat actor-linked Gmail account `redguard.cobra@gmail.com` as early as September 17, 2020—weeks before Fred was hired at SRL. This direct connection between Fred's personal profile and the threat actor's infrastructure strongly indicates either:
1. **Insider Complicity / Staging:** Fred was an active participant or accomplice who established connections with the threat actor and facilitated access to SRL intellectual property.
2. **Early Personal Profile Compromise:** The threat actor had fully compromised Fred's personal Microsoft/Chrome credentials and browser session long before his employment, allowing them to automatically inherit access to his corporate Surface system when he synced his personal accounts.

Both scenarios represent a severe risk and underscore that the compromise began well before Fred's official start date.

## 2. Timeline of Events
The timeline is in UTC.

| Timestamp | MITRE Category | Event Details |
|---|---|---|
| 2020-09-17 20:27:23 | T1078 | Browser Access: Inbox accessed for threat actor Gmail account **`redguard.cobra@gmail.com`** (synced from Fred's personal Chrome profile). |
| 2020-10-14 04:17:01 | T1078 | Browser Access: Inbox accessed for threat actor Gmail account **`redguard.cobra@gmail.com`** (synced from Fred's personal Chrome profile). |
| 2020-10-24 00:00:00 | - | Interview and job accepted |
| 2020-10-24 00:00:00 | - | Fred is shipped a new Microsoft Surface system for home use |
| 2020-10-26 00:00:00 | - | Fred begins work at Stark Research Labs (SRL) |
| 2020-11-08 03:23:30 | T1204.001 | Browser Access: Fred browsed to threat actor domain **`cobracommandcenter.com`** on Chrome. |
| 2020-11-08 03:25:39 | T1078 | Browser Access: Inbox accessed for threat actor Gmail account **`redguard.cobra@gmail.com`** (exactly 2 minutes after visiting `cobracommandcenter.com`). |
| 2020-11-10 04:24:16 | T1078 | Browser Access: Inbox accessed for threat actor Gmail account **`redguard.cobra@gmail.com`**. |
| 2020-11-10 00:00:00 | - | Fred leaves on planned vacation to Disney |
| 2020-11-10 04:54:14 | T1087 | BitLocker Recovery Key (`1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT`) shortcut accessed; local session reconnection at 05:10:55. Fred prepares for vacation. |
| 2020-11-10 14:12:41 | T1567.002 | Google Drive File Stream (`G:`) is first mounted on the Surface system (Link created: `\DosDevices\G:`, Volume Serial Number `0x19831116`, Volume GUID `{f02b9866-6d78-348b-ad99-2a55aa54a850}`). |
| 2020-11-11 00:12:03 | - | Google Drive File Stream (`G:`) is unmounted. |
| 2020-11-11 00:12:10 | - | Local session reconnection occurred. |
| 2020-11-11 00:14:15 | T1567.002 | Google Drive File Stream (`G:`) is remounted. |
| 2020-11-11 08:14:15 | - | Google Drive File Stream (`G:`) is unmounted. |
| 2020-11-11 08:14:18 | T1567.002 | Google Drive File Stream (`G:`) is remounted. |
| 2020-11-13 19:42:50 | T1021.001 | Unauthorized remote RDP session established from IP `52.249.198.56` (Azure) using compromised domain credentials `SRL-FORGE\fredr` (matches residential burglary window). |
| 2020-11-13 19:43:00 | T1011 / T1110 | Physical connection of USB drive `CRIMSON2` (`F:`, Hardware Serial Number `AAZ62W7KENRSJLHY`, Lexar USB Flash Drive) inside Fred's home. Remote RDP attacker executes `BDEUNLOCK.EXE` to decrypt and mount the BitLocker To Go volume (Volume Serial Number `0xCA659866`). |
| 2020-11-13 19:45:00 | T1011 / T1567 | Intruder systematically accesses and copies sensitive project files (KITT, Megaforce, Timothy Dungan, Wolves Lair, Blue Thunder) to USB drive `CRIMSON2` (`F:`) and Google Drive File Stream (`G:`). |
| 2020-11-13 21:15:52 | - | Remote RDP session 1 disconnected. |
| 2020-11-14 04:31:27 | T1021.001 | Unauthorized remote RDP session 2 established from IP `52.249.198.56` (Azure) using compromised credentials `SRL-FORGE\fredr`. |
| 2020-11-14 04:35:00 | T1114 / T1567 | Intruder accesses and stages projects Airwolf, Gunstar, Vibranium, and Ion Thruster to Google Drive File Stream (`G:\My Drive\STARK-RESEARCH-LABS FOLDER`). |
| 2020-11-14 05:42:32 | T1070.004 | Intruder executes Sysinternals `sdelete.exe` to securely delete staging directories and cover tracks. |
| 2020-11-14 06:00:48 | T1114.002 | Intruder exports Fred's entire Outlook email database to a PST archive at `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst`, which synced to Google Drive. |
| 2020-11-14 06:17:13 | - | Remote RDP session disconnected. |
| 2020-11-15 18:29:37 | - | Local session reconnection (Fred returns from vacation and logs in locally). |

## 3. Findings & Analysis
- **Remote Desktop (RDP) Intrusion:** The attacker established unauthorized remote RDP sessions on Fred Rocba's Microsoft Surface laptop using his compromised domain credentials (`SRL-FORGE\fredr`). The sessions originated from the IP address **`52.249.198.56`** (Microsoft Azure hosting).
- **Physical-Digital Burglary Coordination:** The first RDP session occurred on **Nov 13, 2020 (19:42:50 to 21:15:52)**, precisely matching the timeframe of the residential break-in at Fred's home. During this session, the attacker executed **`BDEUNLOCK.EXE`** to mount and decrypt an external BitLocker To Go USB drive named **`CRIMSON2`** (Drive `F:`, Volume Serial Number `0xCA659866`). This proves a physical accomplice entered Fred's home, plugged the USB drive into the Surface, and the remote RDP attacker then unlocked and copied files onto it.
- **USB Drive Characteristics:**
  - **CRIMSON2 (`F:`)**: Removable Drive (Type 2), Volume Serial Number `0xCA659866` (decimal `3395655782`), Hardware Serial Number `AAZ62W7KENRSJLHY` (Lexar USB Flash Drive, USBSTOR: `Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_1100\AAZ62W7KENRSJLHY&0`). Staging folders included `F:\Files from SRL system`, `F:\Files of interest`, and `F:\Key Data`.
  - **Other Connected Removable Volumes**:
    - `FILES` (D:): Volume Serial Number `0x8ED6FE30` (decimal `2396580400`)
    - `ArbcoCircus` (D:): Volume Serial Number `0x469B7A49` (decimal `1184228937`)
    - `Homework` (D: / E:): Volume Serial Number `0x5E937BFB` (decimal `1586727931`)
    - E: (No label): Volume Serial Number `0xB80E41FD` (decimal `3087819261`)
    - D: (No label): Volume Serial Number `0x2CBE0045` (decimal `750385221`)
    - `SRL IRT` (D:): Fixed Drive (Type 3), Volume Serial Number `0xFC3E9002` (decimal `4231980546`)
- **Cloud Exfiltration via Google Drive File Stream:**
  - **Volume Label:** `Google Drive File Stream`
  - **Drive Letter:** `G:`
  - **Drive Type:** Fixed (Type 3 - Virtual Drive)
  - **Volume Serial Number:** `0x19831116` (decimal `428019990`)
  - **Volume GUID:** `{f02b9866-6d78-348b-ad99-2a55aa54a850}`
  - **First Mount:** Nov 10, 2020, 14:12:41 UTC (`06:12:41-08:00` local).
  - **Active Mount/Unmount Sync Timeline (Nov 11, 2020):**
    - Unmounted (Link deleted): Nov 11, 2020, 00:12:03-08:00
    - Remounted (Link created): Nov 11, 2020, 00:14:15-08:00
    - Unmounted (Link deleted): Nov 11, 2020, 08:14:15-08:00
    - Remounted (Link created): Nov 11, 2020, 08:14:18-08:00
  - **Staging Directory:** `G:\My Drive\STARK-RESEARCH-LABS FOLDER`
  - **Associated Google Accounts:** Analysis of Google Drive File Stream's local databases (`account_db_sqlite.db` and metadata databases under `%LOCALAPPDATA%\Google\DriveFS\`) revealed **two** configured accounts:
    1.  **Personal Account (Active/Syncing):** `fred.rocba@gmail.com` (Google User ID: `106274999640256541802`, Root Folder ID: `0AHTIa2KKlB3YUk9PVA`).
    2.  **Threat Actor Account (Suspicious/Configured):** `crimsonguard@cobracommandcenter.com` (Google User ID: `106045340982100456262`, Root Folder ID: `0AI6qhB1Y0KXJUk9PVA`, associated with "Blue Horizon Cybersecurity"). This provides a critical attribution link, confirming that the attacker configured their own Google Drive account under Fred's compromised Windows profile to exfiltrate Stark Research Labs files.
- **Mailbox Exfiltration:** On **Nov 14, 2020, at 06:00:48**, the attacker used Outlook to export Fred's entire corporate mailbox to a PST archive at **`G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst`**, exfiltrating all corporate correspondence and contacts.
- **Anti-Forensics / Cleanup:** On **Nov 14, 2020, at 05:42:32**, the attacker downloaded and executed Sysinternals **`SDelete`** (`sdelete.exe`) to securely wipe local staging directories and cover their tracks.
- **Pre-Compromise Threat Actor Connections & Browsing History:** Chrome browser history analysis on Fred Rocba's profile revealed highly suspicious activity linking him to the threat actor's domain and email account prior to the November 13, 2020 RDP break-in:
  - **Malicious Domain Visits:** On **November 7, 2020, at 19:23:30 Local (03:23:30 UTC)**, Fred's Chrome browser was used to visit the threat actor's domain **`cobracommandcenter.com`** and `www.cobracommandcenter.com`.
  - **Threat Actor Gmail Account Access:** On **September 17, October 13, November 7 (at 19:25:39 Local, exactly 2 minutes after visiting `cobracommandcenter.com`), and November 9, 2020**, Fred's Chrome browser was used to access the inbox of a threat actor-linked Gmail account: **`redguard.cobra@gmail.com`**.
  - **Implications:** Since the Surface laptop was set up with Fred's personal Microsoft and Chrome account sync, the browser history from September and October (prior to his hiring on Oct 24) synced from his personal profile. This proves a direct connection between Fred's personal browsing/account profile and the threat actor's email address and domain weeks before his employment at SRL, indicating either an early credential/profile compromise or insider complicity.

## 4. Confirmed Exfiltrated/Accessed Data
- **Project KITT:** `The Future of KITT.pptx`, `German-KITT-Specs.docx`, `Hydrogen_Hybrid_Tech.docx`, `secretweapon.jpg`, `RareEarthDeposits_Confidential.jpg`
- **Project Megaforce:** `Megaforce Specs & Research.docx`, `Megaforce_Buggy.jpg`, `Megaforce_Flyingbike_test2.jpg`, `Megaforce_Bike.jpg`
- **Project Airwolf:** `Airwolf3.jpg`, `Airwolf II.jpg`, `Wolf AIr Financials.xlsx`
- **Project Gunstar:** `GunStar Death Blossom Data.docx`, `Gunstar Test Harness Data.xlsx`, `GunStar Upgrade Specs.xlsx`, `Death_Blossom_attack.png`, `Quantum Particles Affected by Other Dimensions.pdf`, `Multiverse - Infiniverse Comms Issues.pdf`, `Starfighter 5200 Manual.pdf`
- **Project Blue Thunder:** `blue_thunder_blueprint_by_hurricanepolymar_d3cofgo-fullview.jpg`
- **Project Timothy Dungan - New Alloy Research:** `Alloy_Steel_-_Properties_and_Use.pdf`, `Superalloys_2010_13_50.pdf`
- **Project Wolves Lair:** `Wolves_Lair_Tech_Specs.pptx`
- **Project StarFury:** `StarFury.zip`
- **Project TIVO Research:** `TIVO Research.docx`
- **Project Ion Thruster:** `Research to Weaponize the Ion Thruster.docx`
- **Project Vibranium:** `Vibrainium - SRL.docx`, `Vibrainium(1).doc`
- **Project Adamantium:** `ADAMANTIUM-Background.docx`, `France DGSE Intel Analysis Adamantium .pptx`
- **Fred's Corporate Mailbox:** Complete mailbox export `SRL-EMAIL-EXPORT.pst` containing all corporate correspondence.

## 5. MITRE ATT&CK Mapping
- **Initial Access:** Valid Accounts (T1078) - Compromised domain credentials `SRL-FORGE\fredr` used.
- **Lateral Movement:** Remote Services: Remote Desktop Protocol (T1021.001) - Remote RDP sessions from Azure IP `52.249.198.56`.
- **Collection:** Email Collection: Local Email Archives (T1114.002) - Exported mailbox to PST archive.
- **Collection:** Data from Local System (T1119) / Data from Network Shared Drive (T1039) - Accessing local, OneDrive, and SharePoint files.
- **Exfiltration:** Exfiltration Over Physical Medium (T1011) - Copying files to BitLocker To Go USB drive `CRIMSON2`.
- **Exfiltration:** Exfiltration Over Web Service: Exfiltration to Cloud Storage (T1567.002) - Syncing to Google Drive File Stream.
- **Defense Evasion:** Indicator Removal on Host: File Deletion (T1070.004) - Running `sdelete.exe` to securely wipe files.

## 6. Recommendations
1. **Immediate Credential Revocation:** Reset Fred Rocba's domain password (`SRL-FORGE\fredr`) and revoke all active active directory and cloud sessions.
2. **Enforce Multi-Factor Authentication (MFA):** Mandate MFA for all RDP, VPN, and cloud application logins across the organization.
3. **Restrict RDP Access:** Limit RDP access to systems. Restrict RDP to secure corporate VPN connections with MFA, and block RDP from public cloud provider IP ranges (such as Azure).
4. **Endpoint Protection & Monitoring:** Deploy Endpoint Detection and Response (EDR) agents to monitor and block unauthorized archiving, cloud sync, or secure deletion tools (like SDelete).
5. **USB Control Policies:** Implement strict USB device control policies to prevent mounting unauthorized external USB drives.
6. **Security Awareness Training:** Train remote employees on physical security best practices, securing corporate laptops, and reporting residential break-ins or suspicious activities immediately.

## 7. Evidence
- **Disk Image:** `rocba-cdrive.e01` (Microsoft Surface C-Drive), ingested and parsed into:
  - `fs_timeline.parquet` (2,345,972 rows)
  - `artifacts_timeline.parquet` (409,130 rows)
  - `browser_history.parquet` (2,651 rows)
- **Memory Image:** `rocba-memory.raw` (extracted RAM), ingested and parsed into:
  - `memory_pslist.parquet` (2,186 rows)
  - `memory_netscan.parquet` (430 rows)
  - `memory_timeliner.parquet` (36,012 rows)
- **Mission Cards:**
  - `001-mission-data-analyst-data-inventory.md` (Initial Data Inventory)
  - `002-mission-data-analyst-activity-analysis.md` (Activity Analysis)
  - `003-mission-data-analyst-usb-gdrive-timeline.md` (USB & Google Drive Deep-Dive)
  - `004-mission-data-analyst-google-account-identification.md` (Google Account Identification)
  - `005-mission-data-analyst-cobracommandcenter-browser-link.md` (Cobra Command Center Browser Link)
