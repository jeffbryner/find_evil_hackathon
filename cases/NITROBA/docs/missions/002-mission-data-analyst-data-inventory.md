# Mission: Data Inventory and Environment Initialization
**Target Agent:** data-analyst

## Purpose
The purpose of this mission is to perform a data inventory of the NITROBA case images, verify their integrity, initialize the SIFT forensic environment, and record the findings in `shared_facts.md`.

## Background
We are initiating the forensic analysis of the NITROBA case. The primary evidence file is `cases/NITROBA/images/nitroba.pcap`. We need to verify what evidence is available, check file metadata, and ensure the SIFT container is started and ready.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If the SIFT container cannot be started or the evidence file is missing/corrupted, stop and report.

## Task Checklist
- [x] Verify the existence of `cases/NITROBA/images/nitroba.pcap` on the host
- [x] Calculate the MD5 and SHA-256 hashes of `nitroba.pcap`
- [x] Get the file size and metadata of `nitroba.pcap`
- [x] Start the SIFT container for the case `NITROBA` using `uv run start_case_container.py --case NITROBA` if it is not already running
- [x] Verify the container is running and accessible
- [x] Check if `nitroba.pcap` is visible inside the container at `/case/images/nitroba.pcap`
- [x] Update the `Data Inventory` section of `cases/NITROBA/docs/shared_facts.md` with the verified metadata and hashes
- [x] Update this mission card with the findings
- [x] Write a chronological technical log of 100% of executed queries and commands to the `002-mission-data-analyst-data-inventory-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
The data inventory and SIFT container verification have been successfully completed.
- **Evidence File**: `nitroba.pcap`
- **File Size**: 56,180,821 bytes
- **MD5 Hash**: `9981827f11968773ff815e39f5458ec8`
- **SHA-256 Hash**: `2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb`
- **SIFT Container**: Already running and verified healthy (Container ID: `9e669668f067`).
- **Container Path Visibility**: Verified at `/case/images/nitroba.pcap` with matching hashes.

All tasks have been executed successfully within the designated budgets.

## Discovered Leads (For Followup)
None.
