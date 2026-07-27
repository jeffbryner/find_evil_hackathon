# Mission: Stage 1 Extraction — pcap Metadata + Parquet Conversion
**Target Agent:** sniper-forensics

## Purpose
Make `nitroba.pcap` queryable: establish the capture window (ground truth for the case timeline) and convert packets to a Parquet table for high-speed SQL hunting by downstream missions.

## Background
Case NITROBA: harassing emails to lilytuckrige@yahoo.com traced to 140.247.62.34 (dorm G24, open Wi-Fi). Evidence: `cases/NITROBA/images/nitroba.pcap` (56,180,821 bytes, MD5 9981827f11968773ff815e39f5458ec8). Mission 001 could not get packet count/timespan (no capinfos on host). A SIFT container may already exist (`cases/NITROBA/scratch/container_id.txt`). This mission is EXTRACTION/INGESTION ONLY — no protocol hunting, no stream following.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** Two-strike rule per command. If the SIFT container cannot be started/reached after 2 attempts, record capinfos as unavailable and still attempt the local Parquet conversion (`uv run helpers/pcap_to_parquet.py` runs on host, no container needed). If Parquet conversion fails twice, stop and report `[partially_completed]`.

## Reference Commands (validated by Case Lead)
- Container start (if needed): `uv run start_case_container.py --case NITROBA` (verify script name first; container id file: `cases/NITROBA/scratch/container_id.txt`)
- capinfos inside container (images mount): `docker exec <container> capinfos /case/images/nitroba.pcap`
- Parquet conversion (host): `uv run helpers/pcap_to_parquet.py --pcap cases/NITROBA/images/nitroba.pcap --output cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`
- Verification: `uv run helpers/query_parquet.py --case NITROBA --schema` then `SELECT COUNT(*), MIN(timestamp), MAX(timestamp) FROM packets`

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] Run `capinfos` on the pcap (SIFT container) — record packet count, capture start (UTC), capture end (UTC), duration
- [x] Convert pcap to Parquet at `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` (exact path matters for table naming)
- [x] Verify Parquet: row count, MIN/MAX timestamp, list of schema columns (record them in this card for downstream analysts)
- [x] Append capture window + parquet path + row count + schema columns to `# Data Inventory` in `cases/NITROBA/docs/shared_facts.md`
- [x] Update this mission card with results
- [x] Write a chronological technical log of 100% of executed queries and commands to the `-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
*(Completed 2026-07-26 by sniper-forensics)*

- **Approach:** Used SIFT Docker container (d28f284ea40e) for capinfos metadata extraction; ran host-side `uv run helpers/pcap_to_parquet.py` for Parquet conversion; verified with DuckDB queries via `query_parquet.py` and direct Python duckdb calls.

- **Findings:**
  - **capinfos (SIFT container):**
    - File type: Wireshark/tcpdump pcap, Ethernet encapsulation
    - Packet count: **94,410**
    - First packet: `2008-07-22 01:51:07.095278 UTC`
    - Last packet: `2008-07-22 06:13:47.046029 UTC`
    - Capture duration: **15,759.95 seconds** (~4 hours 22 minutes)
    - Avg packet size: 579.07 bytes; Avg rate: 5 packets/s
    - SHA256: `2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb`
  - **Parquet file:** `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`
    - Row count: **94,410** (matches capinfos — 100% conversion)
    - MIN timestamp: `2008-07-22T01:51:07.095278+00:00`
    - MAX timestamp: `2008-07-22T06:13:47.046029+00:00`
    - Schema columns: `timestamp`, `source_ip`, `dest_ip`, `source_port`, `dest_port`, `protocol`, `length`, `info`, `filename_path`, `imagename`
    - DuckDB table name (for queries): `packets`

- **Confidence Rating:** HIGH — packet count from capinfos (94,410) exactly matches Parquet row count; timestamps are consistent between capinfos and duckdb samples.

- **Budget Tally:** 14 forensic tool calls used (5 orientation + 9 execution). Final 3 calls for reporting (mission card + shared_facts + audit). Total: ~17/25.

- **NPS / Feedback:** Mission well-scoped and efficient. Reference commands in the mission card were accurate. The `query_parquet.py` CLI truncates VARCHAR timestamp display but raw duckdb python confirmed full values. Recommend noting this display limitation in future mission cards.

## Discovered Leads (For Followup)
*(Document any new accounts, IPs, files, or indicators found during this mission that are outside the current scope. Do NOT pursue them during this mission.)*
