# Data Inventory
- Disk Image: `cases/ROCBA/images/rocba-cdrive.e01` (Extracted Parquet files under `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/`, Hostname: `SRL-FORGE`)
- Memory Image: `cases/ROCBA/images/rocba-memory.raw` (Extracted Parquet files under `cases/ROCBA/scratch/rocba-memory.raw/parquet/`, Hostname: `SRL-FORGE`)

# Compromised Accounts
- Fred Rocba (Local account: `fredr` on SRL-FORGE) - Compromised on `2020-11-13` and `2020-11-14` via RDP/Network logons from Azure IP `52.249.198.56`
- `fred.rocba@outlook.com` (Microsoft Account / Local Account) - Compromised on `2020-11-13` and `2020-11-14` via RDP/Network logons from Azure IP `52.249.198.56`. Decrypted Password: `C0bracommand` (found in Firefox logins).
- `redguard.cobra@gmail.com` (Gmail / Personal Account) - Decrypted Password: `C0bracommand` (found in Firefox logins).
- `frocba_stark-research-labs_com` / `SHIELDBASE\frocba` (Stark Research Labs SharePoint/Office365 and Active Directory Account) - Decrypted Password: `Big-Purple-Truck` (found in LSA Secrets / RAS Dial Params).
- `srl-helpdesk@outlook.com` (Microsoft Account / Local Account) - Compromised on `2020-11-10` via RDP logon from IP `174.196.200.9` (associated local username: `srl-h`)
- `crimsonguard@cobracommandcenter.com` (Attacker-controlled Google Drive account used on Fred's workstation for exfiltration)
- `fred.rocba@gmail.com` (Gmail / Personal Account) - Decrypted Password: `C0bracommand` / `c0bracommand` (found in Firefox logins).
- `3392233317` (Facebook Account ID) - Decrypted Password: `C0bracommand` (found in Firefox logins).
- **DPAPI Decryption Analysis Note:** Attempted DPAPI decryption on Fred's master key (`035a9e0d-fb66-4b38-b9cc-70c5571f66b3`) using prekeys generated from password `C0bracommand` and NT hash `3a6cb699b06c274208dc36a0f908a674`. Decryption failed because the account is a Windows Microsoft Account (MSA), meaning DPAPI keys are cloud-linked and cannot be decrypted with standard offline password prekeys. Chrome/Edge databases (which depend on DPAPI) are thus secured, but the attacker's main credentials had already been recovered from Firefox (which does not use DPAPI).

# Known Malicious IPs & Domains
- `213.202.233.104` (External IP, established RDP connection to SRL-FORGE on port 3389)
- `81.30.144.115` (External IP, established RDP connection to SRL-FORGE on port 3389)
- `81.19.209.101` (External IP, incoming RDP connection attempt, SYN_RCVD)
- `201.193.188.114` (External IP, closed RDP connection to SRL-FORGE)
- `85.14.242.76` (External IP, conducted massive NTLM brute-force attack with 30+ usernames between 2020-11-13 and 2020-11-14)
- `174.196.200.9` (External IP, used for successful RDP logon as compromised `srl-helpdesk@outlook.com` on `2020-11-10 05:26:11`)
- `52.249.198.56` (External IP, Microsoft Azure VPS, used for successful RDP logons as compromised `fred.rocba@outlook.com` and network logons as `fredr` on `2020-11-13` and `2020-11-14`)

# Suspicious Files & Staging Directories
- `G:\My Drive\STARK-RESEARCH-LABS FOLDER\` (Google Drive folder used for exfiltration)
- `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\` (Staging folder for email archives)
- `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Airwolf-ARL\` (Staging folder for Project Airwolf files)
- `G:\My Drive\Key\` (Staging folder for BitLocker recovery keys)
- `D:\ROCBA-SYSTEM\` (Staging folder for memory/system files)
- `D:\secret key\` (Staging folder for BitLocker recovery keys)
- `E:\New Homework\` (Staging folder on external USB drive E:)
- `C:\Users\fredr\Downloads\SDelete.zip` (Sysinternals SDelete tool downloaded to cover tracks)
- `C:\Users\fredr\Downloads\SDelete\sdelete.exe` (Sysinternals SDelete tool executed multiple times on `2020-11-14` between `05:42:30` and `05:47:10` to securely delete evidence)
- Drive E: mapped to USB Serial `90008B5EA6FFFF27` (Phison Electronics Corp. USB DISK 2.0, Volume Serial `0x5e938bfb`, Label: `Homework`)
- Connection/Disconnection Timeline for USB `90008B5EA6FFFF27`:
  - 2020-11-04 18:10:00 to 2020-11-05 15:14:52 (Mapped to E:)
  - 2020-11-06 14:42:14 to 2020-11-06 14:51:11 (Mapped to E:)
  - 2020-11-10 04:48:45 to 2020-11-10 04:49:52 (Mapped to E:)
  - 2020-11-10 06:21:38 to 2020-11-10 06:23:33 (Mapped to H:)
- Drive F: mapped to Lexar USB Flash Drive, Serial `AAZ62W7KENRSJLHY` (Volume Serial `0xca659866`, Label: `CRIMSON2`)
  - Connected via **RemoteFX USB Device Redirection** during Fred Rocba's RDP session on `2020-11-13` starting at `19:42:52` (2 seconds after RDP login from IP `52.249.198.56`).
  - Redirection session recorded in event logs: `Microsoft-Windows-TerminalServices-PnPDevices/Admin` (Event ID 36) and `Microsoft-Windows-TerminalServices-ServerUSBDevices/Admin` (Event ID 36) at `19:42:52`.
  - Disconnected or experienced network/redirection drop starting at `19:45:19` (evidenced by numerous StorDiag Event ID 507 errors with code `0xc0000185` STATUS_DEVICE_DATA_ERROR / unplugged).
- `C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe` (Referenced in highly suspicious HKCU Run key persistence with arguments `--type=service /prefetch:8`)

# Decoded Payloads & Scripts
- Run key persistence: `C18E42C7363A0E298C5594A2ABE53A0760B71220._service_run` under `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run` executing `"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=service /prefetch:8` (Created on `2020-11-10 06:12:41.621546-08:00`)
- Suspicious Executed Tools:
  - `MRC.EXE` (DameWare Mini Remote Control) - Executed on `2020-11-10 14:00:54` and `2020-11-14 11:33:04` (Prefetch)
  - `sdelete.exe` (Sysinternals SDelete) - Executed on `2020-11-14 11:34:00` (Prefetch)
  - `powershell.exe` - Executed multiple times (e.g. `2020-11-10`, `2020-11-11`, `2020-11-12`, `2020-11-13`, `2020-11-14`), with most runs containing health check ping commands (`Write-Host 'Final result: 1'`)

# Confirmed Exfiltrated/Accessed Data
- `SRL-EMAIL-EXPORT.pst` (Fred's Outlook email archive containing work emails, exfiltrated to Google Drive)
  - Size: 20,587,520 bytes
  - Google DriveFS stable_id: `1370` (Mapped via `metadata_sqlite_db` of profile `106045340982100456262`)
  - Staged Location: `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst`
  - Recoverability Status: **Fully Recoverable**. While the staged copy on Google Drive and the Google DriveFS cache file `1369`/`1370` were deleted/wiped by Sysinternals SDelete (executed on `2020-11-14` between `05:42:30` and `05:47:10`), the local copy of the PST file was deleted (sent to the Recycle Bin) *after* SDelete ran, at `2020-11-14 06:07:32` local time. It exists as an active, allocated file inside Fred's Recycle Bin folder at `/$Recycle.Bin/S-1-5-21-528816539-567677750-276746561-1002/$RDNBREY.pst` (MFT Record `479180`), with its corresponding index file `$IDNBREY.pst` (MFT Record `107736`). Since the Recycle Bin was never emptied and SDelete was run prior to deletion, the file is 100% intact and recoverable.
  - Alternative PST/OST Locations & Copies:
    - **Recycle Bin:** An active, allocated copy of the PST file exists as `/$Recycle.Bin/S-1-5-21-528816539-567677750-276746561-1002/$RDNBREY.pst` (MFT Record `479180`) with size exactly `20,587,520` bytes, along with its index file `$IDNBREY.pst` (MFT Record `107736`) created on `2020-11-14 06:07:32` local time.
    - **Outlook Default Directories:** No active or historical `.pst` or `.ost` files found in standard locations (e.g., `C:\Users\fredr\AppData\Local\Microsoft\Outlook\` or `C:\Users\fredr\Documents\Outlook Files\`).
    - **Connected Drives:** No `.pst` or `.ost` files found on external drives D:, E:, or F:.
    - **Recent Shortcuts:** Shortcut `SRL-EMAIL-EXPORT.lnk` located at `/users/fredr/appdata/roaming/microsoft/windows/recent/srl-email-export.lnk` pointing to `G:\My Drive`, confirming access to the exfiltrated staging path.
    - **Legacy PST File:** An old, unrelated PST file `/Users/fredr/iCloudDrive/EXFIL.pst` was found (timestamped `2012-04-05 09:16:38-07:00`).
    - **Extracted & Recovered PST Contents:**
      - File: `SRL-EMAIL-EXPORT-RECOVERED.pst`
      - Size: 20,587,520 bytes (MD5: `d7ffc69c21847a8557a39fe27d1d9426`)
      - Folders and Email Counts:
        - `Inbox`: 42 emails
        - `Inbox/Maria`: 23 emails
        - **Total Emails:** 65
      - Key Senders & Recipients:
        - Fred Rocba (`frocba@stark-research-labs.com`)
        - Maria Hill (`mhill@stark-research-labs.com`)
        - Timothy Dungan (`tdungan@stark-research-labs.com`)
        - Natasha Romanoff (`nromanoff@stark-research-labs.com`)
        - Nick Fury (`nfury@stark-research-labs.com`)
        - Ulysses Key (`u.key@spadertech.com`)
      - Key Projects & Topics Discussed:
        - **Project ADAMANTIUM:** Multiple comments/mentions on the document "ADAMANTIUM-Background" involving Timothy Dungan, Maria Hill, Natasha Romanoff, and Fred Rocba (emails 33, 34, 35, 36, 37, 38, 39, 40).
        - **Project KITT:** Maria Hill shared the "KITT" folder and "The Future of KITT" document (emails 15, 18).
        - **Project Megaforce:** Maria Hill shared the "Megaforce" folder and SharePoint Online sent reminders (emails 20, 43).
        - **Project Gunstar:** Discussions on "Gunstar Development Next Steps" and "Gunstar Project" (emails 11, 31).
        - **New Alloy Research:** Folder shared by Timothy Dungan (email 23).
        - **Vibrainium:** Natasha Romanoff shared an anonymous access link to "Vibrainium(1).doc" (email 15).
      - Key Attachments Found:
        - `some-quantum-mechanical-properties-of-the-wolfram-model.pdf` (from Maria Hill, Sat, 7 Nov 2020)
        - `Mongolia_ScoutingTrip.jfif` (from Maria Hill, Sat, 31 Oct 2020)
        - `ponies.jpg` (from Maria Hill, Sun, 1 Nov 2020)
        - `eagle_hunting.jpg` (from Maria Hill, Wed, 4 Nov 2020)
        - `GuessWhere.jpg` (from Maria Hill, Thu, 5 Nov 2020)
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
- `F:\Files of interest\Recovered Documents\Wolves_Lair_Tech_Specs.pptx` (Exfiltrated to redirected Lexar USB drive on `2020-11-13 20:24:10`)
- `F:\Files from SRL system\Quantum Particles Affected by Other Dimensions.pdf` (Exfiltrated to redirected Lexar USB drive on `2020-11-13 20:49:36`)
- `F:\Files from SRL system\The Future of KITT.pptx` (Exfiltrated to redirected Lexar USB drive on `2020-11-13 20:24:11`)

# Known Forensic Artifacts (IGNORE)
- None identified yet
