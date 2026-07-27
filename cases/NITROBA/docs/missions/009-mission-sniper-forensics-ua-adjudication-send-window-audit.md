# Forensic Audit Trail: Mission 009 — Per-Frame UA Adjudication + Send-Window HTTP Narrative

## 1. Initial Prompt & Parameters

**Mission:** cases/NITROBA/docs/missions/009-mission-sniper-forensics-ua-adjudication-send-window.md
**Target Agent:** sniper-forensics
**Budget:** Orientation 4 / Execution 10 / Reporting 4 = 18 total; self-terminate at tool call 15
**Objective:** Adjudicate M006 vs M007 UA conflict (Firefox/2.0.0.16 Mac vs MSIE 6.0 Windows XP) for hostile frames 80614 and 83601; produce send-window HTTP narrative.
**Evidence:** /case/images/nitroba.pcap (SIFT container: NITROBA)
**Output dir:** /scratch/nitroba.pcap/ (host: cases/NITROBA/scratch/nitroba.pcap/)
**Fail-fast:** Two-strike rule per command; do not explore outside named frames/streams/time window.

---

## 2. Chronological Tool Execution Log

**Tool Call #1:** `skill` with `{"name": "delegating-mission-cards-sop"}` → *Outcome: Loaded SOP rules for mission cards, budget tracking, checkpointing, audit trail requirements.*

**Tool Call #2:** `skill` with `{"name": "shared-facts-sop"}` → *Outcome: Loaded SOP for shared facts maintenance; confirmed to read shared_facts.md before any forensic work.*

**Tool Call #3:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/missions/009-mission-sniper-forensics-ua-adjudication-send-window.md"}` → *Outcome: Mission card read. Budget confirmed: Orientation 4, Execution 10, Reporting 4. Frames 80614/83601, streams 1601/1602 identified as targets.*

**Tool Call #4:** `Read` with `{"file_path": "/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/shared_facts.md"}` → *Outcome: Ingested all prior case facts. M007 had already asserted IE6 UA on hostile streams; M006 had asserted Firefox from host-wide frequency counts. No re-derivation of device map, hostnames, or email content needed.*

**Tool Call #5:** `shell` with `{"command": "docker ps --format \"{{.Names}}\\t{{.Status}}\" | grep -i sift", "description": "Check SIFT container is running"}` → *Outcome: No output (grep returned exit 1 — container name does not contain 'sift'). Container status unknown.*

**Tool Call #6:** `shell` with `{"command": "docker ps --format \"{{.Names}}\\t{{.Status}}\"", "description": "List all running containers"}` → *Outcome: Container named `NITROBA` is running (Up 52 minutes). Confirmed container name for subsequent exec calls.*

**Tool Call #7:** `shell` with batched tshark commands for Tasks 1 and 2:
```bash
docker exec NITROBA bash -c '
mkdir -p /scratch/nitroba.pcap

tshark -r /case/images/nitroba.pcap \
  -Y "frame.number == 80614 || frame.number == 83601" \
  -T fields \
  -e frame.number -e frame.time_epoch -e ip.src -e eth.src -e tcp.stream \
  -e http.host -e http.request.uri -e http.user_agent \
  -E header=y \
  > /scratch/nitroba.pcap/m009_hostile_frame_ua.txt 2>&1

tshark -r /case/images/nitroba.pcap \
  -Y "(tcp.stream == 1601 || tcp.stream == 1602) && http.request" \
  -T fields \
  -e frame.number -e frame.time_epoch -e ip.src -e eth.src -e tcp.stream \
  -e http.host -e http.request.uri -e http.user_agent \
  -E header=y \
  > /scratch/nitroba.pcap/m009_identity_stream_ua.txt 2>&1
'
```
*Outcome: SMOKING GUN. Frame 80614: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` on stream 1631 → sendanonymousemail.net. Frame 83601: same UA on stream 1701 → willselfdestruct.com. Identity streams 1601/1602: all 13 HTTP requests carry identical IE6 UA including the jcoachj@gmail.com Google Calendar session.*

**Tool Call #8:** `shell` with batched tshark commands for Tasks 3 and 4:
```bash
docker exec NITROBA bash -c '
tshark -r /case/images/nitroba.pcap \
  -Y "ip.src==192.168.15.4 && http.request && frame.time >= \"Jul 22, 2008 05:55:00\" && frame.time <= \"Jul 22, 2008 06:10:00\"" \
  -T fields \
  -e frame.number -e frame.time -e http.host -e http.request.uri -e http.user_agent \
  -E header=y \
  > /scratch/nitroba.pcap/m009_send_window_requests.txt 2>&1

tshark -r /case/images/nitroba.pcap \
  -Y "ip.src==192.168.15.4 && http.request && frame.time >= \"Jul 22, 2008 05:55:00\" && frame.time <= \"Jul 22, 2008 06:10:00\"" \
  -T fields -e http.user_agent \
  2>/dev/null | sort | uniq -c | sort -rn \
  > /scratch/nitroba.pcap/m009_send_window_ua_counts.txt
'
```
*Outcome: 1,466 lines in send_window_requests.txt (includes header + warning = 1,464 actual HTTP requests). UA counts: Firefox/2.0.0.16=922, MSIE 6.0=475, iTunes=25, Safari=23, Windows-Update-Agent=9, other=10. Firefox dominates by count but is exclusively eBay/shopping traffic. IE6 handles Gmail+search+hostile sends. Full narrative: 05:55 eBay browsing (Firefox/Mac) → 05:56 WinUpdate (IE6/VM) → 06:01 Gmail+GCal jcoachj (IE6/VM) → 06:01:48 Google search "send anonymous mail" (IE6/VM) → 06:02:57 hostile POST 1 frame 80614 (IE6/VM) → 06:04:24 hostile POST 2 frame 83601 (IE6/VM) → 06:09+ eBay/iTunes/Adium/Yahoo (Firefox+iTunes/Mac).*

**Tool Call #9:** `shell` with `{"command": "docker exec NITROBA bash -c 'wc -l /scratch/nitroba.pcap/m009_send_window_requests.txt && echo \"---\" && grep -c \"MSIE 6.0\" /scratch/nitroba.pcap/m009_send_window_requests.txt && grep -c \"Firefox/2.0.0.16\" /scratch/nitroba.pcap/m009_send_window_requests.txt'"}` → *Outcome: 1466 lines total; 475 MSIE 6.0 requests; 922 Firefox/2.0.0.16 requests. Confirmed UA split.*

*Budget closed at 9 active tool calls. Reporting calls (patch×3, write×1) excluded per SOP.*

---

## 3. Key Evidence Summary

| Frame | Time (UTC) | Stream | Host | URI | User-Agent |
|-------|-----------|--------|------|-----|------------|
| 80614 | 06:02:57Z | 1631 | www.sendanonymousemail.net | /send.php | Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) |
| 83601 | 06:04:24Z | 1701 | www.willselfdestruct.com | /secure/submit | Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) |
| 77508 | 06:01:04Z | 1601 | www.google.com | /calendar/render?...gausr=jcoachj%40gmail.com | Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) |

### Send-Window UA Counts (05:55–06:10 UTC, 192.168.15.4)
| Count | User-Agent | Role |
|-------|-----------|------|
| 922 | Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.16) Gecko/20080702 Firefox/2.0.0.16 | Mac OS X host — eBay/shopping browsing ONLY |
| 475 | Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) | Windows XP VM — Gmail, Google search, BOTH hostile email POSTs |
| 23 | iTunes/7.7 (Macintosh; U; Intel Mac OS X 10.5.4) | Mac iTunes Store |
| 23 | Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/525.20.1 Safari/3.1.2 | Mac Safari |
| 9 | Windows-Update-Agent | XP VM Windows Update |
| 2 | iTunes/7.7 (Macintosh; N; Intel) | Mac iTunes |
| 2 | Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1 | XP VM Firefox 3.0.1 (minor) |
| 2 | Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.7.5) | Mac legacy browser (weather.com) |
| 2 | Mozilla/4.0 (compatible; MSIE 5.5) | Yahoo Messenger / address.yahoo.com |
| 2 | CFNetwork/330.4 | Mac system framework |
| 1 | Adium/1.2.7 (Mac OS X) Sparkle/1.1 | Adium IM update check |
| 1 | ee://aol/http | AOL client |

---

## 4. Verdict

**`Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` issued both frame 80614 and frame 83601 — MSIE 6.0 running in a Windows XP VM inside the Apple MacBook1,1 "Obsidian" belonging to Johnny Coach.**

**Mission 007 was correct. Mission 006's Firefox/2.0.0.16 claim was an error arising from host-wide UA frequency counting — Firefox dominated the session in request volume (922 vs 475) because eBay/auction page loads generate hundreds of image/resource requests per page view, but the Firefox browser ran exclusively on the Mac OS X host and never touched the anonymous mailer or Google Calendar sessions.**

---

## 5. Output Files Written (SIFT container → host path)
- `/scratch/nitroba.pcap/m009_hostile_frame_ua.txt` → `cases/NITROBA/scratch/nitroba.pcap/m009_hostile_frame_ua.txt`
- `/scratch/nitroba.pcap/m009_identity_stream_ua.txt` → `cases/NITROBA/scratch/nitroba.pcap/m009_identity_stream_ua.txt`
- `/scratch/nitroba.pcap/m009_send_window_requests.txt` → `cases/NITROBA/scratch/nitroba.pcap/m009_send_window_requests.txt`
- `/scratch/nitroba.pcap/m009_send_window_ua_counts.txt` → `cases/NITROBA/scratch/nitroba.pcap/m009_send_window_ua_counts.txt`
