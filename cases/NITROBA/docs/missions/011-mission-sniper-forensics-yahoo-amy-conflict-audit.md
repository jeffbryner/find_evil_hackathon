# Forensic Audit Trail: Mission 011 — Resolve `amy789smith` Conflict

## 1. Initial Prompt & Parameters
- **Mission Card:** `cases/NITROBA/docs/missions/011-mission-sniper-forensics-yahoo-amy-conflict.md`
- **Target:** Determine whether `amy789smith` occupies YMSG Key 1 (logged-in user) or Key 5/4 (remote peer) in TCP stream 1865. Verify source MAC.
- **Evidence:** `/case/images/nitroba.pcap` in SIFT container `NITROBA`; outputs to `/scratch/nitroba.pcap/` (host: `cases/NITROBA/scratch/nitroba.pcap/`)
- **Budget:** Orientation=4, Execution=11, Reporting=4 (Total=19). Self-terminate at 15.
- **Constraint:** Report what bytes say. Do not shade answer toward existing theory.

## 2. Chronological Tool Execution Log

- **Tool Call #1:** `skill` — `delegating-mission-cards-sop` → *Outcome: Loaded SOP for mission card protocol, budget tracking, living card rules.*

- **Tool Call #2:** `skill` — `shared-facts-sop` → *Outcome: Loaded SOP for shared knowledge base usage.*

- **Tool Call #3:** `Read` — `cases/NITROBA/docs/missions/011-mission-sniper-forensics-yahoo-amy-conflict.md` → *Outcome: Mission card read. Budget=19 total. Evidence confirmed at /case/images/nitroba.pcap in NITROBA container. Key tasks identified: MAC verification and YMSG KV parsing.*

- **Tool Call #4:** `Read` — `cases/NITROBA/docs/shared_facts.md` → *Outcome: Prior facts ingested. MAC 00:17:f2:e2:c0:ce known for 192.168.15.4 (MacBook Obsidian). M010 already identified amy789smith in stream 1865 but did not resolve key role. Prior file m010_stream_1865_yahoo.txt confirmed on disk.*

- **Tool Call #5:** `shell` — `ls /Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/` → *Outcome: Confirmed m010_stream_1865_yahoo.txt and m011_stream1865_layer2.txt (empty) exist. 16 files listed. No re-derivation needed for prior M010 output.*

- **Tool Call #6:** `Read` — `cases/NITROBA/scratch/nitroba.pcap/m010_stream_1865_yahoo.txt` → *Outcome: M010 ASCII follow output read. Line 16 shows YMSG data in ASCII: `YMSG.....s.......Pk.1..amy789smith..38..604800..0..amy789smith..28..12740..27..057f280df74aeda1a8aada6a0f218871b5417eb3.png`. Suggested Key 1 = amy789smith but ASCII representation needed hex verification.*

- **Tool Call #7:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y "tcp.stream==1865" -T fields -e frame.number -e frame.time_utc -e eth.src -e eth.dst -e ip.src -e ip.dst 2>/dev/null | head -20` → *Outcome: Empty output. tshark `-T fields` with eth.src not working correctly for this stream/version combination. Strike 1 for this approach.*

- **Tool Call #8:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y "tcp.stream==1865" -x 2>/dev/null | grep -A 20 "YMSG" | head -50` → *Outcome: SUCCESS — Full hex dump of YMSG packet returned. Critical bytes confirmed: `31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80` = Key "1" → "amy789smith". Also confirmed Key 0, 38, 28, 27, 14, 29 present; Key 5 and Key 4 ABSENT. YMSG header: magic=YMSG, version=0x000f=15, service=0x00c2, session=0x00506bfb.*

- **Tool Call #9:** `shell` — `docker ps --format "{{.Names}}"` → *Outcome: Container name is `NITROBA` (not `sift-nitroba`). Required to fix tool calls 7/10.*

- **Tool Call #10:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -R "ip.dst==209.191.110.214 || ip.src==209.191.110.214" -T fields -e frame.number -e frame.time_utc -e eth.src -e eth.dst -e ip.src -e ip.dst 2>/dev/null | head -10` → *Outcome: Empty output. tshark `-R` filter also not working. Strike 1 for MAC via -R approach.*

- **Tool Call #11:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -R "http.host contains \"yahoo.com\" || frame contains \"amy789smith\"..." -T fields... > m011_yahoo_all_hits.txt` → *Outcome: Exit code 1, empty output. tshark `-R` filter incompatible with this version. Strike 2 — ceased capture-wide Yahoo search via this method. m011_yahoo_all_hits.txt created but empty.*

- **Tool Call #12:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y "tcp.stream==1865" 2>/dev/null | head -5` → *Outcome: SUCCESS — Default tshark output confirms stream 1865 frames: 90455 (SYN), 90466 (SYN/ACK), 90467 (ACK), 90468 (POST). Source IP 192.168.15.4 → 209.191.110.214 confirmed. Frame numbers identified for MAC lookup.*

- **Tool Call #13:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y "frame.number==90455" -V 2>/dev/null | grep -E "Source|Destination|Ethernet" | head -10` → *Outcome: SUCCESS — CRITICAL: "Ethernet II, Src: Apple_e2:c0:ce (00:17:f2:e2:c0:ce), Dst: HonHaiPr_2e:4f:60 (00:1d:d9:2e:4f:60)". Source MAC confirmed as 00:17:f2:e2:c0:ce (Apple). BUDGET LIMIT REACHED. Stopped forensics.*

*(Tool calls #14 onward: final reporting writes — excluded from budget tally per SOP)*

## 3. Key Evidence Summary

### YMSG Hex Bytes (from tool call #8):
```
31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80
^  ^^^^^  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^  ^^^^^
|  delim  "amy789smith"                     delim
key "1"
```

### Full YMSG KV Pairs parsed:
| Key   | Hex Bytes | YMSG Role               | Value                                        |
|-------|-----------|-------------------------|----------------------------------------------|
| 1     | 31        | LOGGED-IN USER OWN ID   | amy789smith                                  |
| 38    | 33 38     | Session timeout         | 604800                                       |
| 0     | 30        | (protocol field)        | amy789smith                                  |
| 28    | 32 38     | File size (bytes)       | 12740                                        |
| 27    | 32 37     | Filename                | 057f280df74aeda1a8aada6a0f218871b5417eb3.png |
| 14    | 31 34     | (empty)                 | (empty)                                      |
| 29    | 32 39     | File type               | PNG (+ binary payload)                       |
| **5** | **35**    | **Remote peer ID**      | **NOT PRESENT**                              |
| **4** | **34**    | **Inbound sender ID**   | **NOT PRESENT**                              |

### MAC Verification (from tool call #13):
```
Ethernet II, Src: Apple_e2:c0:ce (00:17:f2:e2:c0:ce), Dst: HonHaiPr_2e:4f:60 (00:1d:d9:2e:4f:60)
```
- Frame: 90455 (TCP SYN, first frame of stream 1865)
- Source MAC: 00:17:f2:e2:c0:ce — CONFIRMED (Apple OUI)
- Destination MAC: 00:1d:d9:2e:4f:60 (Kenny's Wi-Fi router LAN interface)

## 4. Final Budget Tally
- Orientation: 4 tool calls (#1-4)
- Execution: 9 tool calls (#5-13)
- **Total forensic tool calls: 13** (well within 15 self-termination limit)
- Reporting writes excluded per SOP
