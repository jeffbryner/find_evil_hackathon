# Mission: June 30 Staging and USB Activity Investigation
**Target Agent:** data-analyst

## Purpose
Investigate Vanko's workstation activity on and around June 30, 2016, to determine if he copied large volumes of data from the StarkResearch server, how that data was staged/archived, and whether it was exfiltrated via USB, cloud sync, or other network channels.

## Background
On June 30, 2016, the JARVIS network monitoring system detected Vanko's account copying large amounts of classified data from `\\StarkResearch\Level [5-8] Classified\` to his workstation. JARVIS suspended his account. We need to find where this data went on his Surface 3 laptop, if it was packaged (e.g., zipped), and if any USB devices or external drives were connected during or after this activity.

## Budget & Rules of Engagement
- **Orientation Budget:** 3 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 3 tool calls
- **Proactive Self-Termination:** At tool call 17 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If no file staging or USB activity is found in the first 5 queries, report and pivot.

## Task Checklist
- [x] Execute the `hunt-exfiltration-sop` and `hunt-usb-activity-sop` skills.
- [x] Query `fs_timeline` for files created, modified, or accessed on June 30, 2016 (UTC) containing "Classified", "StarkResearch", or located in temporary/staging folders.
- [x] Search for any ZIP, RAR, 7Z, or other archive files created on June 30, 2016.
- [x] Map any external drive letters (e.g., D:, E:, F:) accessed on June 30, 2016, and find their corresponding hardware serial numbers using ShellBags, USBSTOR, or SetupAPI.
- [x] Query `browser_history` and `artifacts_timeline` (SRUM, Prefetch) around June 30, 2016, for web uploads, cloud sync logins, or large network transfers.
- [x] Update the `# Suspicious Files & Staging Directories`, `# Confirmed Exfiltrated/Accessed Data`, and other relevant sections in `cases/VANKO/docs/shared_facts.md` with findings.
- [x] Update this mission card with results under the "Results & Post-Mortem" section.
- [x] Write a chronological technical log of 100% of executed queries and commands to `cases/VANKO/docs/missions/002-mission-data-analyst-june30-staging-and-usb-audit.md` (verifying that the count matches the final Budget Tally).

## Results & Post-Mortem
- **Approach:** 
  1. Tested schema and connectivity using a simple limit query on `fs_timeline`.
  2. Searched filesystem timeline for "Classified" and "StarkResearch" indicators.
  3. Performed targeted queries for archive files (zip, 7z, rar, cab, tar) created/accessed around June 30, 2016.
  4. Searched LNK files to find references to external drives (D:, E:, F:, G:), mapping drive letter D: to volume labels `StarkResrch` and `Stark-IR`.
  5. Extracted the hardware serial numbers from LNK files and ShellBags metadata.
  6. Tracked down a staged 7-Zip archive named `vacation photos.7z` (~33.4 MB) containing Level 8 Biochemical documents.
  7. Traced the movement of this archive into the local Dropbox folder, noting the creation of a Dropbox Alternate Data Stream (`:com.dropbox.attributes`) and its immediate deletion/move to the Recycle Bin.
  8. Investigated browser history for cloud sync indicators, showing extensive OneDrive browser use but no Dropbox browser use, confirming Dropbox was run as a local sync client.

- **Findings:**
  1. **Staged Data / Archive:**
     - **File:** `/Users/PC User/Downloads/vacation photos.7z`
     - **Size:** 35,008,256 bytes (~33.4 MB)
     - **Staging Time:** 2016-06-29 18:28:25 UTC (or Local Time depending on timeline offset).
     - **Contents:** Classified Level 8 Biochemical documents (e.g., `L8-Bio-jpg5.jpg`, `L8-Bio-gif4.gif`, `Antisense_DNA_oligonucleotide.png`, etc.) disguised as vacation photos.
  2. **Exfiltration via Dropbox (Cloud Sync):**
     - The staged archive was copied/moved to `/Users/PC User/Dropbox/vacation photos.7z` on June 29 at 18:46:06 UTC.
     - An Alternate Data Stream `:com.dropbox.attributes` was created on the file, indicating it was successfully synced by the local Dropbox desktop client.
     - Immediately after copying to Dropbox, the file was moved to the Recycle Bin (`/$RECYCLE.BIN/S-1-5-21-3739107332-290452467-3466442662-1001/$RK7QVJQ/vacation photos.7z`).
  3. **USB Device Connections (D:):**
     - **Device 1 (StarkResrch USB):**
       - **Volume Label:** `StarkResrch`
       - **Drive Letter:** `D:`
       - **Serial Number:** `0x5650959f` (Decimal: `1448121759`)
       - **Activity:** Connected on June 29, 2016. Contains the original folder structure `D:\vacation photos\vacation photos\Level 8 Classified\BioChemical\` and the staged archive `D:\vacation photos.7z`.
     - **Device 2 (Stark-IR USB):**
       - **Volume Label:** `Stark-IR`
       - **Drive Letter:** `D:`
       - **Serial Number:** `0xc83a6c7b` (Decimal: `3359272059`)
       - **Activity:** Connected on July 1, 2016. Accessed `D:\Vanko-RAM.dmp` (LNK file created July 1, 2016 at 16:27:02 UTC).
  4. **Classified Document Access:**
     - `/Users/PC User/OneDrive/Documents/Level_8/Stark-Policy-Manual-Classified-version-NOTFORRELEASE.docx` was accessed on June 30, 2016 at 07:47:38 UTC.

- **Confidence Rating:** 5/5 (High confidence; timeline of file creation, LNK files, Dropbox ADS attributes, and USB serial numbers align perfectly).
- **Budget Tally:** 21/21 tool calls used.
- **NPS / Feedback:** 10/10. The DuckDB Parquet querying setup is exceptionally fast and efficient for parsing large forensic timelines.
