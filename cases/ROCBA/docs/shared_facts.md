# Data Inventory
- **Memory Image:** `cases/ROCBA/images/rocba-memory.raw` (or `cases/ROCBA/scratch/rocba-memory.raw`)
- **Disk Image:** `cases/ROCBA/images/rocba-cdrive.e01` (or `cases/ROCBA/scratch/rocba-cdrive.e01`)
- **Extracted Parquet Files:**
  - `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/fs_timeline.parquet`
  - `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/artifacts_timeline.parquet`
  - `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/browser_history.parquet`
  - `cases/ROCBA/scratch/rocba-cdrive.e01/parquet/browser_passwords.parquet`

# Compromised Accounts
- **Account:** `fredr` (Fred Rocba, RID 1002) - Last login: 2020-11-14 04:51:58-08:00 (Post-burglary activity). Personal emails: `redguard.cobra@gmail.com` (password: `C0bracommand`), `fred.rocba@gmail.com` (password: `C0bracommand`). Work email: `frocba@stark-research-labs.com` (domain account `SHIELDBASE\frocba`, password: `Big-Purple-Truck`). Personal Microsoft Account: `fred.rocba@outlook.com` (password: `C0bracommand`).
- **Account:** `srl-h` (RID 1001) - Last login: 2020-11-10 05:26:09-08:00.

# Known Malicious IPs & Domains
- **Domain:** `drive.google.com` (Accessed for data exfiltration on 2020-11-13/14).
- **Domain:** `starkresearchlabs-my.sharepoint.com` and `starkresearchlabs.sharepoint.com` (Target of data harvesting).
- **IP Address (Attacker/RDP):** `81.30.144.115` (Active RDP remote control sessions established on 2020-11-16 between 02:31 and 02:35).
- **IP Address (Attacker/RDP):** `213.202.233.104` (Active RDP remote control sessions established on 2020-11-16 between 02:31 and 02:35).
- **IP Address (RDP Brute-Force/Attempted):** `201.193.188.114` (RDP connection attempts on 2020-11-16).

# Suspicious Files & Staging Directories
- **Staging Directory (USB F:):** `F:\Files from SRL system`, `F:\Files of interest`, `F:\Key Data` (Staging/exfiltration directories on external USB drive).
  - **Physical Device:** Phison USB DISK 2.0, Serial: `90008B5EB5FFFF64` (VID: `13FE`, PID: `4300`). Volume Serial: `0xca659866`. First connected/migrated: `2020-11-01 17:12:24`.
- **Staging Directory (Google Drive G:):** `G:\My Drive\STARK-RESEARCH-LABS FOLDER` (Cloud exfiltration folder containing projects: Research, starfury, VC Files, Airwolf-SRL, SRL-Projects - Gunstar, Exported-PST).
- **Staging Directory (USB E:):** `E:\New Homework` (Accessed for staging/keys).
  - **Physical Device:** SMI IS917 innostor USB Device, Serial: `201207220009` (VID: `090C`, PID: `1000`). Volume Serial: `0x5e938bfb`. First connected/migrated: `2020-11-01 17:12:24`. Note: This volume was mounted as `D:` on `2020-09-16` and `2020-11-02`, and later mounted as `E:` on `2020-11-10`.
- **Staging Directory (USB D:):** `D:\secret key`, `D:\ROCBA-SYSTEM` (Accessed for staging/keys and containing memory dump `Rocba-Memory.raw`).
  - **Physical Device:** SMI Generic Mass Storage USB Device, Serial: `121118-1061200001494` (VID: `090C`, PID: `1000`). Volume Serial: `0xfc3ee602`. First connected/migrated: `2020-11-01 17:12:24`.
- **Other USB Device:** Lexar USB Flash Drive, Serial: `AAZ62W7KENRSJLHY`. First connected/migrated: `2020-11-01 17:12:24`.
- **Suspicious File:** `C:\Users\fredr\OneDrive\Documents\Outlook Files\backup.pst` (Local email backup, deleted and sent to Recycle Bin as `/$Recycle.Bin/S-1-5-21-528816539-567677750-276746561-1002/$RDNBREY.pst` on `2020-11-14 05:39:11`).
- **Suspicious File:** `C:\Users\fredr\OneDrive\Desktop\Research to Weaponize the Ion Thruster.docx` (Accessed on `2020-11-14 05:50:16` during the exfiltration window).
- **Suspicious File:** `C:\Users\fredr\Stark Research Labs\Maria Hill - KITT\secretweapon.jpg` (Accessed on `2020-11-13 19:51:11`).
- **Suspicious File:** `C:\Users\fredr\Stark Research Labs\SRL-Projects - Airwolf\weapons.jpg` (Accessed on `2020-11-13 20:21:22`).
- **Explorer Search History (WordWheelQuery):** Explorer search history for `fredr` on `2020-11-14 06:04:07` shows active searches for: `backup.pst`, `backup`, `*.pst`, `sdelete`, `bitlocker recovery key`, `bitlocker`, `cobra`, `crimson`, `airwolf`, `kitt`, `starfury`.
- **Browser History Activity:** Chrome browser history shows `fredr` logged into personal email `redguard.cobra@gmail.com` and visited `http://cobracommandcenter.com/` on `2020-11-07 19:23:30`.
- **Suspicious Tool:** `/Users/fredr/Downloads/SDelete.zip` and `SDelete.exe` (Sysinternals secure deletion tool, executed 7 times on 2020-11-14 between 05:42:30 and 05:47:10 for anti-forensics/evidence destruction).
- **Suspicious Tool:** `C:\Windows\System32\MRC.exe` (PID 29440) - Suspicious remote control or execution utility running on `2020-11-16 02:31:15` during active attacker RDP sessions.

# Decoded Payloads & Scripts
*To be determined.*

# Confirmed Exfiltrated/Accessed Data
- **Project KITT:** `Hydrogen_Hybrid_Tech.docx`, `The Future of KITT.pptx`, `secretweapon.jpg`, `German-KITT-Specs.docx`, `RareEarthDeposits_Confidential.jpg`.
- **Project Megaforce:** `Megaforce Testing.jpg`, `Megaforce Specs & Research.docx`, `Megaforce_Flyingbike_test2.jpg`, `Megaforce_Buggy.jpg`, `Megaforce_Bike.jpg`.
- **Project New Alloy Research:** `Alloy_Steel_-_Properties_and_Use.pdf`, `Superalloys_2010_13_50.pdf`.
- **Project Vibranium:** `Vibrainium(1).doc`, `Vibrainium - SRL.docx`.
- **Project Adamantium:** `France DGSE Intel Analysis Adamantium .pptx`.
- **Project StarFury:** `StarFury.zip`, `starfury`.
- **Project TIVO:** `TIVO Research.docx`.
- **Project Airwolf:** `Wolves_Lair_Tech_Specs.pptx`, `Airwolf3.jpg`, `Airwolf II.jpg`, `Airwolf-II-a.jpg`, `airwolf_blueprint.jpg`, `airwolf_blueprints.gif`, `Airwolf_schematics.png`, `airwolf05.jpg`, `Wolf AIr Financials.xlsx`.
- **Project Gunstar:** `Gunstar Test Harness Data.xlsx`, `GunStar Upgrade Specs.xlsx`, `Death_Blossom_attack.png`, `FTL Comms/Quantum Particles Affected by Other Dimensions.pdf`, `FTL Comms/Multiverse - Infiniverse Comms Issues.pdf`, `Starfighter 5200 Manual.pdf`, `GunStar Death Blossom Data.docx`.
- **Project Blue Thunder:** `blue_thunder_blueprint_by_hurricanepolymar_d3cofgo-fullview.jpg`.
- **SRL Email Export:** `SRL-EMAIL-EXPORT.pst` (Exported to Google Drive G: on 2020-11-14 06:01:35).

# Known Forensic Artifacts (IGNORE)
*None.*
