# Mission: Run Email Body Extraction Script
**Target Agent:** data-analyst

## Purpose
Run the python script `cases/ROCBA/scratch/read_email_bodies.py` to extract all recovered email bodies from the PST and save them to `cases/ROCBA/scratch/all_emails_bodies.md` for analysis.

## Background
We have successfully carved Fred Rocba's Outlook PST file from the Recycle Bin and extracted its individual email files. We now have a python script `read_email_bodies.py` that can recursively parse these files, decode their headers and body text, and format them into a single markdown file `all_emails_bodies.md` so that the case lead can analyze what corporate IP or communications were inside.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If the script fails to run or output is not generated, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Run the python script `cases/ROCBA/scratch/read_email_bodies.py` using `uv run` or appropriate python environment.
- [x] Verify that `cases/ROCBA/scratch/all_emails_bodies.md` has been successfully created and contains parsed email content.
- [x] Update this mission card with results.

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
  - Loaded and reviewed the `shared-facts-sop` and `delegating-mission-cards-sop` to align with team procedures.
  - Read and analyzed the python script `cases/ROCBA/scratch/read_email_bodies.py` to understand how it recursively parses the individual recovered email files from `cases/ROCBA/scratch/extracted_pst/Outlook Data File` and writes the decoded metadata and body text into a unified markdown file.
  - Executed the script using `uv run python cases/ROCBA/scratch/read_email_bodies.py`.
  - Verified that `cases/ROCBA/scratch/all_emails_bodies.md` was successfully created with 3174 lines of formatted email data containing all 65 emails (42 in `Inbox` and 23 in `Inbox/Maria`).
- **Findings:**
  - The script successfully ran and extracted all 65 recovered email bodies into `cases/ROCBA/scratch/all_emails_bodies.md`.
  - The emails contain communication regarding Fred Rocba's onboarding (e.g., ID 3 welcoming Fred Rocba, ID 2 discussing VPN and RDP setup for workstation `BASE-RD-08` at IP `172.16.6.18`).
  - Key projects mentioned in the email bodies match the summary in `shared_facts.md` (e.g., Project ADAMANTIUM, Project KITT, Project Megaforce, Project Gunstar, and Vibrainium).
- **Confidence Rating:** 5/5 (High confidence, script executed with exit code 0 and output verified directly).
- **Budget Tally:**
  - Orientation: 4 tool calls (Budget: 5)
  - Execution: 3 tool calls (Budget: 10)
  - Reporting: 1 tool call (Budget: 5)
  - Total: 8 tool calls.
- **NPS / Feedback:** 10/10. The script was well-written and handled encoding/HTML parsing robustly. The process was straightforward and execution was extremely fast.
