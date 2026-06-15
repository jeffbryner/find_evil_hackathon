# Mission: Extract Scenario PDF Text
**Target Agent:** sniper-forensics

## Purpose
The case scenario is stored in a 4.4 MB PDF file at `cases/NITROBA/docs/NITROBA-Scenario.pdf`. This file exceeds the host's direct PDF read limits. We need to convert this PDF to plain text so that the Case Lead can read it and formulate investigative hypotheses.

## Background
We are starting the NITROBA case. The primary evidence image is `nitroba.pcap` in `cases/NITROBA/images/`. The PDF scenario contains the background details and goals.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If `pdftotext` or Python-based extraction fails twice in a row, stop and report the error.

## Task Checklist
- [x] Locate `/case/docs/NITROBA-Scenario.pdf` inside the SIFT container
- [x] Attempt to convert the PDF to text using `pdftotext /case/docs/NITROBA-Scenario.pdf /scratch/NITROBA-Scenario.txt` inside the container
- [ ] If `pdftotext` is not available, write a quick python script using `pypdf` or standard libraries to extract text and run it
- [x] Verify that `/scratch/NITROBA-Scenario.txt` is created and has content
- [x] Update this mission card with results and the first 20 lines of the extracted text
- [x] Write a chronological technical log of 100% of executed queries and commands to the `001-mission-sniper-forensics-extract-scenario-pdf-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
The PDF scenario has been successfully extracted to plain text at `/scratch/NITROBA-Scenario.txt` using `pdftotext` in the `NITROBA` container.

### First 20 Lines of Extracted Text
```
Harassment at
NITROBA
State University

1

The case

NITROBA
State University

You are a staff member at the Nitroba University Incident Response Team.
Lily Tuckrige is teaching chemistry CHEM109 this summer at NSU.
Tuckrige has been receiving harassing email at her personal email address.
• Tuckrige's personal email is lilytuckrige@yahoo.com
• She thinks that it is from one of the students in her class.
Tuckrige contacted IT support.
• She sent a screen shot of one of the harassing email messages.
• She wants to know who is doing it.

istockphoto.com
2
```

## Discovered Leads (For Followup)
- **Primary Targets**: Identify who sent emails to `lilytuckrige@yahoo.com` in `nitroba.pcap`.
- **Network Scope**: Map out the Nitroba dorm room network (IP: `140.247.62.34`, G24.student.nitroba.org).
- **Roommates**: Alice, Barbara, Candice (using an open Wi-Fi router set up by Kenny).
- **Suspects (Class List)**:
  - Amy Smith
  - Burt Greedom
  - Tuck Gorge
  - Ava Book
  - Johnny Coach
  - Jeremy Ledvkin
  - Nancy Colburne
  - Tamara Perkins
  - Esther Pringle
  - Asar Misrad
  - Jenny Kant
