# Data Inventory
- **Memory Image:** `cases/ROCBA/images/rocba-memory.raw` (extracted to `cases/ROCBA/scratch/rocba-memory.raw`)
  - **Table: `memory_pslist`**
    - Row Count: 2,186
    - Temporal Range: `2020-11-11 08:12:57` to `2020-11-16 02:32:35`
  - **Table: `memory_netscan`**
    - Row Count: 430
    - Temporal Range: `2020-11-11 08:13:14` to `2020-11-16 02:36:42`
  - **Table: `memory_timeliner`**
    - Row Count: 36,012
    - Absolute Temporal Range: `1600-12-01 10:52:23` to `7225-06-23 17:00:14`
    - Filtered 2020 Range: 32,368 rows between `2020-09-27 14:37:51` and `2020-11-16 02:36:42`
- **Disk Image:** `cases/ROCBA/images/rocba-cdrive.e01` (extracted to `cases/ROCBA/scratch/rocba-cdrive.e01`)
  - **Table: `fs_timeline`**
    - Row Count: 2,345,972
    - Absolute Temporal Range: `1970-01-01 16:00:00` to `2020-11-15 19:05:45`
    - Filtered 2020 Range: 1,987,075 rows between `2020-01-02 17:05:48` and `2020-11-15 19:05:45`
  - **Table: `artifacts_timeline`**
    - Row Count: 409,130
    - Absolute Temporal Range: `1969-12-31 16:00:00` to `2020-11-15 19:05:14.205449`
    - Filtered 2020 Range: 201,180 rows between `2020-06-23 15:32:06` and `2020-11-15 19:05:14.205449`
  - **Table: `browser_history`**
    - Row Count: 2,651
    - Temporal Range: `2020-06-24 17:58:22.923000` to `2020-11-15 18:32:19.619198`
- **USB Drive CRIMSON2 (F:):** Removable Drive (Type 2), Volume Serial Number `0xCA659866` (decimal `3395655782`), Hardware Serial Number `AAZ62W7KENRSJLHY` (Lexar USB Flash Drive, USBSTOR: `Disk&Ven_Lexar&Prod_USB_Flash_Drive&Rev_1100\AAZ62W7KENRSJLHY&0`). Used to stage and exfiltrate files from SRL.
- **Google Drive File Stream (G:):** Virtual Fixed Drive (Type 3), Volume Serial Number `0x19831116` (decimal `428019990`), Volume GUID `{f02b9866-6d78-348b-ad99-2a55aa54a850}`. Mounted on Nov 10, 2020 at 06:12:41-08:00 local.
- **Other Connected Removable Volumes:**
  - `FILES` (D:): Volume Serial Number `0x8ED6FE30` (decimal `2396580400`)
  - `ArbcoCircus` (D:): Volume Serial Number `0x469B7A49` (decimal `1184228937`)
  - `Homework` (D: / E:): Volume Serial Number `0x5E937BFB` (decimal `1586727931`)
  - E: (No label): Volume Serial Number `0xB80E41FD` (decimal `3087819261`)
  - D: (No label): Volume Serial Number `0x2CBE0045` (decimal `750385221`)
  - `SRL IRT` (D:): Fixed Drive (Type 3), Volume Serial Number `0xFC3E9002` (decimal `4231980546`)

# Compromised Accounts
- **`SRL-FORGE\fredr`** (Fred Rocba's domain account): Compromised and used for unauthorized remote RDP access during his vacation.
- **`fred.rocba@gmail.com`** (Fred Rocba's personal Google Account, Google User ID: `106274999640256541802`): Configured in Google Drive File Stream (`G:`), with state=1 (active/active sync). Root folder ID: `0AHTIa2KKlB3YUk9PVA`.
- **`crimsonguard@cobracommandcenter.com`** (Threat Actor-controlled Google Account, Google User ID: `106045340982100456262`): Configured in Google Drive File Stream (`G:`) under Fred's profile, with state=2. Root folder ID: `0AI6qhB1Y0KXJUk9PVA`. Associated with organization "Blue Horizon Cybersecurity". This account was likely used for the exfiltration of Stark Research Labs (SRL) data.
- **`redguard.cobra@gmail.com`** (Suspicious Google Account): Accessed on Fred Rocba's Chrome browser multiple times prior to the Nov 13, 2020 compromise: on 2020-09-17, 2020-10-13, 2020-11-07, and 2020-11-09.

# Known Malicious IPs & Domains
- **`52.249.198.56`**: Remote IP address (Microsoft Azure hosting) used to establish unauthorized RDP sessions on Nov 13 and Nov 14, 2020.
- **`cobracommandcenter.com`**: Malicious domain associated with the threat actor Google account `crimsonguard@cobracommandcenter.com` used for data exfiltration. Visited by Fred Rocba (`fredr`) using Chrome on 2020-11-07 19:23:30 (prior to the Nov 13, 2020 RDP break-in).

# Suspicious Files & Staging Directories
- **`F:\Files from SRL system`**: Staging folder on external USB drive `CRIMSON2` (`F:`).
- **`F:\Files of interest`**: Staging folder on external USB drive `CRIMSON2` (`F:`).
- **`F:\Key Data`**: Staging folder on external USB drive `CRIMSON2` (`F:`).
- **`G:\My Drive\STARK-RESEARCH-LABS FOLDER`**: Staging and cloud exfiltration directory on Google Drive File Stream (`G:`).
- **`G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst`**: Exported Outlook email archive file synced to Google Drive.
- **`C:\Users\fredr\Downloads\SDelete.zip`** & **`C:\Users\fredr\Downloads\SDelete\sdelete.exe`**: Sysinternals SDelete utility downloaded and run on Nov 14, 2020 to securely delete files and cover tracks.

# Decoded Payloads & Scripts
*None identified in this phase.*

# Confirmed Exfiltrated/Accessed Data
- **Project KITT**:
  - `The Future of KITT.pptx` (stolen to USB `F:` and accessed)
  - `German-KITT-Specs.docx` (accessed, copied to USB `F:\Files from SRL system\Maria Hill - WorkingFiles`)
  - `Hydrogen_Hybrid_Tech.docx` (accessed)
  - `secretweapon.jpg` (accessed)
  - `RareEarthDeposits_Confidential.jpg` (accessed, copied to USB `F:\Files from SRL system\Maria Hill - WorkingFiles`)
- **Project Megaforce**:
  - `Megaforce Specs & Research.docx` (copied to USB `F:\Files of interest\SRL-Projects - Megaforce\Megaforce`)
  - `Megaforce_Buggy.jpg` (copied to USB `F:\Files of interest\SRL-Projects - Megaforce\Megaforce`)
  - `Megaforce_Flyingbike_test2.jpg` (copied to USB `F:\Files of interest\SRL-Projects - Megaforce\Megaforce`)
  - `Megaforce_Bike.jpg` (accessed)
- **Project Airwolf**:
  - `Airwolf3.jpg` (accessed)
  - `Airwolf II.jpg` (accessed)
  - `Wolf AIr Financials.xlsx` (accessed on Google Drive `G:`)
- **Project Gunstar**:
  - `GunStar Death Blossom Data.docx` (accessed on Google Drive `G:`)
  - `Gunstar Test Harness Data.xlsx` (accessed)
  - `GunStar Upgrade Specs.xlsx` (accessed)
  - `Death_Blossom_attack.png` (accessed)
  - `Quantum Particles Affected by Other Dimensions.pdf` (accessed)
  - `Multiverse - Infiniverse Comms Issues.pdf` (accessed)
  - `Starfighter 5200 Manual.pdf` (accessed)
- **Project Blue Thunder**:
  - `blue_thunder_blueprint_by_hurricanepolymar_d3cofgo-fullview.jpg` (copied to USB `F:\Key Data`)
- **Project Timothy Dungan - New Alloy Research**:
  - `Alloy_Steel_-_Properties_and_Use.pdf` (accessed)
  - `Superalloys_2010_13_50.pdf` (accessed, copied to USB `F:\Files from SRL system\Timothy Dungan - New Alloy Research`)
- **Project Wolves Lair**:
  - `Wolves_Lair_Tech_Specs.pptx` (copied to USB `F:\Files of interest\Recovered Documents`)
- **Project StarFury**:
  - `StarFury.zip` (accessed)
- **Project TIVO Research**:
  - `TIVO Research.docx` (accessed)
- **Project Ion Thruster**:
  - `Research to Weaponize the Ion Thruster.docx` (accessed on Google Drive `G:`)
- **Project Vibranium**:
  - `Vibrainium - SRL.docx` (accessed)
  - `Vibrainium(1).doc` (accessed, copied to Google Drive `G:`)
- **Project Adamantium**:
  - `ADAMANTIUM-Background.docx` (accessed)
  - `France DGSE Intel Analysis Adamantium .pptx` (accessed)
- **Fred's Outlook Email**:
  - **`SRL-EMAIL-EXPORT.pst`** (Fred's complete email archive exported and exfiltrated to Google Drive on Nov 14, 2020, 06:00:48)

# Pending Investigative Leads
*To be populated.*

# Known Forensic Artifacts (IGNORE)
*To be populated.*
