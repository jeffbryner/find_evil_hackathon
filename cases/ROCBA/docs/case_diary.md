> **🚨 CURRENT INVESTIGATIVE STATE:** Investigation completed. All missions successfully executed and analyzed.

# Case Diary: Case ROCBA

## 1. Executive Summary
Fred Rocba, initially thought to be a victim of a home break-in and IP theft on November 13, 2020, has been forensically exposed as an **undercover Cobra Crimson Guard agent** (a "Fred" clone, with "Rocba" being an anagram of "Cobra"). The physical break-in was a staged event to cover up a massive insider espionage operation. This investigation recovered plaintext browser passwords (`C0bracommand`) and Windows LSA secrets (`Big-Purple-Truck` for VPN access to `SHIELDBASE\frocba`). The workstation was used to systematically stage and exfiltrate SRL's most sensitive intellectual property (projects ADAMANTIUM, KITT, Megaforce, GunStar, and FTL Communications) to Google Drive (configured with the account `crimsonguard@cobracommandcenter.com`) and an RDP-redirected drive belonging to the attacker. While the attacker used Sysinternals SDelete to securely erase local staging folders, they made a critical error by deleting the local copy of the PST file *after* running SDelete, leaving it fully intact and recoverable inside the Recycle Bin as `$RDNBREY.pst`.

## 2. Timeline of Events
| Timestamp | MITRE ATT&CK Category | Event Details |
| --- | --- | --- |
| 2020-10-24 | N/A | Fred accepts job and is shipped a Microsoft Surface system. |
| 2020-10-26 | N/A | Fred begins work at SRL. |
| 2020-11-10 04:00 | Initial Access | Unauthorized user logs in, initiates password resets for Fred's personal Outlook account, and installs Google Drive Backup and Sync. |
| 2020-11-10 04:48 | Physical USB Connection | Fred's USB drive (Phison Electronics, Serial: `90008B5EA6FFFF27`, Volume: `Homework`) is connected (Session 3) to map drive E:. |
| 2020-11-10 04:53 | Collection | BitLocker Recovery Key `1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT` is accessed from `D:\ secret key\`. |
| 2020-11-10 05:26 | Initial Access | **Attacker RDP Session:** Successful RDP logon using compromised **`srl-helpdesk@outlook.com`** account from IP `174.196.200.9` (local username: `srl-h`). |
| 2020-11-10 06:12 | Persistence | **Edge Masquerading Run Key:** Run key persistence created under name `C18E42C7363A0E298C5594A2ABE53A0760B71220._service_run` running `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=service /prefetch:8`. |
| 2020-11-10 06:21 | Physical USB Connection | Fred's USB drive connected again (Session 4) to map drive H:. |
| 2020-11-10 06:22 | Collection | BitLocker Recovery Key is copied to Google Drive staging folder `G:\My Drive\Key\`. |
| 2020-11-10 14:00 | Command and Control | DameWare Mini Remote Control (`MRC.EXE`) executed, establishing remote control. |
| 2020-11-10 | N/A | Fred leaves on vacation to Disney. |
| 2020-11-13 | N/A | Fred's home is broken into; SRL system targeted. |
| 2020-11-13 14:09 | Collection / Exfiltration | Attacker accesses SRL SharePoint/OneDrive, downloads sensitive Project Megaforce and Airwolf documents, and accesses Maria Hill's quantum physics paper. |
| 2020-11-13 15:12 | Credential Access | Massive external network brute-force attack from `85.14.242.76` targeting 30+ usernames starts (unsuccessful). |
| 2020-11-13 19:42 | Initial Access | **Attacker RDP Session:** Successful console unlock/RDP session using compromised **`fred.rocba@outlook.com`** account from Azure IP `52.249.198.56` (local username: `fredr`). |
| 2020-11-14 04:31 | Initial Access | Successful RDP logon using `fred.rocba@outlook.com` from Azure IP `52.249.198.56`. |
| 2020-11-14 04:52 | Initial Access | Successful RDP logon using `fred.rocba@outlook.com` from Azure IP `52.249.198.56`. |
| 2020-11-14 05:42 | Defense Evasion | Attacker executes Sysinternals SDelete multiple times to securely erase evidence, including `The Future of KITT-older-version.pptx` and `Quantum Particles Affected by Other Dimensions.pdf`. |
| 2020-11-14 06:01 | Collection / Exfiltration | Attacker exfiltrates Fred's Outlook email archive (`SRL-EMAIL-EXPORT.pst`) and BitLocker recovery keys to Google Drive and an RDP-redirected drive (`\\tsclient\F`). |
| 2020-11-14 11:33 | Command and Control | DameWare Mini Remote Control (`MRC.EXE`) executed again. |
| 2020-11-14 11:34 | Defense Evasion | SDelete executed again to securely delete files and cover tracks. |
| 2020-11-15 | Collection / Exfiltration | Attacker stages a raw memory dump of Fred's system to D:\ROCBA-SYSTEM\Rocba-Memory.raw. |

## 3. Findings & Analysis
- **Forensic Data Inventory:**
  - Hostname: `SRL-FORGE`
  - Disk Image `rocba-cdrive.e01` covers filesystem activity up to `2020-11-15 19:05:45`.
  - Memory Image `rocba-memory.raw` covers active processes/connections from `2020-11-11` to `2020-11-16`.
  - Browser history goes up to `2020-11-15 18:32:19`.
  - Extracted tables include `memory_pslist`, `memory_netscan`, `memory_timeliner`, `artifacts_timeline`, `fs_timeline`, and `browser_history`.
- **Initial Browser & Network Investigation (Mission 002):**
  - **Key Projects Accessed:** Fred had access to Project ADAMANTIUM, Project KITT, Project Megaforce, Project GunStar, and Project Firedam.
  - **RDP Compromise:** The system was remotely accessed via RDP (port 3389) from several external IPs: `213.202.233.104`, `81.30.144.115`, `81.19.209.101`, and `201.193.188.114`.
  - **Vacation Activity:** Extensive unauthorized activity occurred while Fred was on vacation, starting on 2020-11-10 and continuing through 2020-11-15.
  - **Exfiltration Staging:** The attacker installed Google Drive Backup and Sync to stage files for exfiltration. Staging folders were also identified on drives D:, E: (USB), and G: (Google Drive).
- **Process Execution & Persistence Analysis (Mission 003):**
  - **DameWare Mini Remote Control:** `MRC.EXE` executed on `2020-11-10 14:00:54` and `2020-11-14 11:33:04`, indicating active remote control sessions.
  - **SDelete Execution:** `sdelete.exe` executed on `2020-11-14` to securely erase critical documents and BitLocker recovery keys to prevent recovery.
  - **Run Key Persistence:** Highly suspicious HKCU Run key persistence created under the name `C18E42C7363A0E298C5594A2ABE53A0760B71220._service_run` running `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=service /prefetch:8`.
  - **Failed Brute-Force:** Massive NTLM brute-force attack from `85.14.242.76` between `2020-11-13` and `2020-11-14` targeting 30+ usernames (all unsuccessful).
- **USB & File Exfiltration Analysis (Missions 004 & 006):**
  - **USB Mapping:** Drive letter `E:` mapped to USB Serial `90008B5EA6FFFF27` (Phison Electronics Corp. USB DISK 2.0, Volume Serial `0x5e938bfb`, Label: `Homework`).
  - **USB Timeline:** USB connected multiple times prior to Fred's vacation, with the last connection on `2020-11-10 06:21:38` (Session 4, mapped to H:). No physical USB storage devices were connected during the compromise window of November 13-14, 2020.
  - **RDP Drive Redirection:** During the RDP session on `2020-11-14 06:01:34`, drive `F:` was mapped as an RDP-redirected network drive (`\\tsclient\F`) from the attacker's client machine.
  - **File Staging & Exfiltration:** Files were staged across Google Drive (`G:\`) and local folders (`D:\ secret key\`). Staged files (such as `SRL-EMAIL-EXPORT.pst`) were then copied and exfiltrated directly to the attacker's machine via the RDP-redirected drive `F:` (`\\tsclient\F`).
  - **Anti-Forensics:** Sysinternals SDelete used to securely delete staged files and documents of interest, such as `The Future of KITT-older-version.pptx` and `Quantum Particles Affected by Other Dimensions.pdf`.
- **Logon Event Analysis (Mission 005):**
  - **Session 1 (Helpdesk Account):** RDP logon (`LogonType 10`) at `2020-11-10 05:26:11` using `srl-helpdesk@outlook.com` (local username: `srl-h`) from IP `174.196.200.9` (likely a cellular/residential proxy). This session created the persistence Run key.
  - **Session 2 (Fred's Account):** Console Unlock (`LogonType 7`) and RDP logons on `2020-11-13 19:42:52`, `2020-11-14 04:31:26`, and `2020-11-14 04:52:03` using `fred.rocba@outlook.com` (local username: `fredr`) from Azure IP `52.249.198.56`. This session performed the exfiltration and ran SDelete.
- **Google Drive & Attacker Account Correlation (Mission 012):**
  - **Accounts Identified:** 
    - **Google Drive Sync Account:** **`crimsonguard@cobracommandcenter.com`** (configured in Google DriveFS).
    - **Browser Session Account:** **`redguard.cobra@gmail.com`** (logged in via Chrome).
  - **Timeline of Access:** On November 10, 2020, during the initial compromise window:
    - At **04:24:16 UTC**, the attacker logged into **`redguard.cobra@gmail.com`** using Chrome under Fred's local profile `fredr`.
    - Later that day, between **14:08 and 14:10 UTC**, the attacker downloaded and configured the Google Drive File Stream client using **`crimsonguard@cobracommandcenter.com`**.
  - **Threat Actor Theme (Cobra Command):** Both accounts follow a highly specific naming convention themed around G.I. Joe's **Cobra Command** and its elite infantry units (the **Crimson Guard** and **Red Guards**). This confirms that both the web session and the exfiltration client were operated by the same threat actor.
  - **Fred's Actual Personal Email:** In contrast, Fred Rocba's actual personal Gmail account is **`fred.rocba@gmail.com`**, as evidenced by a Pinterest autologin notification received on November 12, 2020, at 02:54:57 UTC.
  - **Discovery Method:** Extracted directly from Fred's local Google DriveFS SQLite metadata database (`metadata_sqlite_db`) located at `cases/ROCBA/scratch/metadata_sqlite_db` and browser history records in `cases/ROCBA/scratch/browser_history_vacation.jsonl`, confirming the specific Google accounts used for web sessions and staging/exfiltrating corporate intellectual property.
- **Decrypted Credentials & Insider Threat Revelation (Mission 013):**
  - **Decrypted Browser Passwords:** Plaintext passwords were extracted from Fred's local Firefox credential databases (`logins.json`):
    - `fred.rocba@outlook.com` -> Password: **`C0bracommand`**
    - `redguard.cobra@gmail.com` -> Password: **`C0bracommand`**
    - `fred.rocba@gmail.com` -> Password: **`C0bracommand`**
    - `fred.rocba@gmail.com` (Amazon) -> Password: **`c0bracommand`**
    - `fred.rocba@gmail.com` (Netflix) -> Password: **`C0bracommand`**
    - `3392233317` (Facebook) -> Password: **`C0bracommand`**
  - **Decrypted Windows LSA Secrets:** Recovered the Active Directory domain credentials used to connect to the Stark Research Labs network via VPN:
    - Domain Username: `SHIELDBASE\frocba` (UPN: `frocba_stark-research-labs_com`)
    - VPN Password: **`Big-Purple-Truck`**
  - **The "Fred" Crimson Guard Revelation:** 
    - **Name Anagram:** "Fred Rocba" is an exact anagram of **"Fred Cobra"**.
    - **Cobra Lore Connection:** In G.I. Joe lore, the **Crimson Guard** undercover agents are clones who lead normal civilian lives (such as engineers) and are all named **"Fred"** (e.g., Fred I, Fred II, Fred VII).
    - **Password Reuse:** Fred used the password **`C0bracommand`** (Cobra Command) across all his personal accounts.
    - **Attacker Accounts:** The Google Drive exfiltration account **`crimsonguard@cobracommandcenter.com`** and the Chrome web session account **`redguard.cobra@gmail.com`** are both named after Cobra elite units (Crimson Guard, Red Guard) and share the exact same password **`C0bracommand`** used by Fred.
    - **Conclusion:** Fred Rocba is not a victim. He is an undercover Cobra agent who utilized his position at SRL to steal sensitive intellectual property and staged the home break-in to cover up his voluntary exfiltration of data.
- **DPAPI Decryption & Browser Password Recovery (Mission 015):**
  - **Custom Prekey Generation:** Generated a custom DPAPI prekey using Fred Rocba's SID (`S-1-5-21-528816539-567677750-276746561-1002`) and his password `C0bracommand`.
  - **Master Key Decryption Failure:** Attempted to decrypt Fred's DPAPI master key (`035a9e0d-fb66-4b38-b9cc-70c5571f66b3`) with the custom prekey and alternative prekeys (including those derived from his NT hash `3a6cb699b06c274208dc36a0f908a674` and LSA DPAPI_SYSTEM secrets). All decryption attempts failed.
  - **Microsoft Account (MSA) Limitation:** Confirmed via `pypykatz` structural analysis that the master key (Version 2, SHA512, AES256) belongs to a Windows Microsoft Account (MSA). MSA DPAPI master keys are cryptographically linked to Microsoft's cloud authentication keys, making standard offline decryption using only local password/NT hash prekeys impossible.
  - **Credential Status:** Chrome and Edge databases (which rely on DPAPI) remain secure from offline decryption. However, all of Fred's critical credentials (such as `C0bracommand` and `Big-Purple-Truck`) had already been successfully extracted from Firefox's `logins.json` and Windows LSA secrets in prior missions.

## 4. Confirmed Exfiltrated/Accessed Data
- `SRL-EMAIL-EXPORT.pst` (Fred's Outlook email archive containing work emails, exfiltrated to Google Drive; **Fully Recoverable** inside the Recycle Bin as `$RDNBREY.pst` [MFT record `479180` / index file `$IDNBREY.pst` record `107736` deleted on `2020-11-14 06:07:32` local time]; because deletion occurred *after* SDelete was executed and the Recycle Bin was never emptied, the file remains completely intact and allocated. **PST Contents Extracted & Analyzed:** Contains 65 emails total [42 in `Inbox`, 23 in `Inbox/Maria`]. Key topics include Project ADAMANTIUM discussions [Timothy Dungan, Natasha Romanoff, Maria Hill], Project KITT folder sharing, Project Megaforce folder sharing, Project Gunstar development next steps, New Alloy Research, and Vibranium access. Key attachments recovered: `some-quantum-mechanical-properties-of-the-wolfram-model.pdf` [quantum research], `Mongolia_ScoutingTrip.jfif`, `ponies.jpg`, `eagle_hunting.jpg`, and `GuessWhere.jpg`)
- `Quantum Particles Affected by Other Dimensions.pdf` (Sensitive quantum physics paper by Maria Hill, accessed on SharePoint and exfiltrated)
- `Megaforce Specs & Research.docx` (Sensitive Project Megaforce document, accessed on SharePoint)
- `Megaforce_Bike.jpg` (Project Megaforce image, downloaded from SharePoint)
- `Airwolf3.jpg`, `Airwolf II.jpg` (Project Airwolf images, accessed and copied to Google Drive)
- `BitLocker Recovery Keys` (Multiple BitLocker recovery keys accessed and copied to Google Drive/USB, e.g. `BitLocker Recovery Key 1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT`)
- `ADAMANTIUM-Background.docx` (Project ADAMANTIUM document, accessed)
- `The Future of KITT.pptx` (Project KITT presentation, accessed)
- `GunStar Upgrade Specs.xlsx` (Project GunStar document, accessed)
- `E:\Brony.odp` (Accessed on `2020-11-03 21:00:00`)
- `E:\New Homework\Homework Grade 3.docx` (Accessed on `2020-11-10 06:06:29`)
- `D:\ secret key\BitLocker Recovery Key 1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT` (Accessed on `2020-11-10 04:53:24`)
- `D:\USA HOCKEY Confirmation Page.pdf` (Accessed on `2020-11-02 09:16:50`)
- `D:\KIDS-HOMEWORK.pdf` (Accessed on `2020-11-02 09:18:12`)
- `D:\Minecraft.odp` (Accessed on `2020-11-03 21:00:00`)
- `F:\ Files of interest\Recovered Documents\Wolves_Lair_Tech_Specs.pptx` (Accessed via MRU on `2020-11-14 06:01:34`)
- `F:\ Files from SRL system\Quantum Particles Affected by Other Dimensions.pdf` (Accessed via MRU on `2020-11-14 06:01:34`)
- `F:\ Files from SRL system\The Future of KITT.pptx` (Accessed via MRU on `2020-11-14 06:01:34`)

## 5. MITRE ATT&CK Mapping
| Tactic | Technique | Details |
| --- | --- | --- |
| **Initial Access** | Valid Accounts (T1078) | Compromised `srl-helpdesk@outlook.com` and `fred.rocba@outlook.com` credentials. |
| **Initial Access** | External Remote Services (T1133) | Remote interactive RDP sessions on port 3389. |
| **Persistence** | Boot or Logon Autostart Execution (T1547.001) | Registry run key persistence created under HKCU Run masquerading as Microsoft Edge. |
| **Execution** | Command and Scripting Interpreter (T1059) | Executed PowerShell commands. |
| **Execution** | User Execution (T1204) | DameWare Mini Remote Control (`MRC.EXE`) execution. |
| **Defense Evasion** | Indicator Removal on Host: File Deletion (T1070.004) | Executed Sysinternals SDelete to securely erase staging folders and stolen documents. |
| **Defense Evasion** | Masquerading (T1036) | Run key named after SHA-1 hash executing `msedge.exe` with custom service flags. |
| **Credential Access** | Brute Force (T1110) | NTLM brute-force from `85.14.242.76` targeting 30+ usernames (unsuccessful). |
| **Collection** | Archive Collected Data (T1114) | Staged Fred's Outlook email archive (`SRL-EMAIL-EXPORT.pst`). |
| **Collection** | Data Staged (T1074) | Staged files in `G:\My Drive\`, `E:\New Homework\`, and `D:\ secret key\`. |
| **Exfiltration** | Exfiltration Over Web Service (T1567) | Synced staged files to Google Drive using Backup and Sync. |
| **Exfiltration** | Exfiltration Over RDP Client Drive Redirection (T1048) | Copied files directly to the attacker's client machine via RDP-redirected drive `F:` (`\\tsclient\F`). |

## 6. Recommendations
1. **Revoke and Reset Credentials:** Immediately revoke and reset credentials for `srl-helpdesk@outlook.com`, `fred.rocba@outlook.com`, and all targeted local accounts.
2. **Enforce Multi-Factor Authentication (MFA):** Enforce MFA on all RDP, Office 365, SharePoint, and corporate network logons.
3. **Restrict RDP Access:** Disable external RDP (port 3389) access directly from the internet. Require a secure corporate VPN with MFA for remote administration.
4. **Implement Application Whitelisting:** Block unauthorized execution of administrative and remote control tools (like DameWare `MRC.EXE`) and secure deletion tools (like `sdelete.exe`) on end-user workstations.
5. **Monitor and Block Cloud Sync Applications:** Monitor and restrict the installation of personal cloud synchronization clients (like Google Drive Backup and Sync) on corporate endpoints.
6. **Rotate BitLocker Recovery Keys:** Rotate the compromised BitLocker recovery keys for all affected drives.

## 7. Evidence
- **Disk Image:** `cases/ROCBA/images/rocba-cdrive.e01` (Extracted Parquet files in `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/`)
- **Memory Image:** `cases/ROCBA/images/rocba-memory.raw` (Extracted Parquet files in `cases/ROCBA/scratch/rocba-memory.raw/parquet/`)
- **Mission Cards:**
  - Mission 001 (Inventory): `cases/ROCBA/docs/missions/001-mission-data-analyst-inventory.md`
  - Mission 002 (Browser & Network): `cases/ROCBA/docs/missions/002-mission-data-analyst-network-browser.md`
  - Mission 003 (Process & Persistence): `cases/ROCBA/docs/missions/003-mission-data-analyst-execution-persistence.md`
  - Mission 004 (USB & Exfiltration): `cases/ROCBA/docs/missions/004-mission-data-analyst-usb-exfiltration.md`
  - Mission 005 (Logons): `cases/ROCBA/docs/missions/005-mission-data-analyst-logons.md`
  - Mission 006 (USB Exfiltration Verification): `cases/ROCBA/docs/missions/006-mission-data-analyst-usb-exfiltration-verification.md`
  - Mission 007 (PST Recovery): `cases/ROCBA/docs/missions/007-mission-sniper-forensics-recover-pst.md`
  - Mission 008 (PST Alternative Locations): `cases/ROCBA/docs/missions/008-mission-data-analyst-pst-alternative-locations.md`
  - Mission 009 (Recycle Bin PST Search): `cases/ROCBA/docs/missions/009-mission-data-analyst-recycle-bin-pst-search.md`
  - Mission 010 (Extract and Analyze PST Contents): `cases/ROCBA/docs/missions/010-mission-sniper-forensics-extract-pst-contents.md`
  - Mission 011 (Run Email Body Extraction Script): `cases/ROCBA/docs/missions/011-mission-data-analyst-run-email-body-extraction.md`
  - Mission 012 (Identify Google Drive Gmail Accounts): `cases/ROCBA/docs/missions/012-mission-data-analyst-google-drive-account.md`
  - Mission 013 (Retrieve and Analyze Browser Passwords): `cases/ROCBA/docs/missions/013-mission-data-analyst-browser-passwords.md`
  - Mission 014 (DPAPI Decryption and SAM/Chrome Credential Recovery): `cases/ROCBA/docs/missions/014-mission-data-analyst-dpapi-decryption.md`
  - Mission 015 (DPAPI Decryption and Browser Password Recovery Execution): `cases/ROCBA/docs/missions/015-mission-sniper-forensics-dpapi-execution.md`

