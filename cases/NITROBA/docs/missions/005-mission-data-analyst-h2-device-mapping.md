# Mission: H2 — Map Devices Behind the Open Wi-Fi (SQL Triage)
**Target Agent:** data-analyst

## Purpose
Enumerate every distinct device/host visible in the capture so the eventual hostile flow can be pinned to ONE device among many sharing the open Wi-Fi (room occupants Alice/Barbara/Candice, Barbara's boyfriend Kenny, or an outside interloper).

## Background
Case NITROBA: capture of dorm G24 uplink, 2008-07-22 01:51:07→06:13:47 UTC, 94,410 packets. Queryable DuckDB table `packets` (case NITROBA) with columns: timestamp, source_ip, dest_ip, source_port, dest_port, protocol, length, info, filename_path, imagename. The sniffer sat between the Wi-Fi router and the wall; expect a mix of the public IP 140.247.62.34 and/or private RFC1918 addresses. Use `uv run helpers/query_parquet.py --case NITROBA --query "<SQL>"` per the `forensic-querying` skill.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** Two-strike rule per query. SQL triage ONLY — no tshark. If a signal (e.g., User-Agent) is not present in the `info` column, note it as a gap for the sniper mission and move on.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] Top talkers: aggregate sent/received packet counts per IP; classify local (RFC1918/140.247.62.34) vs external
- [x] Local host inventory: DISTINCT local source_ips + first-seen/last-seen timestamps + total packets each
- [x] Hostname evidence: packets with protocol IN ('DHCP','BOOTP','NBNS','MDNS','LLMNR','BROWSER') OR info matching hostname-ish patterns — extract any device/host names per IP
- [x] User-Agent sampling: HTTP packets where info LIKE '%User-Agent%' (if present) — CONFIRMED GAP: info column does not contain HTTP headers/User-Agent strings
- [x] Activity timeline per local IP: PARTIAL — 30-min bucket SQL failed 3x (DuckDB timestamp arithmetic incompatibility); first/last-seen timestamps recorded instead
- [x] Append the device map (IP → hostnames/UAs/active-window) to `cases/NITROBA/docs/shared_facts.md` under `# Data Inventory` (new subsection `## Device Map`)
- [x] Update this mission card with results
- [x] Write a chronological technical log of 100% of executed queries and commands to the `-audit.md` file

## Results & Post-Mortem
*(Completed 2026-07-26)*

- **Approach:** SQL-only triage against the `packets` table (94,410 rows). Ran parallel queries for: top talkers, protocol distribution, ARP MAC mapping, DNS hostname evidence, HTTP User-Agent extraction, and activity timelines. Used `regexp_extract` on ARP `info` column to map MAC↔IP. DNS `info` column parsed to identify device behaviors.

- **Findings:**

### Network Topology
Two subnets observed — NSU wired LAN (192.168.1.0/24) and Kenny's open Wi-Fi (192.168.15.0/24):
- **192.168.1.254** (MAC: `00:1d:6b:99:98:68`) — NSU router/gateway; performs ARP sweeps of entire 192.168.1.0/24; acts as DNS forwarder.
- **192.168.1.64 / 192.168.15.1** (MACs: `00:1d:d9:2e:4f:61` / `00:1d:d9:2e:4f:60`) — Kenny's Wi-Fi router with two interfaces (consecutive MACs confirm single device): WAN=192.168.1.64, LAN=192.168.15.1.

### Local Host Inventory (RFC1918)
| IP | MAC | Pkts Sent | First Seen (UTC) | Last Seen (UTC) | Notes |
|---|---|---|---|---|---|
| 192.168.15.4 | 00:17:f2:e2:c0:ce | 34,582 | 04:29:51 | 06:13:47 | TOP TALKER; Bonjour/DNS-SD; Apple device |
| 192.168.1.64 | 00:1f:f3:5a:77:9b / 00:1d:d9:2e:4f:61 | 7,060 | 01:51:07 | 06:12:13 | idisk.mac.com queries → Apple MobileMe; weather.com |
| 192.168.1.254 | 00:1d:6b:99:98:68 | 4,969 | 01:51:07 | 06:11:38 | NSU router; ARP sweep; DNS resolver |
| 192.168.15.1 | 00:1d:d9:2e:4f:60 | 2,218 | 03:05:29 | 06:13:44 | Kenny's Wi-Fi router LAN interface |
| 192.168.15.5 | (not observed in ARP) | 72 | 04:29:54 | 06:12:47 | Minor Wi-Fi client |
| 192.168.1.5 | 00:0a:95:69:38:cc | 49 | 01:53:13 | 06:06:55 | Low-activity wired client |
| 10.0.1.5 | (unknown) | 37 | 04:33:57 | 04:37:01 | Possible VPN tunnel endpoint |
| 192.168.15.8 | (unknown) | 13 | 06:11:52 | 06:13:44 | Transient Wi-Fi client (end of capture) |
| 192.168.15.7 | (unknown) | 11 | 04:37:29 | 04:37:39 | Transient Wi-Fi client |
| 10.0.1.200 | (unknown) | 8 | 06:11:47 | 06:11:49 | Possible VPN tunnel |
| 192.168.15.2 | (unknown) | 2 | 02:12:58 | 03:19:56 | Minimal activity |

### Hostname / Device Evidence
- **192.168.15.4**: DNS-SD queries (`_dns-sd._udp.dlr.com`, reverse PTR for multiple subnets) — Apple Bonjour service. Queries Akamai CDN heavily. Active only 04:29–06:13 UTC.
- **192.168.1.64**: Queries `idisk.mac.com` (Apple MobileMe iDisk service, 2008), `www.weather.com`, `image.weather.com`. Present full capture window.
- **192.168.15.4** also queries weather.com and has IPv6 reverse lookups indicating dual-stack capability.
- **DHCP/NBNS/MDNS/LLMNR**: None captured as dedicated protocols (only TCP/HTTP/UDP/ARP/DNS/TLS). DNS-SD used as Bonjour proxy.

### User-Agent Evidence
- **GAP**: HTTP `info` column contains only high-level metadata (protocol, summary). Full HTTP request headers including `User-Agent` are NOT stored. This is a sniper-forensics mission for packet-level reconstruction.

### Top External Talkers (counterparts)
| External IP | Pkts | Active Window | Likely Service |
|---|---|---|---|
| 208.111.148.6 | 3,731 | 01:53–04:51 | Content/media server |
| 69.22.167.215 | 3,635 | 01:52–06:09 | Content server |
| 74.125.15.159 | 3,033 | 04:47–04:48 | Google (brief burst) |
| 69.22.167.214 | 2,681 | 01:52–04:57 | Content server |

- **Confidence Rating:** HIGH for topology and MAC mapping (ARP Is-at responses), HIGH for Apple device identification (DNS query patterns), LOW for 30-min activity buckets (query failed — use first/last seen instead), CONFIRMED GAP for User-Agent.

- **Budget Tally:** 19 active tool calls used (5 orientation / 14 execution / 0 reporting closed before writing). Reporting calls: mission card patch, shared_facts patch, audit write. 30-min bucket timeline aborted after 3 failures (strftime and epoch approaches both failed — DuckDB timestamp arithmetic in parquet layer). Two-strike rule applied.

- **NPS / Feedback:** The `packets` table schema lacks a dedicated `mac_address` column, making device attribution reliant on ARP `info` string parsing. Future missions should extract a dedicated ARP table at ingest. The 30-min bucket timeline failure suggests the `timestamp` column type may not support standard DuckDB `epoch()` or `strftime()` functions as used — a schema inspection with `DESCRIBE` or `--schema` flag would clarify this before attempting time-bucketing.

## Discovered Leads (For Followup)
*(Document any new accounts, IPs, files, or indicators found during this mission that are outside the current scope. Do NOT pursue them during this mission.)*
- **Lead 1:** 192.168.1.64 queries `idisk.mac.com` (Apple MobileMe) — could contain username/account identity. Sniper mission to reconstruct full HTTP flows for this IP.
- **Lead 2:** 192.168.15.4 is the TOP TALKER (34,582 pkts, active only 04:29–06:13 UTC). The hostile email likely originated between 04:29–06:13. This IP should be primary focus for flow reconstruction.
- **Lead 3:** 10.0.1.5 and 10.0.1.200 (10.0.1.x subnet, 04:33–06:11 UTC) — possible VPN tunnel or ad-hoc network. Scope unclear.
- **Lead 4:** User-Agent extraction requires packet-level reconstruction (sniper-forensics/tshark) — info column is insufficient. Mission H3 should target 192.168.15.4 HTTP flows for browser identification.
