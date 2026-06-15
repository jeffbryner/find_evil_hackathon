# Mission: Ingest and Parse PCAP to Parquet
**Target Agent:** data-analyst

## Purpose
The purpose of this mission is to convert the raw network capture `nitroba.pcap` into a structured, high-performance Parquet table (`packets.parquet`) in the scratch directory. This will enable rapid SQL-based triage and threat hunting in subsequent stages.

## Background
We have verified the integrity of `cases/NITROBA/images/nitroba.pcap`. To perform efficient analysis of millions of network packets, we must convert it into a structured Parquet file using our local python utility `helpers/pcap_to_parquet.py`.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If the `pcap_to_parquet.py` script fails twice in a row, stop and report.

## Task Checklist
- [x] Verify the input path `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/images/nitroba.pcap`
- [x] Determine the correct output path `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`
- [x] Execute `uv run helpers/pcap_to_parquet.py --pcap cases/NITROBA/images/nitroba.pcap --output cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`
- [x] Verify that the output Parquet file exists and is non-empty
- [x] Verify that the Parquet file can be queried using a simple test query (e.g., `SELECT count(*) FROM 'cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet'`)
- [x] Update this mission card with the packet count and verification status
- [x] Write a chronological technical log of 100% of executed queries and commands to the `003-mission-data-analyst-parse-pcap-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
The PCAP conversion was completed successfully using the `pcap_to_parquet.py` script. A total of **94,410** packets were parsed and written to the high-performance Parquet format.

- **Total Packets Parsed:** 94,410
- **Input File:** `cases/NITROBA/images/nitroba.pcap` (54MB)
- **Output File:** `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` (2.3MB)
- **Verification Query Result:** `SELECT count(*) FROM packets` successfully returned `94410`.

The resulting Parquet file is now ready for rapid SQL-based triage, analysis, and threat hunting.

## Discovered Leads (For Followup)
None during this phase. (Only ingestion and basic verification were performed.)
