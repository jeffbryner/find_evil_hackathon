# Mission: Activity Analysis (Projects, Access, and Intrusion)
**Target Agent:** data-analyst

## Purpose
Investigate Fred Rocba's system activity to answer:
1. What key projects did Fred have access to?
2. What files were accessed, staged, or stolen?
3. When did the activity occur (especially during his vacation from Nov 10 to Nov 15)?
4. How was the data stolen, and where was it transferred?

## Background
Fred worked from home using RDP and cloud applications. He left on vacation on Nov 10, 2020. His home was broken into on Nov 13, 2020. We have disk and memory forensics. We need to query browser history, file system timeline, and process execution artifacts to reconstruct his work profile and any post-vacation/theft activity.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If no queries return results within 5 attempts, stop and report.

## Task Checklist
- [x] Query browser history (`browser_history`) for URLs, domains, and search terms related to corporate projects, source code repositories, cloud storage, or emails (e.g., git, sharepoint, onedrive, dev.azure, github, srl).
- [x] Query the file system timeline (`fs_timeline`) for file/directory creation or access in Fred's user profile (e.g., `C:\Users\fred` or similar) to identify project files, source code, or documents.
- [x] Query process execution (`artifacts_timeline` with prefetch/appcompatcache) to see what software was run on the system and when.
- [x] Focus on the vacation window (2020-11-10 to 2020-11-16): check `fs_timeline`, `artifacts_timeline`, `memory_pslist`, and `memory_netscan` for any activity. Was the system powered on or used? Was there network activity?
- [x] Search for archiving or staging activity (e.g., zip, rar, 7z) and exfiltration indicators (e.g., FTP, mega, dropbox, cloud uploads, usb connections).
- [x] Update `cases/ROCBA/docs/shared_facts.md` under `# Compromised Accounts`, `# Suspicious Files & Staging Directories`, `# Confirmed Exfiltrated/Accessed Data`, and `# Known Malicious IPs & Domains`.
- [x] Update this mission card with results.
- [x] Write a chronological technical log of 100% of executed queries and commands to `002-mission-data-analyst-activity-analysis-audit.md`.

## Results & Post-Mortem
- **Approach:**
  - Conducted high-speed SQL queries against Parquet evidence files using DuckDB.
  - Investigated RDP logon events, file access history (LNK, Jump Lists, BagMRU, Recent Docs, Trusted Documents), and browser history to reconstruct user activity.
  - Tracked process execution (Prefetch, BAM, AppCompatCache) to identify unauthorized execution, staging, and track-covering tools.
- **Findings:**
  - **Project Access:** Fred had access to numerous highly confidential projects including KITT, Megaforce, Airwolf, Gunstar, Blue Thunder, Timothy Dungan - New Alloy Research, Wolves Lair, StarFury, TIVO Research, Ion Thruster, Vibranium, and Adamantium.
  - **Data Theft & Staging:**
    - **Physical Theft (USB):** On Nov 13, 2020, from 19:42 to 21:15, an intruder connected via RDP from IP `52.249.198.56` (Azure). They attached and unlocked a BitLocker To Go USB drive named **`CRIMSON2`** (Drive `F:`, VSN `0xca659866`) and copied multiple sensitive files (including `The Future of KITT.pptx`, `German-KITT-Specs.docx`, `RareEarthDeposits_Confidential.jpg`, `Megaforce Specs & Research.docx`, `Wolves_Lair_Tech_Specs.pptx`, and `blue_thunder_blueprint_by_hurricanepolymar_d3cofgo-fullview.jpg`).
    - **Cloud Exfiltration:** Staged and synced massive amounts of data to Google Drive via Google Drive File Stream (`G:\My Drive\STARK-RESEARCH-LABS FOLDER`).
    - **Email Exfiltration:** On Nov 14, 2020, the intruder exported Fred's entire Outlook mailbox to a PST archive at **`G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst`**, which synced to Google Drive.
    - **Track Covering:** Downloaded and executed Sysinternals **`SDelete`** on Nov 14, 2020 (EULA accepted at 05:42:32) to securely delete files and hide staging activity.
  - **Vacation Activity:** Fred left on vacation on Nov 10, 2020. The system was powered on and accessed remotely via RDP from Azure IP `52.249.198.56` during his vacation (Nov 13 and Nov 14), corresponding to the dates of his home burglary.
- **Confidence Rating:** 5/5 (Extremely high, supported by multi-artifact correlation across RDP event logs, LNK/Jump Lists, prefetch execution, registry MRUs, and browser history).
- **Budget Tally:** 17 tool calls (Orientation + Execution).
- **NPS / Feedback:** 10/10 - Great forensic data integration and incredibly fast SQL query capabilities.

## Discovered Leads (For Followup)
- **Lead 1:** Correlate Azure IP `52.249.198.56` with other network or VPN logs to see if there are additional compromised accounts or connections.
- **Lead 2:** Analyze the contents of the synced Google Drive folder and the exfiltrated `SRL-EMAIL-EXPORT.pst` if available in evidence.
