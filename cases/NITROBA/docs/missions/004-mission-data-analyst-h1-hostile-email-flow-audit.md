# Forensic Audit Trail: H1 — Locate the Hostile Email Flow (SQL Triage)

## 1. Initial Prompt & Parameters
- **Mission Card:** `cases/NITROBA/docs/missions/004-mission-data-analyst-h1-hostile-email-flow.md`
- **Case:** NITROBA
- **Target Table:** `packets` (DuckDB/Parquet at `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet`)
- **Objective:** Identify TCP flow(s) that carried the harassing message to `lilytuckrige@yahoo.com` — SMTP hunt, DNS hunt, HTTP host profile, HTTP POST inventory — produce 5-tuples + timestamps for follow-up stream reassembly.
- **Orientation Budget:** 5 tool calls | **Execution Budget:** 15 tool calls | **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of 25 total)
- **Fail-Fast:** Two-strike rule per query; SQL triage ONLY — no tshark/tcpdump.
- **System Date:** 2026-07-26

---

## 2. Chronological Tool Execution Log

- **Tool Call #1:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/missions/004-mission-data-analyst-h1-hostile-email-flow.md`
  -> *Outcome: Read mission card. Confirmed 25-call budget, checklist items, and SQL-only constraints.*

- **Tool Call #2:** `skill` — `delegating-mission-cards-sop`
  -> *Outcome: Loaded SOP for mission card structure, checkpointing rules, audit trail requirements, and two-strike fail-fast.*

- **Tool Call #3:** `skill` — `shared-facts-sop`
  -> *Outcome: Loaded SOP for shared facts management. Identified required sections and update procedure.*

- **Tool Call #4:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/shared_facts.md`
  -> *Outcome: Ingested existing case context. Key IP: 140.247.62.34 (G24.student.nitroba.org). Victim: lilytuckrige@yahoo.com. Packets table: 94,410 rows.*

- **Tool Call #5:** `skill` — `forensic-querying`
  -> *Outcome: Loaded forensic querying SOP. Confirmed `uv run helpers/query_parquet.py --case NITROBA --query "..."` syntax, ILIKE usage, and JSONL output flags.*

  **[ORIENTATION PHASE COMPLETE — 5/5 calls used]**

- **Tool Call #6:** `shell` — Protocol distribution baseline:
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT protocol, COUNT(*) as cnt FROM packets GROUP BY protocol ORDER BY 2 DESC" --limit 50
  ```
  -> *Outcome: TCP=72387, HTTP=9748, UDP=4295, ARP=4026, DNS=2905, TLS=979, IPv4=45, ICMP=20, Unknown=5. No dedicated SMTP protocol row present.*

- **Tool Call #7:** `shell` — SMTP port hunt:
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT source_ip, dest_ip, dest_port, MIN(timestamp) as first_seen, MAX(timestamp) as last_seen, COUNT(*) as pkt_count FROM packets WHERE protocol='SMTP' OR dest_port IN (25,465,587) OR source_port IN (25,465,587) GROUP BY source_ip, dest_ip, dest_port ORDER BY pkt_count DESC" --limit 50
  ```
  -> *Outcome: Query returned no results. Zero direct SMTP traffic in capture. Email was NOT sent via raw SMTP — webmail path confirmed.*

- **Tool Call #8:** `shell` — DNS mail-keyword hunt:
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT info, MIN(timestamp) as first_seen, COUNT(*) as cnt FROM packets WHERE protocol='DNS' AND (info ILIKE '%yahoo%' OR info ILIKE '%mail%' OR info ILIKE '%smtp%' OR info ILIKE '%webmail%' OR info ILIKE '%sendmail%' OR info ILIKE '%anonym%' OR info ILIKE '%selfdestruct%' OR info ILIKE '%send%') GROUP BY info ORDER BY first_seen" --limit 100
  ```
  -> *Outcome: 100 rows returned. Key findings: DNS Query for www.sendanonymousemail.net at 2008-07-22T06:01:26Z (→69.80.225.91); DNS Query for www.willselfdestruct.com at 2008-07-22T06:03:43Z (→69.25.94.22); DNS for mail.google.com at 03:44Z; mail.mac.com/smtp.mac.com at 03:43-03:48Z; mail.bethr.org at 05:14Z; mail.dreamhost.com at 05:26Z; mail.m57.biz at 05:32Z.*

- **Tool Call #9:** `shell` — HTTP host profile:
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT regexp_extract(info, 'Host: ([^\r\n]+)', 1) as host, COUNT(*) as cnt FROM packets WHERE protocol='HTTP' AND info ILIKE '%Host:%' GROUP BY host ORDER BY cnt DESC" --limit 50
  ```
  -> *Outcome: Top hosts — ax.phobos.apple.com.edgesuite.net (554), search.namequery.com:80 (333), ebaystatic.com hosts (187+), mail.google.com (151). mail.google.com flagged as mail host. search.namequery.com flagged as anomalous.*

- **Tool Call #10:** `shell` — HTTP POST inventory (ALL POST requests):
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT timestamp, source_ip, dest_ip, source_port, dest_port, info FROM packets WHERE protocol='HTTP' AND info ILIKE '%POST%' ORDER BY timestamp" --limit 100 --jsonl 2>/dev/null | head -200
  ```
  -> *Outcome: 101 JSONL lines returned (truncated at 100 results). Key POST findings: POST /m57jean → sync.aol.com (192.168.1.64); POST /v6/UpdateRegulationService → update.microsoft.com (192.168.1.64); POST /mail/?ui=2... → mail.google.com (192.168.1.64, 03:44 UTC); POST / → search.namequery.com:80 (192.168.15.4, 04:36 UTC onward, ~333 times). Note: POST to sendanonymousemail and willselfdestruct not visible in first 100 because output was truncated to limit 100. Subsequent targeted queries captured them.*

- **Tool Call #11:** `shell` — HTTP mail-related host filter (flagging anonymous/mail endpoints):
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT regexp_extract(info, 'Host: ([^\r\n]+)', 1) as host, COUNT(*) as cnt FROM packets WHERE protocol='HTTP' AND info ILIKE '%Host:%' AND (info ILIKE '%yahoo%' OR info ILIKE '%mail%' OR info ILIKE '%compose%' OR info ILIKE '%webmail%' OR info ILIKE '%anonymous%' OR info ILIKE '%send%') GROUP BY host ORDER BY cnt DESC" --limit 50
  ```
  -> *Outcome: mail.google.com=151, www.sendanonymousemail.net=7, www.willselfdestruct.com=1 (but multiple linked via about.com referrer). Both anonymous email sites flagged as PRIME candidates.*

- **Tool Call #12:** `shell` — Full packet detail for PRIME candidates (sendanonymousemail + willselfdestruct):
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT timestamp, source_ip, dest_ip, source_port, dest_port, protocol, info FROM packets WHERE info ILIKE '%sendanonymousemail%' OR info ILIKE '%willselfdestruct%' ORDER BY timestamp" --limit 50 --jsonl 2>/dev/null
  ```
  -> *Outcome: 45 JSONL entries. Confirmed full attack timeline: Google search for "send anonymous mail" → sendanonymousemail.net form load → POST /send.php (06:02:57Z) → CAPTCHA reload (possible failure) → navigation via email.about.com → willselfdestruct.com form → POST /secure/submit (06:04:24Z) → GET /secure/success (06:04:24Z) = EMAIL SENT. All traffic from 192.168.15.4.*

- **Tool Call #13:** `shell` — Flow summary for PRIME candidates:
  ```
  uv run helpers/query_parquet.py --case NITROBA --query "SELECT source_ip, dest_ip, source_port, dest_port, protocol, MIN(timestamp) as first_seen, MAX(timestamp) as last_seen, COUNT(*) as pkt_count FROM packets WHERE info ILIKE '%sendanonymousemail%' OR info ILIKE '%willselfdestruct%' GROUP BY source_ip, dest_ip, source_port, dest_port, protocol ORDER BY first_seen" --limit 50
  ```
  -> *Outcome: Full 5-tuple table with timestamps for all flows touching both sites. PRIME CANDIDATE 1: 192.168.15.4:35876→69.80.225.91:80 at 06:02:57Z. PRIME CANDIDATE 2: 192.168.15.4:36044→69.25.94.22:80 at 06:04:24Z (followed immediately by success response).*

  **[EXECUTION PHASE COMPLETE — 8 execution calls (13 total) used]**

---

## 3. Key Findings Summary

| Priority | Flow (5-Tuple) | Timestamp | URI | Verdict |
|---|---|---|---|---|
| **PRIME (HIGH 95%)** | TCP 192.168.15.4:36044 → 69.25.94.22:80 | 2008-07-22T06:04:24.311700Z | POST /secure/submit (willselfdestruct.com) | **CONFIRMED SEND** — /secure/success returned |
| **PRIME (MED 60%)** | TCP 192.168.15.4:35876 → 69.80.225.91:80 | 2008-07-22T06:02:57.548149Z | POST /send.php (sendanonymousemail.net) | Possible — CAPTCHA re-loaded after POST |

**Attacker IP:** `192.168.15.4` (Wi-Fi subnet 192.168.15.0/24, behind open router in G24)

---

## 4. Budget Tally (Pre-Reporting)

| Phase | Allocated | Used |
|---|---|---|
| Orientation | 5 | 5 |
| Execution | 15 | 8 |
| **Active Total** | **20** | **13** |

*Reporting tool calls (mission card patch, shared_facts patch, this audit write) are excluded from the tally per the delegating-mission-cards-sop recursive audit exclusion rule.*
