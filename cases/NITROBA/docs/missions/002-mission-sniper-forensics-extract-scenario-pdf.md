# Mission: Extract Text of NITROBA Scenario PDF for Case Lead
**Target Agent:** sniper-forensics

## Purpose
The case scenario is locked inside `cases/NITROBA/docs/NITROBA-Scenario.pdf` (4,401,268 bytes — exceeds the case lead's direct read limit). Extract its full text so the case lead can read the scenario and generate hypotheses.

## Background
New case NITROBA. Evidence is a single pcap (handled by a separate inventory mission — DO NOT touch the pcap). This mission is documentation extraction ONLY.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** Try `pdftotext` first (locally via `uv`/system, or inside the SIFT container — consult the `sift-docker` skill for path mapping; the case dir is read-only in the container, output MUST go to `/scratch/`). If `pdftotext` fails twice, try ONE alternative extraction method (e.g., python `pypdf`). If that also fails twice, stop and report `[partially_completed]`. Do NOT attempt OCR of embedded images — text layer only.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] Extract text layer of `cases/NITROBA/docs/NITROBA-Scenario.pdf` to `cases/NITROBA/scratch/NITROBA-Scenario.txt` (host path; container path `/scratch/NITROBA-Scenario.txt`)
- [x] Verify the output file is non-empty and contains readable scenario text (read first ~50 lines)
- [x] Append a concise scenario summary (who/what/when/question-to-answer, named persons, addresses, key facts) under `# Case Background / Scenario` in `cases/NITROBA/docs/shared_facts.md`
- [x] Update this mission card with results (include the full path of the extracted txt)
- [x] Write a chronological technical log of 100% of executed queries and commands to the `-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
- **Approach:** `pdftotext` was unavailable (command not found on host). Fell back to Python `pypdf` (v6.14.2), installed via `uv add pypdf`. Extracted text layer from all 15 pages to scratch. Output verified non-empty (116 lines, 2,662 chars). Scenario summary written to `shared_facts.md`.
- **Findings:**
  - Extracted text file: `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/NITROBA-Scenario.txt` (116 lines, 2,662 chars, 15 PDF pages)
  - Victim: Lily Tuckrige (lilytuckrige@yahoo.com), CHEM109 professor at NSU
  - Suspected harassment source IP: 140.247.62.34 → G24.student.nitroba.org (dorm with open Wi-Fi)
  - Dorm occupants: Alice, Barbara, Candice (Barbara's boyfriend Kenny installed the open router)
  - 11 student suspects in class list
  - Evidence: nitroba.pcap (network packet capture)
- **Confidence Rating:** High — text layer extracted cleanly; scenario content is coherent and complete.
- **Budget Tally:** 10 tool calls used (5 orientation / 3 execution / 2 reporting — within budget)
- **NPS / Feedback:** Mission card was well-formed. Suggestion: include `pypdf` in project `pyproject.toml` dependencies by default to avoid the install step.

## Discovered Leads (For Followup)
- **Lead 1:** IP 140.247.62.34 (G24.student.nitroba.org) — key source IP; should be filtered in pcap analysis.
- **Lead 2:** Open Wi-Fi router in dorm room — traffic could come from anyone in range, not just the three named occupants.
- **Lead 3:** 11 CHEM109 students to cross-reference against pcap identifiers (browser user-agent, email headers, etc.).
