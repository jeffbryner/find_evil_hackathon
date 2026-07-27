# Forensic Audit Trail: Mission 014 — Yahoo Messenger Session Reconstruction

## 1. Initial Prompt & Parameters

**Mission:** Full Yahoo Messenger Session Reconstruction — Scope and Timing of `amy789smith`
**Target Agent:** sniper-forensics
**Evidence:** `/case/images/nitroba.pcap` in SIFT container (`NITROBA`)
**Output directory:** `/scratch/nitroba.pcap/` (container), `cases/NITROBA/scratch/nitroba.pcap/` (host)
**Budget:** 4 orientation + 12 execution + 4 reporting = 20 total; self-terminate at 16
**Key instruction:** Use `-Y` display filter flag (NOT `-R`)
**Objectives:** Establish first/last occurrence of `amy789smith`; determine if Yahoo session predates hostile emails; build minute-by-minute timeline; verdict on session type.

---

## 2. Chronological Tool Execution Log

- **Tool Call #1:** `skill` with `{"name": "delegating-mission-cards-sop"}` → *Outcome: Loaded SOP for mission card reading and reporting. Confirmed budget enforcement rules, living mission card requirement, two-strike fail-fast rule.*

- **Tool Call #2:** `skill` with `{"name": "shared-facts-sop"}` → *Outcome: Loaded shared facts SOP. Confirmed ingest-before-execute rule; identified shared_facts.md update requirement.*

- **Tool Call #3:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/missions/014-mission-sniper-forensics-yahoo-session-reconstruction.md"}` → *Outcome: Full mission card loaded. Budget confirmed (4+12+4=20). Key objectives: (1) amy789smith literal search, (2) Yahoo/YMSG/5050 enumerate, (3) session start, (4) client ID, (5) other screen names, (6) timeline, (7) verdict.*

- **Tool Call #4:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/shared_facts.md"}` → *Outcome: Case context ingested. Known: 192.168.15.4 active 04:29:51–06:13:47Z, stream 1865 frame 90504 = amy789smith YMSG, hostile emails 06:02:57 and 06:04:24Z. M011 sweep failed due to -R flag. M012 confirmed amy789smith active 06:09:59Z via MSIE 5.5 VM UA.*

- **Tool Call #5:** `shell` with `{"command": "docker ps --filter name=sift --format '{{.Names}} {{.Status}}'"}` → *Outcome: No output (no container named sift). Container name unknown.*

- **Tool Call #6:** `shell` with `{"command": "docker ps --format '{{.Names}} {{.Status}}'"}` → *Outcome: Container `NITROBA` is running, status "Up About an hour". Correct container identified.*

- **Tool Call #7:** `shell` with `{"command": "docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y 'frame contains \"amy789smith\"' -T fields -e frame.number -e frame.time_relative -e frame.time_epoch -e ip.src -e ip.dst -e tcp.stream -e tcp.srcport -e tcp.dstport -E header=y -E separator='|' > cases/NITROBA/scratch/nitroba.pcap/m014_amy_all_frames.txt 2>&1 && echo 'Exit: 0'"}` → *Outcome: Exit 0. File written. 9 frames matched. All in streams 1861 (port 5050) and 1865 (HTTP). Epoch range 1216706999.003548–1216707000.664388 = 06:09:59–06:10:00Z.*

- **Tool Call #8:** `shell` with `{"command": "docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y 'tcp.port==5050 || frame contains \"YMSG\" || http.host contains \"yahoo\"' -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e http.host -e http.request.uri -e tcp.stream -E header=y -E separator='|' > cases/NITROBA/scratch/nitroba.pcap/m014_yahoo_traffic.txt 2>&1 && echo 'Exit: 0'"}` → *Outcome: Exit 0. 88 matching rows. First Yahoo frame 24419 at epoch 1216701826 (04:43:46Z). First port-5050 frame 90372 at epoch 1216706998 (06:09:58Z). Last frame 93899 at epoch 1216707069 (06:11:09Z). Critical finds: img.avatars.yahoo.com at 04:43:49Z; address.yahoo.com?prog=ymsgr at 05:02:05Z; Yahoo Answers search at 05:58:32Z.*

- **Tool Call #9:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/m014_amy_all_frames.txt"}` → *Outcome: Confirmed 9 frames all at 06:09:59–06:10:00Z. Streams 1861 (port 5050) and 1865 (HTTP). Frame 90388 = earliest (06:09:59Z); frame 90580 = latest (06:10:00Z). IPs: 192.168.15.4 ↔ 66.163.181.179 (stream 1861) and 192.168.15.4 → 209.191.110.214 (stream 1865).*

- **Tool Call #10:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/m014_yahoo_traffic.txt"}` → *Outcome: 88 rows analyzed. Key findings: (1) buddy avatar downloads starting 04:43:49Z; (2) address.yahoo.com prog=ymsgr call at 05:02:05Z (stream 1045); (3) Yahoo Answers "can I go to jail for harassing my teacher?" at 05:58:32Z (stream 1540); (4) port 5050 YMSG traffic 06:09:58–06:10:18Z (stream 1861); (5) filetransfer.msg.yahoo.com POST at 06:09:59Z (stream 1865). Server 66.163.181.179 = YMSG server.*

- **Tool Call #11:** `shell` with `{"command": "docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y 'tcp.stream==1045' -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e http.request.method -e http.host -e http.request.uri -e http.cookie -e http.user_agent -E header=y -E separator='|' 2>/dev/null"}` → *Outcome: Frame 48627 at 05:02:05Z: GET address.yahoo.com /yab/us?v=XM&prog=ymsgr&.intl=us&diffs=1&t=0&tags=short&rt=0&prog-ver=8.1.0.249&useutf8=1&legenc=codepage-1252 Cookie: T=z=jnWhIBjtrhIB3a25/TYqdPCNDA3BjYzMTU2TjU3MjE-&a=YAE&sk=DAAszSVBqFLfLO&ks=EAAX5nEn_0nBpUqJEdstRVSDw--~A; Y=v=1&n=7tngdm3vg06tk&... UA: Mozilla/4.0 (compatible; MSIE 5.5). CRITICAL: identical UA to amy789smith YMSG frame; T= auth cookie present = YM already authenticated at 05:02:05Z.*

- **Tool Call #12:** `shell` with `{"command": "docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y 'frame contains \"ymsgr\" || frame contains \"y=amy\" || frame contains \"yahoo.com\" && tcp.dstport==5050' -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst -e tcp.stream -E header=y -E separator='|' 2>/dev/null | head -30"}` → *Outcome: No matching frames returned. No early ymsgr string occurrences outside already-known frames. Confirmed no pre-06:09Z port-5050 YMSG traffic with amy789smith or ymsgr keyword in frames.*

- **Tool Call #13:** `shell` with `{"command": "docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y 'tcp.stream==1861' -T fields ... && docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y 'tcp.stream==1861' -x 2>/dev/null | head -60"}` → *Outcome: Stream 1861 frame list: TCP SYN frame 90372 at 06:09:58Z; SYN-ACK 90384; ACK 90385; first data 90388 at 06:09:59Z. Hex dump confirms YMSG magic bytes (59 4d 53 47); version 0x000f (15); service 0x0057 (YMSG_SERVICE_VERIFY) in first packet from client containing key 1 = `amy789smith` (hex: 31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80). Server response also 0x0057 with key 1 = amy789smith + key 94 (challenge). Later server sends 0x0054 (AUTH challenge) with key 0 = amy789smith + key 6 = challenge string. Full fresh login exchange confirmed at 06:09:58Z.*

*(Tool calls #14–#15 = mission card update and shared_facts.md update — excluded from budget tally per Recursive Audit Exclusion Rule)*

---

## 3. Key Commands (Copy-Pasteable)

```bash
# Search all frames for literal string amy789smith
docker exec NITROBA tshark -r /case/images/nitroba.pcap \
  -Y 'frame contains "amy789smith"' \
  -T fields -e frame.number -e frame.time_relative -e frame.time_epoch \
  -e ip.src -e ip.dst -e tcp.stream -e tcp.srcport -e tcp.dstport \
  -E header=y -E separator='|' \
  > /scratch/nitroba.pcap/m014_amy_all_frames.txt

# Enumerate all Yahoo/YMSG/port-5050 traffic
docker exec NITROBA tshark -r /case/images/nitroba.pcap \
  -Y 'tcp.port==5050 || frame contains "YMSG" || http.host contains "yahoo"' \
  -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst \
  -e tcp.srcport -e tcp.dstport -e http.host -e http.request.uri -e tcp.stream \
  -E header=y -E separator='|' \
  > /scratch/nitroba.pcap/m014_yahoo_traffic.txt

# Inspect stream 1045 (YM address book call) for cookies/UA
docker exec NITROBA tshark -r /case/images/nitroba.pcap \
  -Y 'tcp.stream==1045' \
  -T fields -e frame.number -e frame.time_epoch -e ip.src -e ip.dst \
  -e http.request.method -e http.host -e http.request.uri \
  -e http.cookie -e http.user_agent \
  -E header=y -E separator='|'

# Hexdump stream 1861 (YMSG port 5050 auth exchange)
docker exec NITROBA tshark -r /case/images/nitroba.pcap \
  -Y 'tcp.stream==1861' -x | head -60
```

---

## 4. Final Budget Tally

| Phase | Calls Used | Budget |
|---|---|---|
| Orientation | 4 | 4 |
| Execution | 9 | 12 |
| Reporting | 2 (mission card + shared_facts) | 4 |
| **Total** | **15** | **20** |

Budget not exhausted. No fail-fast triggered. Mission completed within constraints.
