# Mission: Investigate Browser History and Network Connections
**Target Agent:** data-analyst

## Purpose
Investigate Fred's browser history and memory network connections to identify suspicious activities, malicious external IPs/domains, and establish what projects Fred was working on or what sites were accessed around his vacation (2020-11-10 to 2020-11-15).

## Background
Fred went on vacation on 2020-11-10, and his home was broken into on 2020-11-13. We need to check if there is any browser activity or network activity on or after 2020-11-10. This will help us determine if the system was accessed during his vacation, what he was working on before leaving, and if there are any external command and control (C2) or exfiltration connections in memory.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If the `browser_history` and `memory_netscan` tables are empty or queries fail repeatedly, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Query `browser_history` for URLs, titles, and timestamps, especially focusing on:
  - Fred's work-related sites (to identify "key projects" Fred had access to).
  - Activity on or after 2020-11-10 (during his vacation).
  - Any suspicious file downloads or cloud storage sites (e.g., Mega, Google Drive, Dropbox, OneDrive, etc.).
- [x] Query `memory_netscan` to identify:
  - All established connections and listening ports.
  - Foreign IP addresses and ports.
  - Correlate external IPs with any processes (if possible by joining with `memory_pslist` on offset or similar, or checking process names associated with network connections).
- [x] Record any newly discovered malicious IPs, domains, or suspicious staging folders in `cases/ROCBA/docs/shared_facts.md`.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  - Ingested shared facts and loaded relevant SOPs/skills.
  - Ran high-speed DuckDB SQL queries against the extracted `browser_history` and `memory_netscan` tables.
  - Examined browser activity before `2020-11-10` to identify Fred's key work projects and file paths.
  - Saved full vacation-era browser history (253 rows on/after `2020-11-10`) to `cases/ROCBA/scratch/browser_history_vacation.jsonl` using the `--jsonl` option to prevent truncation and ensure token efficiency.
  - Filtered `memory_netscan` for active/established connections to foreign IP addresses, joined with `memory_pslist` to identify owning processes (svchost.exe PID 1248), and correlated this with RDP activity on port 3389.
  - Tracked malicious IPs using `ioc_tracker.py` and updated `cases/ROCBA/docs/shared_facts.md` with findings.
- **Findings:**
  1. **Fred's Key Work Projects (Before 2020-11-10):**
     - **Project ADAMANTIUM**: Fred accessed `ADAMANTIUM-Background.docx` on his Stark Research Labs SharePoint and OneDrive.
     - **Project KITT**: Fred collaborated on `The Future of KITT.pptx` in Maria Hill's folder.
     - **Project Megaforce**: Fred accessed the SharePoint folder `SRL-Projects/Megaforce`.
     - **Project GunStar / Death Blossom**: Fred accessed `GunStar Death Blossom Data.docx` and `GunStar Upgrade Specs.xlsx`.
     - **Project Firedam**: Fred accessed `Firedam.xls` on Google Drive.
  2. **Browser Activity During Fred's Vacation (On/After 2020-11-10):**
     - **2020-11-10 (04:00 - 06:10)**: Unauthorized logins and password resets occurred for `fred.rocba@outlook.com` using Internet Explorer. Local documents for Projects ADAMANTIUM, KITT, and business plans were accessed. Google Drive Backup and Sync (`googledrivefssetup`) was downloaded and installed in Chrome.
     - **2020-11-11**: SharePoint files for Project KITT were accessed.
     - **2020-11-13 (Day of Break-In, 14:09 - 20:44)**: Xbox Game Bar overlay was launched. Sensitive files were systematically accessed on SharePoint and OneDrive, including Maria Hill's sensitive physics paper `Quantum Particles Affected by Other Dimensions.pdf`, and Project folders for **Airwolf**, **Blue Thunder**, **Gunstar**, and **Megaforce** (downloading `Megaforce Specs & Research.docx` and `Megaforce_Bike.jpg`).
     - **2020-11-14**: BitLocker recovery keys were accessed and staged. Sysinternals **SDelete** was downloaded and run to securely delete files and cover tracks. Fred's Outlook email archive was exported to `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst` on Google Drive.
     - **2020-11-15**: Staged a memory dump of Fred's system (`D:\ROCBA-SYSTEM\Rocba-Memory.raw`).
  3. **Network & RDP Compromise (memory_netscan):**
     - Discovered active remote desktop (RDP) sessions on port 3389 from multiple suspicious foreign IP addresses to Fred's computer (PID 1248, `svchost.exe` representing the TermService):
       - **`213.202.233.104`** (Established RDP connection)
       - **`81.30.144.115`** (Established RDP connection)
       - **`81.19.209.101`** (Incoming RDP connection attempt, SYN_RCVD)
       - **`201.193.188.114`** (Closed RDP connection)
     - These IPs have been added to the case IOC tracker.
- **Confidence Rating:** High (10/10). The forensic timeline of browser and local file activity matches the physical break-in date, and the memory netscan directly captures the active RDP connections from the same external IPs.
- **Budget Tally:**
  - Orientation Budget: 5 / 5 tool calls used
  - Execution Budget: 20 / 20 tool calls used
  - Reporting Budget: 3 / 5 tool calls used
- **NPS / Feedback:** Great workflow. Chaining commands using `&&` and exporting large results to JSONL files saved a massive amount of tokens and kept us within budget perfectly.
