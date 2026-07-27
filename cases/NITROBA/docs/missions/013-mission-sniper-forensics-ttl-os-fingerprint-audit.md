# Forensic Audit Trail: Mission 013 — OS Fingerprinting via TTL / TCP Stack

## 1. Initial Prompt & Parameters

**Mission:** OS Fingerprinting via TTL / TCP Stack — UA-Independent Environment Separation  
**Target Agent:** sniper-forensics  
**Evidence:** `/case/images/nitroba.pcap` in SIFT container `NITROBA`. Outputs to `/scratch/nitroba.pcap/`.  
**Key host:** 192.168.15.4  
**Budget:** Orientation=4, Execution=12, Reporting=4. Self-terminate at tool call 16.  
**Fail-Fast:** Two-strike rule. Batch tshark commands.

## 2. Chronological Tool Execution Log

- **Tool Call #1:** `skill` with `{"name": "delegating-mission-cards-sop"}` → *Loaded SOP for mission card handling and audit trail requirements.*

- **Tool Call #2:** `skill` with `{"name": "shared-facts-sop"}` → *Loaded SOP for shared facts ingestion and update procedure.*

- **Tool Call #3:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/missions/013-mission-sniper-forensics-ttl-os-fingerprint.md"}` → *Read full mission card (60 lines). Budget and ROE confirmed: 4/12/4 tool calls. Six anchor frames identified. Control frames 32229 and 22757 must validate for method to be sound.*

- **Tool Call #4:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/shared_facts.md"}` → *Read shared facts (169 lines). Key context: 192.168.15.4 is MacBook Obsidian running Windows XP VM via VMware NAT (vmnet8 at 192.168.194.1). amy789smith classified as VM in M010/M012. Hostile emails confirmed from this host.*

- **Tool Call #5:** `shell` with `{"command": "docker ps --format \"{{.Names}}\" | head -5"}` → *Outcome: Container name is `NITROBA`. Useful — confirmed container running.*

- **Tool Call #6:** `shell` with `{"command": "docker exec NITROBA bash -c \"mkdir -p /scratch/nitroba.pcap && echo '=== TTL HISTOGRAM ===' > /scratch/nitroba.pcap/m013_ttl_histogram.txt && tshark -r /case/images/nitroba.pcap -q -Y 'ip.src==192.168.15.4' -T fields -e ip.ttl 2>/dev/null | sort | uniq -c | sort -rn >> /scratch/nitroba.pcap/m013_ttl_histogram.txt && echo '' >> /scratch/nitroba.pcap/m013_ttl_histogram.txt && echo 'Done.' >> /scratch/nitroba.pcap/m013_ttl_histogram.txt && cat /scratch/nitroba.pcap/m013_ttl_histogram.txt\""}` → *Outcome: TTL histogram shows 33,392@63, 1,161@64, 1@126. NO bimodal 64/127 split. Critical finding: VMware NAT collapses both stacks to TTL 63 at capture point. Saved to `/scratch/nitroba.pcap/m013_ttl_histogram.txt`.*

- **Tool Call #7:** `shell` with `{"command": "docker exec NITROBA bash -c \"tshark -r /case/images/nitroba.pcap -q -Y 'frame.number in {80614,83601,77508,32229,90504,22757}' -T fields -e frame.number -e frame.time -e ip.src -e ip.ttl -e ip.id -e tcp.srcport -e http.user_agent 2>/dev/null\" > /Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/m013_anchor_frames_ttl.txt && cat /Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/m013_anchor_frames_ttl.txt"}` → *Outcome: ALL 6 anchor frames show TTL 63 — including both Mac controls (22757, 32229) AND VM frames (77508, 80614, 83601) AND disputed frame 90504. TTL method FAILS validation. File saved locally.*

- **Tool Call #8:** `shell` with `{"command": "docker exec NITROBA bash -c \"echo '=== SYN FINGERPRINTS from 192.168.15.4 ===' > /scratch/nitroba.pcap/m013_syn_fingerprints.txt && tshark -r /case/images/nitroba.pcap -q -Y 'tcp.flags.syn==1 && tcp.flags.ack==0 && ip.src==192.168.15.4' -T fields -e frame.number -e ip.ttl -e tcp.window_size_value -e tcp.options.mss_val -e tcp.options.timestamp.tsval -e tcp.option_kind 2>/dev/null >> /scratch/nitroba.pcap/m013_syn_fingerprints.txt && ... (windows summary and no-timestamp filter) ...\""}` → *Outcome: All SYN packets from 192.168.15.4 are at TTL 63. Two distinct TCP option profiles: (1) `2,1,3,1,1,8,4,0` (MSS+NOP+WScale+NOP+NOP+TS+SACK+EOL) = Mac OS X style with timestamps; (2) `2,4,0` (MSS+SACK+EOL) = Windows-style no-timestamps. Saved to `/scratch/nitroba.pcap/m013_syn_fingerprints.txt`.*

- **Tool Call #9:** `shell` with `{"command": "docker exec NITROBA bash -c \"echo '=== UA vs TTL cross-reference from 192.168.15.4 ===' > /scratch/nitroba.pcap/m013_ua_vs_ttl.txt && tshark -r /case/images/nitroba.pcap -q -Y 'http.user_agent && ip.src==192.168.15.4' -T fields -e ip.ttl -e http.user_agent 2>/dev/null | sort | uniq -c | sort -rn >> /scratch/nitroba.pcap/m013_ua_vs_ttl.txt && cat /scratch/nitroba.pcap/m013_ua_vs_ttl.txt\""}` → *Outcome: ALL 15 unique User-Agent strings appear at TTL 63 only. Firefox Mac (2463), Safari Mac (632), MSIE 6.0 (475), iTunes (468), Safari older (333), MSIE 5.5 (3), Adium (2), Firefox WinNT (2), etc. No UA distinguishable by TTL. Saved to `/scratch/nitroba.pcap/m013_ua_vs_ttl.txt`.*

- **Tool Call #10:** `shell` with `{"command": "docker exec NITROBA bash -c \"(SYN option summary + no-timestamp filter listing)\""}` → *Outcome: Window size is the cleanest differentiator: Mac connections consistently use initial window=65535; identified frames with options `2,4,0` span streams 1054/1055/1087/1299/1301/1700 (third unidentified class). Full SYN listing appended to m013_syn_fingerprints.txt.*

- **Tool Call #11:** `shell` with `{"command": "docker exec NITROBA bash -c \"(anchor stream stream-number lookup + SYN for streams 1631,1701,1601,624,1865,468)\""}` → *Outcome: Critical bimodal split confirmed. Stream→SYN window: 468(Mac/Computrace)=65535, 624(Mac/Facebook)=65535, 1601(VM/Google)=64240, 1631(VM/HostilePOST1)=64240, 1701(VM/HostilePOST2)=64240, 1865(Yahoo/amy789smith)=65535. Frame 90504/stream 1865 = MAC-SIDE. Saved to `/scratch/nitroba.pcap/m013_anchor_syns.txt`.*

---
*Budget tally at close of forensics: 11 tool calls (4 orientation + 7 execution including container check). Reporting calls (mission card patch, shared_facts patch, this audit write) excluded per SOP recursive audit exclusion rule.*

## 3. Key Commands (Copy-Pasteable)

```bash
# TTL Histogram
docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'ip.src==192.168.15.4' -T fields -e ip.ttl 2>/dev/null | sort | uniq -c | sort -rn

# Anchor Frame Classification
docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'frame.number in {80614,83601,77508,32229,90504,22757}' -T fields -e frame.number -e frame.time -e ip.src -e ip.ttl -e ip.id -e tcp.srcport -e http.user_agent 2>/dev/null

# All SYN packets from host
docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'tcp.flags.syn==1 && tcp.flags.ack==0 && ip.src==192.168.15.4' -T fields -e frame.number -e ip.ttl -e tcp.window_size_value -e tcp.options.mss_val -e tcp.options.timestamp.tsval -e tcp.option_kind 2>/dev/null

# SYNs without TCP timestamps (Windows-style)
docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'tcp.flags.syn==1 && tcp.flags.ack==0 && ip.src==192.168.15.4 && !tcp.options.timestamp' -T fields -e frame.number -e ip.ttl -e tcp.window_size_value -e tcp.options.mss_val -e tcp.option_kind -e tcp.stream 2>/dev/null

# UA vs TTL cross-reference
docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'http.user_agent && ip.src==192.168.15.4' -T fields -e ip.ttl -e http.user_agent 2>/dev/null | sort | uniq -c | sort -rn

# Anchor stream SYN lookup (stream numbers and their SYN characteristics)
docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'frame.number in {80614,83601,77508,32229,90504,22757}' -T fields -e frame.number -e tcp.stream -e ip.ttl -e tcp.window_size_value -e http.user_agent 2>/dev/null

docker exec NITROBA tshark -r /case/images/nitroba.pcap -q -Y 'tcp.flags.syn==1 && tcp.flags.ack==0 && tcp.stream in {1631,1701,1601,624,1865,468}' -T fields -e frame.number -e tcp.stream -e ip.ttl -e tcp.window_size_value -e tcp.options.mss_val -e tcp.options.timestamp.tsval -e tcp.option_kind -e ip.src 2>/dev/null
```

## 4. Output Files

- `/scratch/nitroba.pcap/m013_ttl_histogram.txt` — TTL frequency distribution for 192.168.15.4
- `/scratch/nitroba.pcap/m013_anchor_frames_ttl.txt` — Six anchor frames with TTL, IP.ID, UA
- `/scratch/nitroba.pcap/m013_syn_fingerprints.txt` — All TCP SYNs from 192.168.15.4 with option profiles
- `/scratch/nitroba.pcap/m013_anchor_syns.txt` — SYN characteristics for the 6 anchor streams
- `/scratch/nitroba.pcap/m013_ua_vs_ttl.txt` — Full UA×TTL cross-reference
