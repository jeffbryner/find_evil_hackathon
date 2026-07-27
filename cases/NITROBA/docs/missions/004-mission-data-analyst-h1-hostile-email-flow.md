# Mission: H1 — Locate the Hostile Email Flow (SQL Triage)
**Target Agent:** data-analyst

## Purpose
Identify the candidate TCP flow(s) that carried the harassing message to `lilytuckrige@yahoo.com`, producing precise timestamps and 5-tuples for a follow-up deep-dive stream reassembly mission.

## Background
Case NITROBA: capture of dorm G24 uplink, 2008-07-22 01:51:07→06:13:47 UTC, 94,410 packets. Queryable DuckDB table `packets` (case NITROBA) with columns: timestamp, source_ip, dest_ip, source_port, dest_port, protocol, length, info, filename_path, imagename. The harassing message was likely sent via (a) SMTP, (b) Yahoo webmail HTTP POST, or (c) an anonymous web email/"self-destruct" message service over HTTP. Use `uv run helpers/query_parquet.py --case NITROBA --query "<SQL>"` per the `forensic-querying` and `analyze-network-traffic` skills.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** Two-strike rule per query. SQL triage ONLY — do NOT run tshark/tcpdump or follow streams (that is a later sniper mission). If no mail-related traffic found after the checklist queries, report that honestly.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] Protocol distribution baseline: `SELECT protocol, COUNT(*) FROM packets GROUP BY protocol ORDER BY 2 DESC`
- [x] SMTP hunt: packets with protocol='SMTP' OR dest_port IN (25,465,587) — list distinct flows — **NO RESULTS: zero direct SMTP traffic**
- [x] Mail-site DNS hunt: DNS packets whose info matches yahoo|mail|smtp|webmail|sendmail|anonym|selfdestruct — multiple Yahoo, mail.google.com, mail.mac.com, smtp.mac.com, mail.bethr.org, mail.dreamhost.com, mail.m57.biz hits found
- [x] HTTP host profile: `www.sendanonymousemail.net` (7 pkts), `www.willselfdestruct.com` (multiple pkts), `mail.google.com` (151 pkts) flagged as mail/anonymous-messaging hosts
- [x] HTTP POST inventory: PRIME candidates identified — POST /send.php → 69.80.225.91 and POST /secure/submit → 69.25.94.22 with confirmed /secure/success response
- [x] For each PRIME candidate flow: 5-tuples recorded below under Results
- [x] Append new facts to `cases/NITROBA/docs/shared_facts.md` under `# Pending Investigative Leads`
- [x] Update this mission card with results
- [x] Write a chronological technical log of 100% of executed queries and commands to the `-audit.md` file — saved to `004-mission-data-analyst-h1-hostile-email-flow-audit.md`

## Results & Post-Mortem

- **Approach:** SQL-only triage against `packets` table (DuckDB/Parquet). Ran 6 query groups: protocol baseline, SMTP port hunt, DNS mail-keyword hunt, HTTP host profile, HTTP POST inventory, and targeted 5-tuple extraction for PRIME candidates.

- **Findings:**
  - **No direct SMTP traffic** on ports 25/465/587. Email was sent via anonymous web service over HTTP.
  - **Attacker IP:** `192.168.15.4` (Wi-Fi client behind the open router in G24 at 192.168.15.1/192.168.1.254). Distinct from `192.168.1.64` (Ethernet/Mac client).
  - **PRIME CANDIDATE 1 — www.sendanonymousemail.net POST (possible failed attempt due to CAPTCHA re-load):**
    - 5-tuple: `TCP  192.168.15.4:35876 → 69.80.225.91:80`
    - Timestamp: `2008-07-22T06:02:57.548149+00:00`
    - URI: `POST /send.php Host: www.sendanonymousemail.net`
    - Note: CAPTCHA image reloaded after the POST suggesting possible failure.
  - **PRIME CANDIDATE 2 — www.willselfdestruct.com POST (HIGHEST CONFIDENCE — SUCCESS confirmed):**
    - 5-tuple: `TCP  192.168.15.4:36044 → 69.25.94.22:80`
    - Timestamp: `2008-07-22T06:04:24.311700+00:00`
    - URI: `POST /secure/submit Host: www.willselfdestruct.com`
    - Confirmation: Immediately followed by `GET /secure/success` at `2008-07-22T06:04:24.564165+00:00` — server confirmed delivery.
  - **Attack Timeline:**
    - `06:01:26` — Googled "send anonymous mail", DNS resolved `www.sendanonymousemail.net` → `69.80.225.91`
    - `06:01:26` — Loaded sendanonymousemail.net form
    - `06:02:57` — POST /send.php (possibly failed — CAPTCHA re-appeared)
    - `06:03:43` — Navigated via email.about.com to willselfdestruct.com, DNS resolved → `69.25.94.22`
    - `06:03:43` — Loaded /secure/submit form
    - `06:04:24` — POST /secure/submit → GET /secure/success = **EMAIL SENT**
  - **Secondary mail traffic (outside scope):** Gmail (mail.google.com → 74.125.19.19, 151 HTTP pkts from 192.168.1.64), smtp.mac.com lookups, mail.bethr.org, mail.dreamhost.com, mail.m57.biz.

- **Confidence Rating:** PRIME CANDIDATE 2 (willselfdestruct.com POST) = **HIGH (95%)** — confirmed by /secure/success response. PRIME CANDIDATE 1 (sendanonymousemail.net POST) = **MEDIUM (60%)** — possible failed attempt.

- **Budget Tally:** Orientation: 5/5 | Execution: 8/15 (13 total through execution) | Reporting: reporting phase calls excluded per SOP. Total active forensic calls: 13.

- **NPS / Feedback:** Mission well-scoped. The SQL-only approach found both anonymous email services clearly. Recommend follow-up sniper mission to reassemble TCP stream for POST /secure/submit to extract the full message body and confirm recipient is lilytuckrige@yahoo.com.

## Discovered Leads (For Followup)
- **Lead 1:** `192.168.15.4` — Wi-Fi attacker IP; all other TCP connections from this IP should be enumerated to build a full activity profile for attribution.
- **Lead 2:** `www.willselfdestruct.com` POST stream (`192.168.15.4:36044 → 69.25.94.22:80`) — reassemble TCP stream to extract message body, To/From fields, and any identifying info (name, return address, etc.).
- **Lead 3:** `www.sendanonymousemail.net` POST stream (`192.168.15.4:35876 → 69.80.225.91:80`) — reassemble to check if a real email was sent (despite CAPTCHA reload).
- **Lead 4:** `mail.google.com` activity from `192.168.1.64` — Gmail session with key `ik=4233eca8e4`; may reveal attacker's identity or linked account.
- **Lead 5:** DNS queries to `mail.bethr.org`, `mail.dreamhost.com`, `mail.m57.biz` — possible additional email accounts used by suspects; warrant further lookup.
- **Lead 6:** `search.namequery.com:80` (209.53.113.23) — 333 HTTP packets with mass POST `/` from 192.168.15.4; possibly a DNS-hijacking or surveillance tool. Investigate separately.
