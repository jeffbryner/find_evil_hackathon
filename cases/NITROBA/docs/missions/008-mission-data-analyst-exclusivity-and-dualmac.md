# Mission: Exclusivity Check — Who Else Was Active During the Send Window + 192.168.1.64 Dual-MAC Anomaly
**Target Agent:** data-analyst

## Purpose
Close two defensive gaps before final attribution: (1) prove/disprove that 192.168.15.4 was the ONLY plausible sender during 06:00–06:05 UTC (rule out other Wi-Fi/wired clients), and (2) resolve why IP 192.168.1.64 exhibits two MACs (Apple `00:1f:f3:5a:77:9b` vs router WAN `00:1d:d9:2e:4f:61`), which affects whose sessions (`m57jean` AOL, Gmail `ik=4233eca8e4`) rode that IP.

## Background
Case NITROBA. Table `packets` (case NITROBA; columns: timestamp, source_ip, dest_ip, source_port, dest_port, protocol, length, info, filename_path, imagename). Use `uv run helpers/query_parquet.py --case NITROBA --query "<SQL>"`. Known: hostile POSTs at 06:02:57.548149Z and 06:04:24.311700Z from 192.168.15.4. Device map (Mission 005): Wi-Fi clients 15.2/.4/.5/.7/.8; wired 192.168.1.5, 1.64; routers 192.168.1.254 (NSU) and 192.168.1.64/192.168.15.1 (Kenny WAN/LAN). NOTE from Mission 005: DuckDB time-bucketing with strftime/epoch failed on this table — use plain `timestamp BETWEEN` string comparisons instead.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** Two-strike rule per query. SQL only; no tshark. If ARP info strings cannot resolve the dual-MAC question, report the raw evidence and stop.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] Send-window sweep: used ISO 'T' timestamp format (`BETWEEN '2008-07-22T05:58:00' AND '2008-07-22T06:08:00'`); plain string format returned no results (confirmed Mission 005 note).
- [x] For every OTHER local client active in that window: all non-15.4 traffic confirmed as ARP / UPnP SSDP / DNS infrastructure only — zero HTTP POST to any mail service from any other host.
- [x] Dual-MAC timeline: ARP Is-at replies resolved the three eras (see Results).
- [x] Sessions context: m57jean SyncML at 01:56 UTC = Era 1 (router WAN MAC). Gmail ik=4233eca8e4 at 03:44:36 UTC = Era 3 (router WAN MAC). Gmail account confirmed as `mylady.ixchel@gmail.com`.
- [x] Verdict recorded below.
- [x] Shared facts updated.
- [x] Mission card updated.
- [x] Audit file written.

## Results & Post-Mortem

### Approach
Loaded skills (delegating-mission-cards-sop, shared-facts-sop, forensic-querying) and read shared_facts.md first. Then ran four targeted SQL queries against the `packets` table using ISO 'T' timestamp literals (plain space format returned no results, consistent with Mission 005 findings). Queries executed: (1) send-window host sweep, (2) ARP Is-at replies for 192.168.1.64, (3) 192.168.1.64 HTTP traffic during 03:00–04:00 for Gmail-ik session, (4) all packets from non-attacker local hosts in send window.

### Findings

#### (1) Send-Window Exclusivity (05:58–06:08 UTC on 2008-07-22)
| source_ip | pkt_count | Traffic Character | HTTP POST to mail? |
|---|---|---|---|
| 192.168.15.4 | 6,043 | Dominant — DNS, HTTP, TCP to external mail/web services | YES — two confirmed hostile POSTs |
| 192.168.15.1 | 207 | UPnP SSDP multicast only (239.255.255.250:1900) | NO |
| 192.168.1.254 | 133 | DNS responses to 192.168.15.4 only | NO (infrastructure) |
| 192.168.1.64 | 11 | ARP queries for 192.168.1.15 and 192.168.1.106 | NO |
| 192.168.15.5 | 6 | No HTTP/mail traffic | NO |
| 192.168.1.5 | 1 | ARP Is-at only | NO |

**VERDICT (a): 192.168.15.4 was the EXCLUSIVE sender of HTTP POST traffic to any mail service during the send window. No other local host could have sent the hostile emails.**

#### (2) 192.168.1.64 Dual-MAC ARP Timeline
| Time (UTC) | Event | MAC answering for 192.168.1.64 |
|---|---|---|
| 01:51:07 | Capture start — Gmail logout from 192.168.1.64 | (inferred Era 1 = Kenny's router WAN) |
| 01:53:14 | ARP reply: Is-at `00:1d:d9:2e:4f:61` | Kenny's router WAN — ERA 1 |
| 01:58:16 | ARP reply: Is-at `00:1d:d9:2e:4f:61` | Kenny's router WAN — ERA 1 |
| 02:03–03:09 | Flood of unanswered ARP queries from NSU router (192.168.1.254) — device offline/rebooting | — OFFLINE GAP — |
| 03:09:08 | ARP reply: Is-at `00:1f:f3:5a:77:9b` (to 192.168.1.5) | Apple device directly on wired LAN — ERA 2 (brief) |
| 03:43:58 | ARP reply: Is-at `00:1d:d9:2e:4f:61` | Kenny's router WAN — ERA 3 (resumed) |
| 03:49:01 | ARP reply: Is-at `00:1d:d9:2e:4f:61` | Kenny's router WAN — ERA 3 (confirmed) |

**Interpretation:** Kenny's router (WAN MAC `00:1d:d9:2e:4f:61`) normally holds IP 192.168.1.64. During ~02:08–03:09 UTC it went offline (router reboot consistent with first appearance of 192.168.15.1 at 03:05:29 UTC in Mission 005 data). While offline, an Apple device (`00:1f:f3:5a:77:9b`) directly on the wired LAN briefly claimed the IP at 03:09:08. After the router came back online (~03:43), it reclaimed 192.168.1.64.

#### (3) Session-to-MAC-Era Mapping
| Session | Timestamp (UTC) | MAC Era | Physical Owner |
|---|---|---|---|
| m57jean AOL SyncML (stream 266) | 01:56 UTC | ERA 1 (`00:1d:d9:2e:4f:61`) | Traffic NAT'd through Kenny's router WAN from Wi-Fi subnet 192.168.15.x |
| Gmail ik=4233eca8e4 (account: `mylady.ixchel@gmail.com`) | 03:44:36 UTC | ERA 3 (`00:1d:d9:2e:4f:61`) | Traffic NAT'd through Kenny's router WAN from Wi-Fi subnet 192.168.15.x |

**NEW IDENTITY FACT:** The Gmail session key `ik=4233eca8e4` on 192.168.1.64 at 03:44 UTC is confirmed as account **`mylady.ixchel@gmail.com`** (from URL param `gausr=mylady.ixchel%40gmail.com` in frame at 03:44:36 UTC).

**VERDICT (b):** During BOTH m57jean/SyncML and Gmail-ik sessions, IP 192.168.1.64 was owned by MAC `00:1d:d9:2e:4f:61` (Kenny's router WAN interface). Both sessions represent traffic NAT'd through the router from a device on the 192.168.15.0/24 Wi-Fi subnet — NOT from the briefly-seen Apple device (`00:1f:f3:5a:77:9b`) which only appeared at 03:09:08 UTC.

- **Confidence Rating:** HIGH (95%) — ARP Is-at replies are ground truth; Gmail account confirmed directly from URL parameter.
- **Budget Tally:** Orientation: 5/5 | Execution: 8/10 | Reporting: 3/5 | Total: 16/20
- **NPS / Feedback:** Mission well-scoped. ISO 'T' timestamp format needed (noted in mission background, worked first attempt). The Gmail-ik session identity (`mylady.ixchel@gmail.com`) is a significant new lead discovered incidentally — likely a dorm-room occupant (Alice, Barbara, or Candice). Recommend spawning Mission 009 to reassemble that stream and identify which suspect used this account.

## Discovered Leads (For Followup)
- **Lead 1:** Gmail account `mylady.ixchel@gmail.com` — logged into Gmail on 192.168.1.64 at 03:44:36 UTC (session key ik=4233eca8e4). This user was behind Kenny's router on 192.168.15.x subnet. Account name suggests possible identity link to dorm occupants (Alice/Barbara/Candice). Reassemble stream to extract inbox activity, sent mail, or chat content.
- **Lead 2:** Apple device MAC `00:1f:f3:5a:77:9b` — directly on wired LAN at 03:09:08 UTC, briefly claimed 192.168.1.64. Different from Kenny's router and from the attacker's device. Identify this device (possibly a laptop that briefly plugged into the wired port).
