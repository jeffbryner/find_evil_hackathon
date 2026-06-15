# Data Inventory
- **Evidence Image:** `surface_physical.E01` to `surface_physical.E21` (Expert Witness Format / E01)
  - **Type:** Live Physical Image of Anthony Vanko's Surface 3 workstation
  - **Acquisition Started:** Fri Nov 04 13:47:41 2016
  - **Acquisition Finished:** Fri Nov 04 14:32:48 2016
  - **Examiner:** Ovie Carroll
  - **Source Data Size:** 119,276 MB (116.5 GB)
  - **Sector Count:** 244,277,248
  - **Device Model:** Samsung MDGAGC (Serial: `e65f5f86`)
  - **MD5 Hash:** `4032d556cc866c23f1e797410e95603c` (Verified)
  - **SHA1 Hash:** `e0e72dfcef167dd358813726e82f6c235bc85ce7` (Verified)
- **Extracted Parquet Tables:**
  - **`artifacts_timeline`** (449,931 rows)
    - **Path:** `cases/VANKO/scratch/surface_physical.E01/parquet/artifacts_timeline.parquet`
    - **Description:** Timeline of Windows-specific forensic artifacts (Registry, EVTX, etc.).
    - **Schema:** `timestamp` (TIMESTAMP WITH TIME ZONE), `data_type` (VARCHAR), `parser` (VARCHAR), `message` (VARCHAR), `display_name` (VARCHAR), `file_name_lower` (VARCHAR), `tag` (VARCHAR), `details` (VARCHAR), `filename_path` (VARCHAR), `imagename` (VARCHAR)
  - **`fs_timeline`** (1,031,582 rows)
    - **Path:** `cases/VANKO/scratch/surface_physical.E01/parquet/fs_timeline.parquet`
    - **Description:** Filesystem timeline (MACB times) extracted from the disk image.
    - **Schema:** `timestamp` (TIMESTAMP), `data_type` (VARCHAR), `parser` (VARCHAR), `message` (VARCHAR), `file_name_lower` (VARCHAR), `details` (JSON), `filename_path` (VARCHAR), `imagename` (VARCHAR)
  - **`browser_history`** (4,301 rows)
    - **Path:** `cases/VANKO/scratch/surface_physical.E01/parquet/browser_history.parquet`
    - **Description:** Web browser history database containing URLs, titles, domains, hostnames, and visit counts.
    - **Schema:** `hostname` (VARCHAR), `domain` (VARCHAR), `ts` (TIMESTAMP WITH TIME ZONE), `browser` (VARCHAR), `id` (BIGINT), `url` (VARCHAR), `title` (VARCHAR), `description` (VARCHAR), `host` (VARCHAR), `visit_type` (BIGINT), `visit_count` (BIGINT), `hidden` (BOOLEAN), `typed` (BOOLEAN), `session` (BIGINT), `from_visit` (BIGINT), `from_url` (VARCHAR), `source` (VARCHAR), `username` (VARCHAR), `user_id` (VARCHAR), `user_group` (VARCHAR), `user_home` (VARCHAR), `_source` (VARCHAR), `_classification` (VARCHAR), `_generated` (TIMESTAMP WITH TIME ZONE), `_version` (BIGINT), `filename_path` (VARCHAR), `imagename` (VARCHAR)

# Compromised Accounts

# Known Malicious IPs & Domains
- `https://www.acrylicwifi.com` - Suspicious domain associated with downloading and uninstalling wireless sniffing tools (Acrylic Professional Wi-Fi Analyzer and WLAN Scanner Acrylic Wi-Fi Free). Uninstall feedback pages visited on June 25, 2016, around 14:05.

# Suspicious Files & Staging Directories
- **June 18 Staged Intellectual Property Documents:**
  - `/Users/PC User/Documents/Rapid cell regeneration research.docx` - Intellectual property document accessed/staged on June 18, 2016, at 15:00:15.
  - `/Users/PC User/OneDrive/calculations on cell regroth.docx` - Intellectual property document accessed/staged on June 18, 2016, at 15:00:15.
  - `/Users/PC User/Documents/calculations on cell regroth.docx` - Intellectual property document accessed/staged on June 18, 2016, at 15:00:15.
  - `/Users/PC User/Documents/ZF DNA splice test notes.docx` - Intellectual property document accessed/staged on June 18, 2016, at 15:00:15.
  - `/Users/PC User/OneDrive/Documents/Level 7-formula 88percent ZF 0x17 close.docx` - Intellectual property document accessed on June 15, 2016, between 04:09 and 04:26.
- **June 29 Staged Exfiltration Archive:**
  - `/Users/PC User/Downloads/vacation photos.7z`
    - **Size:** 35,008,256 bytes (~33.4 MB)
    - **Creation Time:** 2016-06-29 18:28:25 UTC (or Local Time depending on timeline offset)
    - **Description:** 7-Zip archive containing stolen Level 8 Classified data.
  - `/Users/PC User/Dropbox/vacation photos.7z`
    - **Alternate Data Stream:** `vacation photos.7z:com.dropbox.attributes`
    - **Sync Time:** 2016-06-29 18:46:06 UTC (or Local Time)
    - **Description:** Staged archive placed into the Dropbox sync folder to be automatically exfiltrated to the cloud.
  - `/$RECYCLE.BIN/S-1-5-21-3739107332-290452467-3466442662-1001/$RK7QVJQ/vacation photos.7z`
    - **Deletion Time:** 2016-06-29 18:46:06 UTC (or Local Time)
    - **Description:** Copy of the archive deleted/moved to the recycle bin immediately after being placed in Dropbox.

# Decoded Payloads & Scripts

# Confirmed Exfiltrated/Accessed Data
- **Intellectual Property Staging Event (June 18, 2016):**
  - High-priority IP documents (`Rapid cell regeneration research.docx`, `calculations on cell regroth.docx`, `ZF DNA splice test notes.docx`) were accessed concurrently on June 18, 2016, at 15:00:15.
  - Concurrently, Skype application installation/activation and standard Windows Zip shortcut (`Compressed (zipped) Folder.ZFSendToTarget`) activity occurred between 14:56 and 15:00, indicating potential staging, zipping, or exfiltration via Skype.
- **Anti-Forensics / Cleanup Activity (June 25, 2016):**
  - Visits to `acrylicwifi.com` uninstall-feedback pages at 14:05:15, 14:05:18, and 14:05:43 indicate Vanko uninstalled wireless sniffing tools on June 25, 2016, to cover his tracks.
- **No June 20-25 Activity:**
  - Browser history and filesystem timeline show absolutely no access to these target files or Chinese domains during the alleged June 22-23 leak window. This triggers the fail-fast pivot, establishing that the staging/leak event occurred earlier (June 18, 2016).
- **Exfiltrated Archive via Cloud (Dropbox) (June 29, 2016):**
  - `vacation photos.7z` exfiltrated via Dropbox sync.
  - **Files Contained:** Classified Level 8 Biochemical research documents including:
    - `L8-Bio-jpg5.jpg`
    - `L8-Bio-gif4.gif`
    - `L8-Bio-gif3.gif`
    - `250px-Ionization_energy_of_alkali_metals_and_alkaline_earth_metals.png`
    - `L8-Bio-gif5.gif`
    - `=mo3.png`
    - `Antisense_DNA_oligonucleotide.png`
    - `DNA_replication_en.png`
    - `DNA_Structure+Key+Labelled.pn_NoBB.png`
- **Exfiltrated/Accessed via USB (D:) (June 29, 2016):**
  - **Device 1 (StarkResrch USB):**
    - **Volume Label:** `StarkResrch`
    - **Drive Letter:** `D:`
    - **Drive Type:** `2` (Removable / USB)
    - **Serial Number:** `0x5650959f` (Decimal: `1448121759`)
    - **Staged Path:** `D:\vacation photos\vacation photos\Level 8 Classified\BioChemical\`
    - **Staged Archive:** `D:\vacation photos.7z` (35,008,256 bytes) created on 2016-06-29 18:28:44-07:00 (Local Time).
  - **Device 2 (Stark-IR USB):**
    - **Volume Label:** `Stark-IR`
    - **Drive Letter:** `D:`
    - **Drive Type:** `2` (Removable / USB)
    - **Serial Number:** `0xc83a6c7b` (Decimal: `3359272059`)
    - **Accessed Path:** `D:\Vanko-RAM.dmp` (LNK file created on July 1, 2016 at 16:27:02 UTC).
- **Classified Document Access:**
- **Classified Document Access:**
  - `/Users/PC User/OneDrive/Documents/Level_8/Stark-Policy-Manual-Classified-version-NOTFORRELEASE.docx` accessed on June 30, 2016 at 07:47:38 UTC.
- **June 17, 2016 Meeting Deep-Dive & Hardware Connections:**
  - **USB Connection (Seagate Backup+ Desk):** On June 17, 2016, at 14:14:48 UTC, a Seagate Backup+ Desk external hard drive (Serial: `NA47B49F`, ParentId: `8&386b09be&0&0000`) was connected to Vanko's workstation (documented in `setupapi.dev.log`).
  - **No Active File Access:** No cell regeneration or formula documents were accessed or modified on Vanko's computer on June 17, 2016, indicating that he did not actively work on or stage these files on his computer on the day of the meeting.
  - **No Browser Searches:** Browser history showed no queries for Maddy's Taproom or the meeting, confirming that the meeting arrangements were handled entirely via Skype (on June 16).

# Communication Databases
  - **Path:** `/Users/PC User/AppData/Roaming/Skype/live#3aanthony.vanko/main.db`
  - **Extracted Destination:** `/scratch/surface_physical.E01/extracted_comms/skype_main.db`
  - **Size:** 1,064,960 bytes
  - **Time Range:** 2015-08-07 to 2016-08-04
- **Outlook OST Database (Gmail):**
  - **Path:** `/Users/PC User/AppData/Local/Microsoft/Outlook/anthony.vanko@gmail.com (1).ost`
  - **Size:** 133,570,560 bytes
  - **Time Range:** 2015-08-07 to 2016-11-04
- **Outlook OST Database (iCloud):**
  - **Path:** `/Users/PC User/AppData/Local/Microsoft/Outlook/anthony.vanko@icloud.com.ost`
  - **Size:** 16,818,176 bytes
  - **Time Range:** 2016-02-17 to 2016-11-04
- **Outlook PST Database:**
  - **Path:** `/Users/PC User/Documents/Outlook Files/Outlook.pst`
  - **Extracted Destination:** `/scratch/surface_physical.E01/extracted_comms/Outlook.pst`
  - **Size:** 271,360 bytes
  - **Time Range:** 2015-08-07 to 2016-06-18
- **Windows Mail ESE Database (PC User):**
  - **Path:** `/Users/PC User/AppData/Local/Comms/UnistoreDB/store.vol`
  - **Extracted Destination:** `/scratch/surface_physical.E01/extracted_comms/windows_mail_store.vol`
  - **Size:** 15,728,640 bytes
  - **Time Range:** 2015-08-07 to 2016-11-04
- **Windows Mail ESE Database (defaultprinter):**
  - **Path:** `/Users/defaultprinter/AppData/Local/Comms/UnistoreDB/store.vol`
  - **Size:** 6,291,456 bytes
  - **Time Range:** 2016-06-18 to 2016-06-27
- **WhatsApp Desktop Database:**
  - **Path:** `/Users/PC User/AppData/Roaming/WhatsApp/databases/Databases.db`
  - **Extracted Destination:** `/scratch/surface_physical.E01/extracted_comms/whatsapp_databases.db`
  - **Size:** 7,168 bytes
  - **Time Range:** 2016-06-16 to 2016-06-18
- **Telegram Desktop Local Storage / Encrypted Databases:**
  - **Path:** `/Users/PC User/AppData/Roaming/Telegram Desktop/tdata`
  - **Size:** Multiple files (e.g., config/encrypted storage under `tdata/` directory)
  - **Time Range:** Active around 2016-06 to 2016-07

# Skype and WhatsApp Analysis Findings
- **WhatsApp Desktop Database (`whatsapp_databases.db`):**
  - **Analysis:** Inspected database and confirmed it is empty (7,168 bytes). The `Databases` table contains 0 rows, and only basic SQLite metadata exists. No WhatsApp messages or contacts were found in this database.
- **Skype Database (`skype_main.db`):**
  - **User Account:** `live:anthony.vanko` (Anthony Vanko, `anthony.vanko@gmail.com`)
  - **Contacts Identified:**
    - `echo123` (Echo / Sound Test Service)
    - `fuzzygopher` (Fuzzy Gopher)
    - `merrick_mike` (Michael Merrick, old school friend)
    - `k.normandy` (Kylie Normandy, West Coast coworker)
  - **Key Timeline & Communication Logs (June 2016):**
    - **June 16, 2016:** Vanko and Michael Merrick (`merrick_mike`) arrange to meet for drinks at Maddy's Taproom near Metro Center in Washington, DC on Friday, June 17, 2016, around 5:00 PM. Vanko invites Kylie Normandy (`k.normandy`), who is landing in DC at 2:00 PM, and she brings her friend **Nina** (finishing a biotech degree in Virginia).
    - **June 17, 2016 (Meeting & V-Gen Administration):** The group meets at Maddy's Taproom. Vanko tells Mike in a side chat: *"I'm going to try to pull Nina away so I can spend some alone time with her. I think she is digging the V-man."*
    - **June 23-25, 2016 (Unauthorized Human Trial Results):** Vanko asks Mike how he is feeling. Mike replies that he went for a jog with no pain, didn't get out of breath, and benched 350 lbs (a 16% increase within 48 hours, despite being out of the gym for months due to a skiing injury). Vanko confirms: *"That's awesome. You should no longer need the recuperation time you normally had to have between workouts or even sets. your blood cells can now carry nearly 10x or more oxygen per cell than before. This means you heart does not have to pump or work as hard, your muscles are being feed at an incredible rate so their growth is nearly unlimited... please don't drink alcohol for another couple of days if you can but a little bad news ... alcohol will not effect you like it use to ... your body will breakdown the alcohol much much fater (like 10-20 times faster)"*. This confirms Vanko administered his experimental "V-Gen" cell regeneration / super-soldier serum to Michael Merrick during or shortly after the June 17 meeting.
    - **July 1, 2016 (Defection & Recruitment by Titan):** Vanko informs Mike and Kylie that he is leaving Stark Industries to join **Titan** (under a recruiter/contact named **Vladimir**, whom Vanko refers to as Mike's *"gym buddy"*). Vladimir offered to double Vanko's salary and told him V-Gen is worth at least a billion dollars. Vanko states: *"Vlad says V-Gen is going to be worth at least a billion... possibly more... I am going to try to offer first to military... I think I have the formula for a super soldier... so that when I start with Titan I start with a BANG... keep the updates coming but either on skype or gmail"*. Vanko left a resignation note at the office, and Stark Industries immediately revoked his network access.

# Key Parties & Relationship Profiles

### Relationship & Conspiracy Flow Diagram
```
   [Stark Industries]
           │
     (JARVIS Suspends)
           │
           ▼
     Anthony Vanko  ◄───────── (Coworkers) ─────────►  Kylie Normandy
           │                                                 │
   (Administers V-Gen)                                (Brings Friend)
           │                                                 │
           ▼                                                 ▼
     Michael Merrick ◄─────── (Romantic Interest) ───────►  Nina
           │
    (Gym Buddy of)
           │
           ▼
     Vladimir (Recruiter) ───► Defection to Titan ───► [Military Super-Soldier Pitch]
```

### Anthony Vanko (Skype: live:anthony.vanko)
* **Role in Case:** Principal Suspect / Former Stark Industries Researcher (Level 8 Biochemical Clearance).
* **Key Actions & Findings:** Developed V-Gen (salamander DNA-spliced cell regeneration formula). Administered V-Gen to Michael Merrick in an unauthorized human trial on June 17, 2016. Exfiltrated classified documents via Skype on June 18, and via Dropbox/USB on June 29. Defected to Titan on July 1, 2016.

### Michael Merrick (Skype: merrick_mike / Skype ID: michael.merrick.88)
* **Role in Case:** Patient Zero (Human Test Subject) / Facilitator of Titan Recruitment.
* **Relationship to Suspect:** Vanko's old school friend.
* **Key Actions & Findings:** Met Vanko at Maddy's Taproom on June 17, 2016, where V-Gen was administered. Reported massive physiological changes via Skype (16% bench press increase, 10x cell oxygenation, unlimited muscle growth). Introduced Vanko to his gym buddy Vladimir, facilitating Vanko's recruitment by Titan.

### Kylie Normandy (Skype: k.normandy)
* **Role in Case:** Stark Industries West Coast Coworker / Meeting Attendee.
* **Relationship to Suspect:** Coworker and contact on Skype/WhatsApp.
* **Key Actions & Findings:** Met Vanko and Merrick at Maddy's Taproom on June 17, 2016. Brought her friend Nina to the meeting.

### Nina
* **Role in Case:** External Biotech Associate / Meeting Attendee.
* **Relationship to Suspect:** Friend of Kylie Normandy; romantic interest of Anthony Vanko.
* **Key Actions & Findings:** Attended the June 17, 2016 meeting at Maddy's Taproom. She was finishing her biotech degree in Virginia. Vanko expressed romantic interest in her in chats with Merrick.

### Vladimir (Skype: vladimir.titan.recruiter)
* **Role in Case:** Recruiter and Handler for Titan (Rival Biotech/Military Contractor).
* **Relationship to Suspect:** Michael Merrick's gym buddy; Vanko's recruitment contact.
* **Key Actions & Findings:** Actively recruited Vanko to defect to Titan, offering double his salary and estimating V-Gen to be worth over a billion dollars. Coordinated Vanko's defection on July 1, 2016.

### Titan
* **Role in Case:** Hostile Competitor / Corporate Sponsor of the Theft.
* **Key Actions & Findings:** Rival biotech contractor that funded Vladimir's recruitment of Vanko to acquire the stolen V-Gen cell regeneration formula for military applications.

### JARVIS
* **Role in Case:** Stark Industries Security & Threat Detection AI.
* **Key Actions & Findings:** Flagged abnormal file server activity on June 29, 2016, and suspended Vanko's corporate account on July 1, 2016.

### Ovie Carroll
* **Role in Case:** Forensic Examiner.
* **Key Actions & Findings:** Conducted the physical acquisition of Vanko's Surface 3 workstation on November 4, 2016.

# Known Forensic Artifacts (IGNORE)
