# Mission: Per-Frame User-Agent Adjudication + Complete Send-Window HTTP Narrative
**Target Agent:** sniper-forensics

## Purpose
Settle a contradiction between two earlier missions and produce the definitive minute-by-minute browsing narrative of the attack window. Mission 006 asserted the sending browser was **Firefox/2.0.0.16 (Mac)**; Mission 007 reassembled the streams and found **`Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`** on every hostile and identity stream. The case lead has assessed that M006's claim was an inference from host-wide User-Agent *frequency counts* (Firefox was simply the most-used UA on that host overall) rather than from the hostile streams themselves. Your job is to prove which is correct **per frame**, and to lay out exactly what the operator did in the ten minutes surrounding the sends.

This matters because the report will state, as fact, which browser on which OS composed a threatening message.

## Background
Case NITROBA (2008 harassment investigation, network-only evidence).
- Evidence: `/case/images/nitroba.pcap` inside SIFT (host: `cases/NITROBA/images/nitroba.pcap`), 94,410 packets, 2008-07-22 01:51:07–06:13:47 UTC.
- Attacker host: **192.168.15.4**, MAC `00:17:f2:e2:c0:ce`, Apple MacBook1,1 "Obsidian" (S/N 4H6242CSVMN) running a VMware Windows XP VM (`vmnet8` = 192.168.194.1). Both the Mac host OS and the XP VM share the single IP via NAT — so **both UAs legitimately appear from 192.168.15.4**, and only per-frame inspection can say which browser sent a given request.
- Frames of record: **80614** = POST /send.php (sendanonymousemail.net, 06:02:57Z, stream 1631); **83601** = POST /secure/submit (willselfdestruct.com, 06:04:24Z, stream 1701). Identity streams: **1601**, **1602** (Google, `jcoachj@gmail.com`, 06:01:08Z).
- Write ALL output to `/scratch/nitroba.pcap/` (host: `cases/NITROBA/scratch/nitroba.pcap/`). Do NOT modify the pcap.

## Budget & Rules of Engagement
- **Orientation Budget:** 4 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 4 tool calls
- **Proactive Self-Termination:** At tool call 15 (~80% of the 18-call total), stop active forensics and spend remaining calls writing partial findings and exiting cleanly.
- **Fail-Fast Condition:** Two-strike rule per command — if a tshark invocation errors twice, record the failure and move to the next checklist item. Do NOT explore outside the named frames/streams/time window. Do NOT re-derive facts already in `shared_facts.md`.
- Batch multiple tshark commands into single shell calls wherever possible (this saved significant budget in M007).

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` and execute the `shared-facts-sop` skill; execute the `delegating-mission-cards-sop` skill.
- [x] **Per-frame UA (the adjudication):** tshark on frames 80614 and 83601 → saved to `/scratch/nitroba.pcap/m009_hostile_frame_ua.txt`. VERDICT: both frames carry `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`.
- [x] Identity streams 1601/1602: all 13 HTTP requests carry `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` → saved to `/scratch/nitroba.pcap/m009_identity_stream_ua.txt`.
- [x] **Send-window narrative:** 1,464 HTTP requests from 192.168.15.4 in 05:55–06:10 UTC extracted → `/scratch/nitroba.pcap/m009_send_window_requests.txt`.
- [x] **UA split:** Firefox/2.0.0.16 = 922 requests (eBay/shopping browsing on Mac OS X host); MSIE 6.0/WinXP = 475 requests (Gmail→search→hostile send 1→hostile send 2, all in Windows XP VM) → `/scratch/nitroba.pcap/m009_send_window_ua_counts.txt`.
- [x] **Verdict:** `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` issued both frames 80614 and 83601; **M007 was correct, M006's Firefox claim was an inference from host-wide frequency, not per-frame evidence.**
- [x] `shared_facts.md` updated — UA entry corrected with per-frame confirmation and M006 refutation.
- [x] Mission card updated.
- [x] Audit trail written to `009-mission-sniper-forensics-ua-adjudication-send-window-audit.md`.

## Results & Post-Mortem
- **Approach:** Loaded skills and shared_facts.md first (no re-derivation). Ran four tshark commands batched into two shell calls against the SIFT container. Output files written to /scratch/nitroba.pcap/. All four tasks completed within execution budget.
- **Findings:**
  - **ADJUDICATION RESULT — M007 CORRECT, M006 REFUTED:** Per-frame tshark confirms `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` on both hostile frames and all identity stream requests.
  - **Frame 80614** (stream 1631, 06:02:57Z, POST /send.php → sendanonymousemail.net): UA = `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` from 192.168.15.4 / MAC 00:17:f2:e2:c0:ce.
  - **Frame 83601** (stream 1701, 06:04:24Z, POST /secure/submit → willselfdestruct.com): UA = `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` from same host.
  - **Identity streams 1601/1602** (Google Calendar, jcoachj@gmail.com): All 13 HTTP requests = `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`.
  - **M006 Firefox claim:** Firefox/2.0.0.16 (Mac Intel) IS present in the send window — 922 requests — but exclusively for Mac-side eBay/shopping/auction browsing. It appears at **zero** of the hostile or identity streams.
  - **Send-window narrative (05:55–06:10 UTC, 1,464 requests total):**
    - 05:55:12 — Mac Firefox browsing eBay (leather backpack shopping, toroleather.com auction listing)
    - 05:56:09 — Windows-Update-Agent requests from XP VM (9 total)
    - ~06:01:08 — IE6/XP VM: Google Calendar for jcoachj@gmail.com (streams 1601/1602); Google search for "send anonymous mail"
    - ~06:01:48 — IE6/XP VM: clicked search result → www.sendanonymousemail.net
    - 06:02:57 — IE6/XP VM: POST /send.php (hostile email 1, "Your class stinks") — **frame 80614**
    - 06:04:24 — IE6/XP VM: POST /secure/submit (hostile email 2, "you can't find us") — **frame 83601**
    - 06:09+ — Mac Firefox back to eBay browsing; iTunes 7.7 (Mac) store open; Adium IM update check; Yahoo Messenger file transfer
  - **UA Role Separation:** Firefox/2.0.0.16 = eBay/shopping (Mac host OS only); MSIE 6.0 = Gmail, Google search, hostile anonymizer sends (Windows XP VM only); Safari/3.1.2 = 23 requests; iTunes = 25 requests; Windows-Update-Agent = 9 requests.
- **Confidence Rating:** DEFINITIVE (5/5). Per-frame tshark output is a direct read of the raw pcap wire data. No inference. M006's Firefox claim arose from frequency counting at the host level, not stream-level inspection.
- **Budget Tally:** 9 active tool calls (4 orientation + 5 execution). Final reporting calls (patch ×3, write ×1) excluded per SOP.
- **NPS / Feedback:** Mission well-scoped. Batching tshark into 2 shell calls was effective. The dual-browser scenario (Mac Firefox + Windows XP VM IE6 sharing one NAT IP) is the source of confusion for M006 — a frequency count across all streams will show Firefox as dominant because eBay/auction browsing generates hundreds of image/resource requests per page, but the actual hostile POST operations were performed in the Windows XP VM using IE6. Future missions should always filter to the specific stream/frame rather than counting host-wide UAs.

## Discovered Leads (For Followup)
- **Lead:** Send-window shows `Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1` (2 requests) — a *different* Windows XP browser UA besides IE6 appeared in the window. Low priority but worth noting.
