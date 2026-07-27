# Mission: Identity ↔ User-Agent ↔ OS Correlation Matrix (The Decisive Analysis)
**Target Agent:** sniper-forensics

## Purpose
This is the mission that decides the case.

The attacker laptop (192.168.15.4) is a **shared machine**: at least three human identities appeared on it inside 80 minutes (`beth@bethr.org`, `jcoachj@gmail.com`, `amy789smith`), and two of them are on the CHEM109 suspect roster. Machine ownership therefore cannot identify the sender.

But we know something much sharper: the hostile emails were sent from **Internet Explorer 6 running inside a VMware Windows XP virtual machine** (`Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`), while the Mac host OS was simultaneously running Firefox/Safari/iTunes under different identities. The VM is a separate execution environment with its own cookie jar.

**The question to answer: across the ENTIRE capture, which human identities ever appear in traffic bearing the XP-VM IE6 User-Agent?**
- If **only `jcoachj@gmail.com`** ever appears inside the VM, then the person operating the VM — the person who sent the threats — is Johnny Coach, regardless of who else used the Mac side. Attribution holds.
- If **other identities** also appear inside the VM, the VM was shared too, and we cannot name a single sender on network evidence alone. That is a legitimate and important outcome.

**Follow the data. A negative result is a successful mission.**

## Background
Case NITROBA (2008 harassment, network-only evidence).
- Evidence: `/case/images/nitroba.pcap` in SIFT (host: `cases/NITROBA/images/nitroba.pcap`). Do NOT modify. Outputs to `/scratch/nitroba.pcap/`.
- Host: **192.168.15.4** / MAC `00:17:f2:e2:c0:ce`, online 04:29:51–06:13:47 UTC. VMware NAT (`vmnet8` 192.168.194.1) means the VM's traffic carries the host's IP and MAC — **the User-Agent is the only way to separate VM traffic from Mac traffic.**
- UA → environment mapping already established (M006/M009):
  - **XP VM:** `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` (475 reqs), `Windows-Update-Agent` (10), `Mozilla/5.0 (Windows; U; Windows NT 5.1...) Firefox/3.0.1` (2)
  - **Mac host:** `Firefox/2.0.0.16` (2,463), `Safari/525.20.1` (632), `iTunes/7.7` (468), `Apple-PubSub`, `Adium`, `CFNetwork`
- Known identity anchors: `jcoachj@gmail.com` (streams 1601/1602, 06:01:08); `beth@bethr.org` + FB uid `588141158` (stream 624, 04:50–04:52); `amy789smith` (stream 1865, 06:09:59); Flickr `89101607@N00`; `login.live.com` visits 05:57/05:59.
- Useful prior output already on disk: `m009_send_window_requests.txt`, `h3_user_agents.txt`.

## Budget & Rules of Engagement
- **Orientation Budget:** 4 tool calls
- **Execution Budget:** 12 tool calls
- **Reporting Budget:** 4 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of the 20-call total), stop forensics and write up partial findings cleanly.
- **Fail-Fast Condition:** Two-strike rule per command. Analyse ONLY host 192.168.15.4. Do NOT re-open the hostile email streams or the device fingerprint — both are settled. Batch tshark commands into single shell calls.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md`; execute the `shared-facts-sop` and `delegating-mission-cards-sop` skills.
- [x] **Extract the full request corpus for the host.** Used tshark on container NITROBA with VM UA filter — produced `m012_vm_only_requests.txt` (490 rows). Note: m012_all_requests.txt not separately produced; VM corpus extracted directly per known UA list.
- [x] **Isolate the VM.** 490 total VM-UA requests. Earliest: frame 48627 @ 05:02:05 UTC. Latest: frame 90504 @ 06:09:59 UTC. Output: `m012_vm_only_requests.txt`, `m012_vm_hosts.txt`.
- [x] **Hunt identities inside the VM.** Searched URI/cookie fields — confirmed `jcoachj@gmail.com` (frames 77508/78571/78575, gausr= param). `amy789smith` in POST body (MSIE 5.5 / YMSG, not URI). Windows Live login loaded twice (05:57, 05:59) — no credentials in GET URIs. Output: `m012_vm_identities.txt`.
- [x] **Do the mirror analysis for the Mac side.** beth@bethr.org (Facebook, 04:50-04:52, Firefox Mac) and Flickr 89101607@N00 (04:49, 04:51, 05:21, Firefox Mac). Output: `m012_mac_identities.txt`.
- [x] **Build the matrix.** See Results section below.
- [x] **VERDICT:** NO — jcoachj@gmail.com is NOT the only human identity in the VM.
- [x] Append confirmed facts to `cases/NITROBA/docs/shared_facts.md`.
- [x] Update this card's **Results & Post-Mortem**.
- [x] Write the chronological technical log to `012-mission-sniper-forensics-identity-ua-matrix-audit.md`.

## Results & Post-Mortem
- **Approach:** Loaded skills and shared facts. Checked existing scratch files to avoid re-derivation. Ran targeted tshark on SIFT container NITROBA to extract all requests from 192.168.15.4 with Windows/VM user-agents (WinNT 5.1, Windows-Update-Agent, MSIE 5.5). Searched URI/cookie fields for identity-bearing strings. Cross-referenced with prior mission outputs (M009, M010) for POST-body identities. Compiled the full matrix.

- **Findings:**

  **VM corpus:** 490 requests, 05:02:05–06:09:59 UTC, UA breakdown: MSIE 6.0/WinNT5.1 (475), Windows-Update-Agent (10), MSIE 5.5 (3), Firefox/3.0.1/WinNT5.1 (2).

  **Identity ↔ Environment Matrix:**

  | Identity | Environment | First Seen UTC | Last Seen UTC | Evidence Frame / Method |
  |---|---|---|---|---|
  | jcoachj@gmail.com | **VM** (MSIE 6.0/WinNT5.1) | 06:00:44 | 06:00:56 | Frame 77508/78571 — gausr= URI param, Google Calendar + Gmail |
  | amy789smith | **VM** (MSIE 5.5, Windows-only UA) | 06:09:59 | 06:09:59 | Frame 90504 — YMSG POST body to filetransfer.msg.yahoo.com (M010) |
  | (unknown) | **VM** (MSIE 6.0/WinNT5.1) | 05:57:24 | 05:59:21 | Frames 72156/75689 — Windows Live login page loaded; no credentials in GET URIs |
  | beth@bethr.org | **Mac** (Firefox/2.0.0.16) | 04:50:30 | 04:52:04 | Frame 32229 — email= URI param, Facebook precog.php |
  | 89101607@N00 | **Mac** (Firefox/2.0.0.16) | 04:49:57 | 05:21:18 | Frames 31901/33498/64503 — Flickr RSS feed |

  **VERDICT (literal answer):** **NO** — `jcoachj@gmail.com` is NOT the only human identity inside the Windows XP VM across the entire capture.

  `amy789smith` (Amy Smith, CHEM109 student) is also present in VM-side traffic: MSIE 5.5 POST to `filetransfer.msg.yahoo.com` at 06:09:59 UTC, 5m35s after the second hostile email. Additionally, Windows Live login page was loaded from the VM at 05:57 and 05:59 UTC with no credentials captured (unknown identity).

  **Attribution implication:** The VM was itself shared by at least two human identities (jcoachj and amy789smith). Network evidence alone cannot prove a single sender. The hostile emails were sent during the jcoachj@gmail.com session, which immediately preceded (within ~2 minutes) the sendanonymousemail.net POST, but Amy Smith's VM activity after the sends shows the device/VM was accessible to at least one other CHEM109 student.

- **Confidence Rating:** HIGH (95%) — jcoachj@gmail.com presence in VM during hostile sends is confirmed by direct URI evidence; amy789smith in VM is confirmed by M010 stream reassembly and MSIE 5.5 (Windows-only) UA; MSIE 5.5 exclusion from mission card's VM UA list was an oversight as the UA is Windows-only with no Mac equivalent.

- **Budget Tally:** ~16 tool calls used (orientation 4, execution 10, reporting 2 in progress).

- **NPS / Feedback:** Mission succeeded in delivering a definitive negative answer. The batched tshark approach was efficient. One wasted call (wrong container name on first attempt). The MSIE 5.5 UA was not in the mission card's VM UA list — recommended to clarify in future mission cards that ALL Windows-only UAs (no Mac platform string) should be treated as VM traffic.

## Discovered Leads (For Followup)
- **Lead 1:** Unknown Windows Live (Hotmail) identity — loaded login.live.com from VM at 05:57 and 05:59 UTC (MSIE 6.0/WinNT5.1). Login page loaded but no POST credentials visible in GET URIs. Possible third identity in VM — warrants stream reassembly of those TCP sessions to check for POST data.
- **Lead 2:** Amy Smith (`amy789smith`) VM activity at 06:09:59 UTC requires deeper investigation — what was the PNG file transferred? Who was the recipient? Spawn dedicated mission.
