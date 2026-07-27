# Forensic Audit Trail: Mission 007 — Validate Attribution Streams

## 1. Initial Prompt & Parameters

**Mission:** Reassemble TCP streams 1701, 1631, 1601, 1602, 468 from /case/images/nitroba.pcap (SIFT container; outputs to /scratch/nitroba.pcap/). Recover FULL hostile message texts, verify User-Agent/Cookie continuity between hostile send streams and jcoachj@gmail.com identity streams, and confirm Computrace device fingerprint (frame 22757) originates from 192.168.15.4 MAC 00:17:f2:e2:c0:ce.

**Budget:** 25 total (5 orientation / 15 execution / 5 reporting). Self-terminate at 20 calls.

**Output files required:**
- Mission card update: `007-mission-sniper-forensics-validate-attribution-streams.md`
- Shared facts update: `cases/NITROBA/docs/shared_facts.md`
- This audit file: `007-mission-sniper-forensics-validate-attribution-streams-audit.md`

**SIFT container:** NITROBA  
**PCAP path in container:** `/case/images/nitroba.pcap`  
**Scratch path in container:** `/scratch/nitroba.pcap/`  
**Scratch path on host:** `cases/NITROBA/scratch/nitroba.pcap/`

---

## 2. Chronological Tool Execution Log

**Tool Call #1:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/missions/007-mission-sniper-forensics-validate-attribution-streams.md`
→ *Outcome: Mission card loaded. Confirmed 5 streams to reassemble (1701, 1631, 1601, 1602, 468), frame 22757 to verify, outputs to /scratch/nitroba.pcap/.*

**Tool Call #2:** `skill` — `delegating-mission-cards-sop`
→ *Outcome: Loaded SOP for mission card checkpointing, audit trail requirements, two-strike rule, living mission card rule.*

**Tool Call #3:** `skill` — `shared-facts-sop`
→ *Outcome: Loaded SOP for reading/writing shared_facts.md, section headers, IOC tracking requirements.*

**Tool Call #4:** `skill` — `analyze-network-traffic`
→ *Outcome: Loaded tshark recipe reference including `follow,tcp,ascii,<stream_id>` syntax and container path mapping.*

**Tool Call #5:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/docs/shared_facts.md`
→ *Outcome: Ingested case context. Confirmed attacker is 192.168.15.4 / MAC 00:17:f2:e2:c0:ce. jcoachj@gmail.com identified in prior missions. Device fingerprint (MacBook1,1, Obsidian, S/N 4H6242CSVMN) noted. Five target streams pre-identified.*

**Tool Call #6:** `shell` — `docker ps --format "{{.Names}}\t{{.Status}}" | grep -i nitroba`
→ *Outcome: Container "NITROBA" confirmed running ("Up 31 minutes").*

**Tool Call #7:** `shell` — `docker exec NITROBA bash -c "mkdir -p /scratch/nitroba.pcap && tshark -r /case/images/nitroba.pcap -q -z follow,tcp,ascii,1701 > /scratch/nitroba.pcap/stream_1701_willselfdestruct.txt 2>&1 && echo 'STREAM_1701_DONE' && tshark -r /case/images/nitroba.pcap -q -z follow,tcp,ascii,1631 > /scratch/nitroba.pcap/stream_1631_sendanonymousemail.txt 2>&1 && echo 'STREAM_1631_DONE'"`
→ *Outcome: Both extractions succeeded. STREAM_1701_DONE and STREAM_1631_DONE printed. Files written to /scratch/nitroba.pcap/.*

**Tool Call #8:** `shell` — `docker exec NITROBA bash -c "tshark -r /case/images/nitroba.pcap -q -z follow,tcp,ascii,1601 > /scratch/nitroba.pcap/stream_1601_gmail.txt 2>&1 && echo 'STREAM_1601_DONE' && tshark -r /case/images/nitroba.pcap -q -z follow,tcp,ascii,1602 > /scratch/nitroba.pcap/stream_1602_gcal.txt 2>&1 && echo 'STREAM_1602_DONE' && tshark -r /case/images/nitroba.pcap -q -z follow,tcp,ascii,468 > /scratch/nitroba.pcap/stream_0468_computrace.txt 2>&1 && echo 'STREAM_0468_DONE'"`
→ *Outcome: All three extractions succeeded. STREAM_1601_DONE, STREAM_1602_DONE, STREAM_0468_DONE printed. Files written to /scratch/nitroba.pcap/.*

**Tool Call #9:** `shell` — `docker exec NITROBA tshark -r /case/images/nitroba.pcap -Y "frame.number==22757" -T fields -e frame.time -e eth.src -e ip.src -e ip.dst -e ip.proto 2>/dev/null`
→ *Outcome: Single line returned: `Jul 22, 2008 04:36:48.535629000 UTC  00:17:f2:e2:c0:ce  192.168.15.4  209.53.113.23  6` — CONFIRMED frame 22757 originates from MAC 00:17:f2:e2:c0:ce and IP 192.168.15.4.*

**Tool Call #10:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/stream_1701_willselfdestruct.txt`
→ *Outcome (SMOKING GUN): Stream 1701 confirmed POST /secure/submit to www.willselfdestruct.com from 192.168.15.4:36044. User-Agent: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`. POST body: `to=lilytuckrige@yahoo.com&from=&subject=you+can%27t+find+us&message=and+you+can%27t+hide+from+us.%0D%0A%0D%0AStop+teaching.%0D%0A%0D%0AStart+running.+`. Server returned HTTP 302 → /secure/success. EMAIL 2 CONFIRMED SENT.*

**Tool Call #11:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/stream_1631_sendanonymousemail.txt`
→ *Outcome (SMOKING GUN): Stream 1631 confirmed POST /send.php to www.sendanonymousemail.net from 192.168.15.4:35876. User-Agent: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` (IDENTICAL to stream 1701). Cookie: `PHPSESSID=762adba03236142ccec305f6a20aaffa`. POST body: `email=lilytuckrige@yahoo.com&sender=the_whole_world_is_watching@nitroba.org&subject=Your+class+stinks&message=Why+do+you+persist+in+teaching+a+boring+class%3F%0D%0A%0D%0AWe+don%27t+like+it.%0D%0A%0D%0AWe+don%27t+like+you.%0D%0A%0D%0A`. Server returned HTTP 200 OK + "Thank You Your message has been sent!" — EMAIL 1 CONFIRMED SENT. CAPTCHA image loaded AFTER send (for a second attempt, not a failure of the first).*

**Tool Call #12:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/stream_1601_gmail.txt`
→ *Outcome (IDENTITY CONFIRMATION): Stream 1601 confirmed GET /calendar/render?...&gausr=jcoachj%40gmail.com from 192.168.15.4:35796 at 06:01:08Z. User-Agent: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` (IDENTICAL to streams 1631/1701). Server Set-Cookie: `OL_SESSION=jcoachj@gmail.com-cal`. POST /calendar/load body emf field contains base64 encoding of jcoachj@gmail.com with calendar date ranges.*

**Tool Call #13:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/stream_0468_computrace.txt`
→ *Outcome (DEVICE FINGERPRINT): Stream 468 confirmed 192.168.15.4:32992 → 209.53.113.23:80 (search.namequery.com). UA: Safari/Mac OS X (Mac host OS, different from Windows XP VM UA). Stream contains XML payload with: ComputerMake=Apple, ComputerModel=MacBook1,1, ComputerSerial=4H6242CSVMN, ComputerName=Obsidian, HDDSerialNumber0=NW81T6325527, HDDSerialNumber1=K3376NB5022, NIC en1 MAC=0016cbbf89d6, NIC vmnet8 IP=192.168.194.1 (VMware NAT). Hostname "Obsidian" visible in plaintext at stream line 294.*

**Tool Call #14:** `Read` — `/Users/jeffbryner/development/find_evil_hackathon/cases/NITROBA/scratch/nitroba.pcap/stream_1602_gcal.txt` (lines 1-80)
→ *Outcome: Stream 1602 confirmed GET /calendar/... from 192.168.15.4:35798 at 06:01:08Z. User-Agent: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` (IDENTICAL). Cookie includes OL_SESSION=jcoachj@gmail.com-cal — same Google session as stream 1601. This is a companion CSS resource load for the same Google Calendar session.*

**Tool Call #15:** `patch` — Mission card checklist items checked and Results & Post-Mortem section filled.
→ *Outcome: Mission card updated with all findings, timelines, continuity verdict, device fingerprint details, and discovered leads.*

**Tool Call #16:** `patch` — `shared_facts.md` — appended `# Confirmed Exfiltrated/Accessed Data` (full message texts) and `# Attacker Attribution` (full attribution summary).
→ *Outcome: Both hostile email message texts fully documented; attacker profile (jcoachj@gmail.com / Johnny Coach / MacBook Obsidian) documented under new section.*

---

## 3. Budget Tally

| Phase | Calls Used | Calls Budgeted |
|---|---|---|
| Orientation | 5 | 5 |
| Execution | 9 | 15 |
| Reporting (excl. this file) | 3 | 5 |
| **Total (excl. audit write)** | **17** | **25** |

*Per delegating-mission-cards-sop: the final patch/write calls for the mission card results and this audit file are excluded from the budget tally and execution log.*

---

## 4. Key Evidence Summary

| Artifact | Finding |
|---|---|
| Stream 1701 POST body | `to=lilytuckrige@yahoo.com`, `subject=you can't find us`, `message=and you can't hide from us. Stop teaching. Start running.` |
| Stream 1701 server response | HTTP 302 → /secure/success — **SENT** |
| Stream 1631 POST body | `email=lilytuckrige@yahoo.com`, `sender=the_whole_world_is_watching@nitroba.org`, `subject=Your class stinks`, `message=Why do you persist in teaching a boring class? We don't like it. We don't like you.` |
| Stream 1631 server response | HTTP 200 OK + "Thank You Your message has been sent!" — **SENT** |
| Streams 1631/1701/1601/1602 UA | IDENTICAL: `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` |
| Streams 1601/1602 identity | `OL_SESSION=jcoachj@gmail.com-cal`; `gausr=jcoachj%40gmail.com` |
| All 4 streams source | 192.168.15.4, MAC 00:17:f2:e2:c0:ce |
| Frame 22757 | MAC 00:17:f2:e2:c0:ce / IP 192.168.15.4 → 209.53.113.23 at 04:36:48.535629Z |
| Stream 468 Computrace XML | MacBook1,1 / S/N 4H6242CSVMN / hostname Obsidian / HDD NW81T6325527 |
