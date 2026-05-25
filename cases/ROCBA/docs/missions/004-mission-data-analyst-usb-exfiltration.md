# Mission: Hunt USB Activity and File Exfiltration
**Target Agent:** data-analyst

## Purpose
Identify the hardware details of the USB device(s) connected to Fred's system, establish their connection timelines, and trace all files staged and exfiltrated to USB, Google Drive, or other locations.

## Background
We know that the attacker staged files to Google Drive (`G:\`), an external USB drive (`E:\`), and other drives (`D:\`). We need to identify the exact USB device used (vendor, product, serial number), when it was connected/disconnected, and what files were copied to these destinations.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no USB or file exfiltration indicators are found, stop and report.

## Task Checklist
## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Execute the `hunt-usb-activity-sop` to identify the USB device(s) connected to Fred's system, mapping drive letter `E:` to its hardware serial number, vendor, and product details.
- [x] Determine the connection and disconnection timeline for the USB device.
- [x] Execute the `hunt-exfiltration-sop` to find file staging and copying activity to `G:\`, `E:\`, and `D:\`.
- [x] Identify if SDelete was used to delete files and what files were targeted for secure deletion.
- [x] Update `cases/ROCBA/docs/shared_facts.md` with any discovered USB hardware details, exfiltrated files, and deleted files.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  - Loaded `shared-facts-sop` and `delegating-mission-cards-sop` to establish strict context.
  - Used native `query_parquet.py` against `artifacts_timeline` and `fs_timeline` to identify USB storage device installations (Security-Auditing event 6416, Partition Driver event 1006, and setupapi.dev.log records).
  - Traced drive letter mappings and mapped drive `E:` to USB Serial `90008B5EA6FFFF27`.
  - Correlated LNK files, Shellbags, MRU lists, and filesystem timelines to reconstruct the timeline of exfiltration and staging across drives `G:\`, `E:\`, and `D:\`.
  - Audited prefetch and NTFS events to track Sysinternals SDelete (`sdelete.exe` / `sdelete64.exe`) execution and correlated it with accessed sensitive documents.
- **Findings:**
  - **USB Hardware Mapping:**
    - Drive `E:` was mapped to a **Phison Electronics Corp. USB DISK 2.0** device.
    - Hardware Serial Number: `90008B5EA6FFFF27`
    - Vendor ID (VID): `13FE`, Product ID (PID): `4300`, Revision: `PMAP`
    - Volume Serial Number: `0x5e938bfb` (Volume Label: `Homework`)
  - **USB Connection Timeline (90008B5EA6FFFF27):**
    - **Session 1:** Connected `2020-11-04 18:10:00` -> Mapped to `E:\` at `18:10:02` -> Disconnected `2020-11-05 15:14:52`
    - **Session 2:** Connected `2020-11-06 14:42:14` -> Mapped to `E:\` -> Disconnected `2020-11-06 14:51:11`
    - **Session 3:** Connected `2020-11-10 04:48:45` -> Mapped to `E:\` -> Disconnected `2020-11-10 04:49:52`
    - **Session 4:** Connected `2020-11-10 06:21:38` -> Mapped to `H:\` -> Disconnected `2020-11-10 06:23:33`
  - **File Staging and Copying Activity:**
    - **Drive G:\ (Google Drive, Volume Serial `0x19831116`):**
      - `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Airwolf-SRL\Wolf Air\Wolf AIr Financials.xlsx` (Accessed `2020-11-02 19:07:00`)
      - `G:\My Drive\Key\BitLocker Recovery Key 1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT` (Accessed `2020-11-10 06:22:54`)
      - `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst` (Accessed `2020-11-14 06:01:34`)
    - **Drive E:\ (USB, Volume Serial `0x5e938bfb` / `0xb80c61fd`):**
      - `E:\Brony.odp` (Accessed `2020-11-03 21:00:00`)
      - `E:\New Homework\Homework Grade 3.docx` (Accessed `2020-11-10 06:06:29`)
      - `E:\New Homework\BitLocker Recovery Key 1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT` (Accessed `2020-11-14 06:01:34`)
    - **Drive D:\ (Volume Serial `0xfc3ee602` / `0x2cb9f845` / `0x8ed8ea30`):**
      - `D:\USA HOCKEY Confirmation Page.pdf` (Accessed `2020-11-02 09:16:50`)
      - `D:\KIDS-HOMEWORK.pdf` (Accessed `2020-11-02 09:18:12`)
      - `D:\Minecraft.odp` (Accessed `2020-11-03 21:00:00`)
      - `D:\ secret key\BitLocker Recovery Key 1694D560-A615-4ABB-B721-E7C3E884F8BD.TXT` (Accessed `2020-11-10 04:53:24` and `2020-11-14 06:01:34`)
  - **SDelete Anti-Forensics Execution:**
    - Sysinternals SDelete was executed in two major windows:
      - **Baseline Window (2020-10-20):** `sdelete64.exe` executed on drive `D:` (`20:32:11`) and drive `C:` (`20:47:57`) to wipe pre-incident prep traces.
      - **Incident Window (2020-11-14):** `sdelete.exe` executed multiple times between `05:42:30` and `05:47:10` (Prefetch run count 5, System Restore point created with description `sdelete` at `05:48:07`).
      - **Targeted Files:** Attacker targeted critical files from local directories (including `C:\Users\fredr\Stark Research Labs\Maria Hill - KITT\The Future of KITT-older-version.pptx`, `F:\` drive resources, and the BitLocker recovery keys staged on local/external drives) to cover their tracks.
- **Confidence Rating:** 5/5 - Complete forensic artifact alignment across event logs, prefetch files, registry keys, and LNK/Shellbag timelines.
- **Budget Tally:**
  - Orientation Budget: 5 / 5 tool calls
  - Execution Budget: 20 / 20 tool calls
  - Reporting Budget: 4 / 5 tool calls
- **NPS / Feedback:** 10/10 - Extremely high speed and clean DuckDB query capabilities on Parquet files. Highly structured forensic workflow!
