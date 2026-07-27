# Forensic Audit Trail: Stage 1 Extraction — pcap Metadata + Parquet Conversion

## 1. Initial Prompt & Parameters
- **Mission Card:** `cases/NITROBA/docs/missions/003-mission-sniper-forensics-pcap-to-parquet.md`
- **Target:** `cases/NITROBA/images/nitroba.pcap` (56,180,821 bytes, MD5: 9981827f11968773ff815e39f5458ec8)
- **Objective:** Run capinfos for metadata; convert pcap to Parquet at `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`; verify (count, min/max timestamp, schema); update shared_facts.md and mission card; write this audit.
- **Budgets:** 5 orientation / 15 execution / 5 reporting = 25 total. Self-terminate at call 20.
- **Executed:** 2026-07-26 by sniper-forensics agent

---

## 2. Chronological Tool Execution Log

- **Tool Call #1:** `Read` `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/missions/003-mission-sniper-forensics-pcap-to-parquet.md`
  -> *Outcome: Loaded mission card. Confirmed budget (5/15/5), objectives, reference commands, container id file location.*

- **Tool Call #2:** `skill` `{"name": "delegating-mission-cards-sop"}`
  -> *Outcome: Loaded mission card SOP. Key rules: update card after each checklist item; two-strike fail-fast; write audit trail with exact commands.*

- **Tool Call #3:** `skill` `{"name": "shared-facts-sop"}`
  -> *Outcome: Loaded shared facts SOP. Key rules: read before acting; append under # Data Inventory; use patch tool.*

- **Tool Call #4:** `Read` `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/shared_facts.md`
  -> *Outcome: Read existing shared facts. Confirmed pcap path/MD5/SHA1. Packet count/timestamps were unknown — exactly what this mission resolves.*

- **Tool Call #5:** `shell` `{"command": "ls cases/NITROBA/scratch/ 2>/dev/null && cat cases/NITROBA/scratch/container_id.txt 2>/dev/null || echo \"no container_id.txt\""}`
  -> *Outcome: Container ID found: `d28f284ea40eed8aa1e63d87e8908b8bc1f0fb2eeed3c8ec25d34bedfe1a7865`. Scratch dir contents: container_id.txt, NITROBA-Scenario.txt.*

- **Tool Call #6:** `shell` `{"command": "ls helpers/pcap_to_parquet.py helpers/query_parquet.py 2>&1"}`
  -> *Outcome: Both helper scripts confirmed present.*

- **Tool Call #7:** `shell` `{"command": "docker ps --filter id=d28f284ea40eed8aa1e63d87e8908b8bc1f0fb2eeed3c8ec25d34bedfe1a7865 --format \"{{.Status}}\""}`
  -> *Outcome: Container status: `Up 13 minutes`. Container is running and available.*

- **Tool Call #8:** `shell` `{"command": "docker exec d28f284ea40eed8aa1e63d87e8908b8bc1f0fb2eeed3c8ec25d34bedfe1a7865 capinfos /case/images/nitroba.pcap 2>&1"}`
  -> *Outcome: SUCCESS. Key results — Number of packets: 94,410; First packet time: 2008-07-22 01:51:07.095278; Last packet time: 2008-07-22 06:13:47.046029; Duration: 15759.950751 seconds; SHA256: 2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb; Encapsulation: Ethernet.*

- **Tool Call #9:** `shell` `{"command": "mkdir -p cases/NITROBA/scratch/nitroba.pcap/parquet && uv run helpers/pcap_to_parquet.py --pcap cases/NITROBA/images/nitroba.pcap --output cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet 2>&1"}`
  -> *Outcome: SUCCESS. Converted 94,410 packets to Parquet. Output: `[+] Successfully converted 94410 packets to cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`*

- **Tool Call #10:** `shell` `{"command": "uv run helpers/query_parquet.py --case NITROBA --schema 2>&1"}`
  -> *Outcome: Schema confirmed. Table: `packets`. Columns: timestamp (VARCHAR), source_ip (VARCHAR), dest_ip (VARCHAR), source_port (INTEGER), dest_port (INTEGER), protocol (VARCHAR), length (INTEGER), info (VARCHAR), filename_path (VARCHAR), imagename (VARCHAR).*

- **Tool Call #11:** `shell` `{"command": "uv run helpers/query_parquet.py --case NITROBA --query \"SELECT COUNT(*) as row_count, MIN(timestamp) as capture_start, MAX(timestamp) as capture_end FROM packets\" 2>&1"}`
  -> *Outcome: Row count = 94,410 confirmed. Timestamp display truncated to `2008-07-` in CLI output (VARCHAR display issue).*

- **Tool Call #12:** `shell` `{"command": "uv run helpers/query_parquet.py --case NITROBA --query \"SELECT MIN(timestamp) as capture_start, MAX(timestamp) as capture_end FROM packets\" 2>&1"}`
  -> *Outcome: Still truncated in display. Proceeded to direct duckdb python verification.*

- **Tool Call #13:** `shell` `{"command": "uv run python -c \"import duckdb; conn = duckdb.connect(); result = conn.execute(\\\"SELECT MIN(timestamp), MAX(timestamp) FROM read_parquet('cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet')\\\").fetchall(); print(result)\" 2>&1"}`
  -> *Outcome: Still truncated. Needed sample rows instead.*

- **Tool Call #14:** `shell` `{"command": "uv run python -c \"import duckdb; conn = duckdb.connect(); result = conn.execute(\\\"SELECT timestamp FROM read_parquet('cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet') LIMIT 3\\\").fetchall(); print(result); result2 = conn.execute(\\\"SELECT timestamp FROM read_parquet('cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet') ORDER BY timestamp DESC LIMIT 3\\\").fetchall(); print(result2)\" 2>&1"}`
  -> *Outcome: Full timestamps confirmed. First: `2008-07-22T01:51:07.095278+00:00`. Last: `2008-07-22T06:13:47.046029+00:00`. Both match capinfos exactly.*

---

## 3. Budget Tally (Pre-Reporting)
- Orientation calls: 6 (calls #1–#6)
- Execution calls: 8 (calls #7–#14)
- **Total forensic tool calls: 14** (reporting writes excluded per SOP)

---

## 4. Findings Summary

| Metric | Value |
|---|---|
| Packet count (capinfos) | 94,410 |
| Parquet row count | 94,410 (100% match) |
| Capture start (UTC) | 2008-07-22T01:51:07.095278+00:00 |
| Capture end (UTC) | 2008-07-22T06:13:47.046029+00:00 |
| Capture duration | 15,759.95 seconds (~4h 22m) |
| File type | Wireshark/tcpdump pcap, Ethernet |
| SHA256 | 2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb |
| Parquet path | `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` |
| DuckDB table name | `packets` |
| Schema columns | timestamp, source_ip, dest_ip, source_port, dest_port, protocol, length, info, filename_path, imagename |

---

## 5. Self-Audit Verification
- Logged 14 tool calls in chronological log above.
- Budget tally states 14 forensic tool calls.
- Counts match. All commands present in full, copy-pasteable form with no truncation or ellipses.
- Final reporting writes (patch mission card, patch shared_facts, write this audit) excluded from count per SOP.
