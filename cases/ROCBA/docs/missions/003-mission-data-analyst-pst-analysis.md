# Mission: PST Files, PowerShell History, and Keyword Search
**Target Agent:** data-analyst

## Purpose
Investigate Outlook PST/OST email files, retrieve any PowerShell command history, and perform a keyword search across all timelines for terms related to the burglary, vacation, and potential insider threat indicators (such as "Cobra", "Redguard", "Disney", "burglary", "break-in", "theft").

## Background
We have found that a complete Outlook email archive (`SRL-EMAIL-EXPORT.pst`) was copied to Google Drive, and a local backup (`backup.pst`) was accessed. We also suspect that Fred Rocba (alias "Cobra" / "Redguard") may be an insider threat who staged the burglary. We need to find any email communication, command-line history, or keyword matches that shed light on his plans, motivations, or coordination.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 25 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no PST files or command history are found in 5 queries, stop and report.

## Task Checklist
- [x] Search for all `.pst` and `.ost` files in the filesystem timeline (`fs_timeline`) and identify their paths and creation/modification timestamps.
- [x] Check if there is any PowerShell command history (e.g., `ConsoleHost_history.txt` or registry keys) in `fs_timeline` or `artifacts_timeline`.
- [x] Perform a keyword search in `fs_timeline`, `artifacts_timeline`, and `browser_history` for: "burglary", "break-in", "theft", "vacation", "Disney", "Cobra", "Redguard", "secret", "weapon", "sell", "buyer".
- [x] Identify any other communications or documents that discuss Fred's employment, resignation, or vacation plans.
- [x] Update `cases/ROCBA/docs/shared_facts.md` with findings.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:** High-speed SQL querying against DuckDB Parquet databases (`fs_timeline`, `artifacts_timeline`, `browser_history`) using custom Python-wrapped helper tools. Refined search criteria by filtering out system noise (e.g., `/Windows`, `/Program Files`, and "Upsell" keywords) to isolate user profile activity and targeted exfiltration artifacts.
- **Findings:**
  - **PST/OST Analysis:**
    - Local Outlook backup `C:\Users\fredr\OneDrive\Documents\Outlook Files\backup.pst` (size: 20,587,520 bytes) was deleted on `2020-11-14 05:39:11` and moved to the Recycle Bin as `/$Recycle.Bin/.../$RDNBREY.pst`.
    - Exactly 11 seconds later, at `2020-11-14 05:39:22`, a new email archive `G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst` was created/accessed on Google Drive. It was accessed multiple times up to `06:00:54`, and Outlook updated registry values (`LastCorruptStore`) to point to it at `06:09:16`.
  - **PowerShell History:**
    - No PowerShell history file exists for user `fredr`. A `ConsoleHost_history.txt` file exists for user `srl-h` on `2020-10-20` but contains no parsed command entries. UserAssist shows `powershell.exe` execution count is 0 for `fredr` (indicating potential execution clearing).
  - **Keyword Search & Project Harvesting:**
    - No direct matches for burglary, break-in, theft, vacation, or Disney were found in the browser history or user files.
    - Critical hits for "secret" and "weapon" include: `secretweapon.jpg` (Project KITT, accessed `2020-11-13 19:51:11`) and `weapons.jpg` (Project Airwolf, accessed `2020-11-13 20:21:22`).
    - Most importantly, Fred Rocba accessed `C:\Users\fredr\OneDrive\Desktop\Research to Weaponize the Ion Thruster.docx` on `2020-11-14 05:50:16` right during his early morning email exfiltration and SDelete window.
  - **Explorer Search History (WordWheelQuery):**
    - Explorer search history for `fredr` on `2020-11-14 06:04:07` shows active searches for: `backup.pst`, `backup`, `*.pst`, `sdelete`, `bitlocker recovery key`, `bitlocker`, `cobra`, `crimson`, `airwolf`, `kitt`, `starfury`.
  - **Personal Email/Alias & Browser History:**
    - Fred Rocba logged into personal email `redguard.cobra@gmail.com` on Chrome and visited `http://cobracommandcenter.com/` on `2020-11-07 19:23:30`.
  - **Employment Offer:**
    - Found `/Users/fredr/Google Drive/SRL-Offer.pdf` accessed on `2020-11-01 10:23:11`.
- **Confidence Rating:** 5/5. The timeline, file sizes, Explorer search history, and browser profile artifacts provide a highly aligned, definitive, and comprehensive timeline of Fred Rocba's insider threat data harvesting, email exfiltration, and anti-forensics secure-deletion activities.
- **Budget Tally:**
  - Orientation: 5 tool calls (Budget: 5)
  - Execution: 25 tool calls (Budget: 25)
  - Reporting: 3 tool calls (Budget: 5)
  - Total: 33 tool calls.
- **NPS / Feedback:** 10/10. The Parquet timelines combined with DuckDB allow for incredibly fast and highly precise forensic querying. WordWheelQuery was an absolute goldmine of user intent. Filtering out system noise was essential to pinpointing the insider threat activity.
