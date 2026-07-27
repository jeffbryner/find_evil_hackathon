# Mission: Complete Windows XP VM Activity Profile — Everything the Attacker Did
**Target Agent:** sniper-forensics

## Purpose
Attribution is settled: the Windows XP VM on MacBook "Obsidian" held exactly one human identity (`jcoachj@gmail.com`) and issued the premeditation search, the Gmail session, and both threatening emails. What we do **not** yet have is the *complete* picture of that VM session — and two prior missions left specific gaps:
1. **M012's VM activity window (05:02:05–06:09:59) is now known to be WRONG.** It was built from User-Agent guessing and wrongly included Mac streams 1045 and 1865. The VM's true start and end times have never been established.
2. **M016 ran out of budget** after extracting 1,182 HTTP request lines for 05:50–06:02 into `m016_all_http_5950_0602.txt` without filtering them. The full pre-attack research trail is unknown — we have one search phrase, but there may be more.

Produce the definitive, stack-verified profile of the attacker's virtual machine session.

## Background
Case NITROBA (2008 harassment, network-only evidence).
- Evidence: `/case/images/nitroba.pcap` in SIFT (host: `cases/NITROBA/images/nitroba.pcap`). Do NOT modify. Outputs to `/scratch/nitroba.pcap/`. Use **`-Y`** for display filters (legacy `-R` fails).
- **The container may be stopped — start it before running tshark** (this cost M016 two calls).
- Host: **192.168.15.4** / MAC `00:17:f2:e2:c0:ce`. Runs Mac OS X 10.5 natively + a VMware Windows XP guest behind NAT; both share IP and MAC.
- **The reliable environment discriminator (M015, validated on 10 streams):**
  - **Windows XP VM** = client SYN `tcp.window_size_value == 64240` AND `tcp.options.wscale.shift == 0`
  - **Mac OS X host** = client SYN window `65535` with a non-zero wscale (1 or 3)
  - IP TTL is useless (VMware NAT normalises it; everything arrives at 63). **Do not use User-Agent to determine OS.**
- Known VM streams: 1540 (Yahoo Answers search), 1601/1602 (Gmail `jcoachj@gmail.com`), 1631 (threat #1), 1701 (threat #2). Known Mac streams: 468, 624, 1045, 1861, 1864, 1865.
- Already on disk and reusable: `m015_all_syn_fingerprints.txt` (all client SYNs with window/wscale), `m016_all_http_5950_0602.txt` (1,182 HTTP requests 05:50–06:02), `m009_send_window_requests.txt`.

## Budget & Rules of Engagement
- **Orientation Budget:** 4 tool calls
- **Execution Budget:** 12 tool calls
- **Reporting Budget:** 4 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of the 20-call total), stop forensics and write up partial findings cleanly.
- **Fail-Fast Condition:** Two-strike rule per command. Do NOT re-read the hostile message bodies, the Gmail contents, the Computrace XML, or the Yahoo Answers search — all settled and quoted. **Prefer reusing the existing `m015_*` and `m016_*` files over re-running expensive full-capture scans.**

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md`; execute the `shared-facts-sop` and `delegating-mission-cards-sop` skills.
- [x] **Enumerate every VM stream in the capture.** 147 unique VM streams (window=64240, wscale=0) extracted from m015_all_syn_fingerprints.txt → `m017_vm_streams.txt`.
- [x] **Establish the VM's true active window.** FIRST: stream 1095, frame 51957, 2008-07-22T05:41:26Z. LAST: stream 1727, frame 84644, 2008-07-22T06:05:10Z. M012's "05:02:05" figure was wrong (built from UA guessing that included Mac streams). VM was active 21m31s before first hostile email at 06:02:57Z.
- [x] **Profile all VM HTTP activity.** 480 HTTP requests across 63 distinct hosts → `m017_vm_http_requests.txt`, `m017_vm_hosts.txt`.
- [x] **Extract the complete search/research trail.** 4 attacker search queries found → `m017_vm_search_trail.txt`.
- [x] **Identity re-sweep.** `jcoachj@gmail.com` CONFIRMED as the only human identity. `amy789smith`, `beth`, `bethr` NOT found in any VM URI.
- [x] **Anti-forensic check.** sendanonymousemail.net + willselfdestruct.com used (known). No Tor, no proxy/VPN found. www.annoy.com and www.clintonfein.com accessed (research context).
- [x] **VERDICT.** See Results below.
- [x] Append facts to `cases/NITROBA/docs/shared_facts.md`.
- [x] Update this card's Results & Post-Mortem.
- [x] Write chronological log to `017-mission-sniper-forensics-vm-activity-profile-audit.md`.

## Results & Post-Mortem

### STATUS: [completed]

- **Approach:** Reused m015_all_syn_fingerprints.txt (no new full-capture scan). Parsed all 1,761 SYN entries with Python regex to find window=64240/wscale=0 entries. Started stopped SIFT container and ran a single targeted tshark query with an OR-filter of all 147 VM stream numbers to produce m017_vm_http_requests.txt (480 lines). Python post-processed for hosts, search trail, identity sweep, and anti-forensic indicators. All output files written to scratch.

- **Findings:**

  **(a) VM True Active Window:**
  - FIRST VM stream: **stream 1095, frame 51957, 2008-07-22T05:41:26Z** (port 80)
  - LAST VM stream: **stream 1727, frame 84644, 2008-07-22T06:05:10Z** (port 80)
  - Total VM active duration: **23 minutes 44 seconds**
  - M012's stated window of "05:02:05–06:09:59" is SUPERSEDED. It was built from User-Agent matching that incorrectly included Mac OS X streams (1045 at 05:02:05 is Mac; 1865 at 06:09:59 is Mac). The correct TCP-stack-verified window is 05:41:26Z–06:05:10Z.
  - The VM was active **21 minutes 31 seconds** before the first hostile email (06:02:57Z).

  **(b) VM Streams and Distinct Hosts:**
  - **147 unique VM streams** (SYN fingerprint: window=64240, wscale=0)
  - **480 HTTP requests** extracted from those streams
  - **63 distinct HTTP hosts** contacted
  - Top hosts: mail.google.com (124 reqs), z.about.com (52), www.google.com (43), l.yimg.com (41), pagead2.googlesyndication.com (23), www.annoy.com (13), i.ytimg.com (13), www.willselfdestruct.com (10), login.live.com (7), www.sendanonymousemail.net (7), download.windowsupdate.com (6)

  **(c) Complete Chronological Search/Research Trail (URL-decoded):**
  1. **2008-07-22T05:57:38Z** — Google search: **"how to annoy people"** (stream 1473)
  2. **2008-07-22T05:58:01Z** — Google search: **"sending anonymous mail"** (stream 1473)
  3. **2008-07-22T05:58:07Z** — Google search: **"i want to harass my teacher"** (stream 1473)
  4. **2008-07-22T05:58:32Z** — Yahoo Answers search: **"can I go to jail for harassing my teacher?"** (stream 1540)
  5. **2008-07-22T05:59:34Z** — Google search: **"google calendar"** (stream 1574, navigating to Gmail/GCal for jcoachj account)
  6. **2008-07-22T06:01:24Z** — Google search: **"send anonymous mail"** (stream 1602, follow-up research for second anonymiser)
  
  *Premeditation narrative:* Attacker first sought annoyance tactics, then anonymity methods, then directly expressed intent ("harass my teacher"), then researched legal consequences, then proceeded to act.

  **(d) Identity Confirmation — VM-only, stack-verified:**
  - `jcoachj@gmail.com` CONFIRMED: Google Calendar and Gmail URIs in streams 1601 and 1605 contain auth tokens referencing this account (06:00:44Z–06:00:56Z).
  - `amy789smith` — NOT found in any VM HTTP URI. Confirmed Mac OS X side only (stream 1865, M015).
  - `beth@bethr.org` — NOT found in any VM HTTP URI. Confirmed Mac OS X side only (stream 624, M010).
  - `mylady.ixchel@gmail.com` — NOT found in VM URIs.
  - **VERDICT: `jcoachj@gmail.com` is the ONE and ONLY human identity verified in the Windows XP VM. Attribution to Johnny Coach is DEFINITIVE.**

  **(e) Anti-Forensic / Evasion:**
  - `sendanonymousemail.net` (streams 1621/1622) and `willselfdestruct.com` (streams 1674-1683, 1701-1705) — both anonymous email services, previously confirmed used.
  - `www.annoy.com` (stream 1497, 05:57:52Z) — "Annoy.com" harassment resource site; visited immediately after Google searches for annoyance tactics.
  - `www.clintonfein.com` (streams, 06:01:26-27Z) — Clinton Fein is a First Amendment/harassment legal/art site. Possibly researched for legal context after "go to jail" search.
  - `login.live.com` / `mail.live.com` (streams 1455-1466, 05:57:23-25Z and streams 1567-1571, 05:59:20Z) — Windows Live (Hotmail) login page loaded TWICE but no POST credentials captured. Possible third anonymous email service attempted but abandoned (no send action captured).
  - **No Tor, no proxy, no VPN detected.** No cookie-clearing endpoints found.

- **Confidence Rating:** HIGH (all findings derived from TCP stack fingerprint, not User-Agent)
- **Budget Tally:** 16 tool calls (4 orientation, 12 execution, including 2 writing steps excluded per SOP)
- **NPS / Feedback:** The m015 reuse strategy worked extremely well. Building the tshark OR-filter programmatically from the stream list was efficient. The search trail is the most compelling forensic artifact — 4 escalating searches in 55 seconds culminating in "can I go to jail" 4m25s before the attack.

## Discovered Leads (For Followup)
- **Lead 1:** `www.annoy.com` accessed at 05:57:52Z from VM (stream 1497). This site is explicitly about harassment. Full page content not captured; may contain templates or advice used in the hostile emails.
- **Lead 2:** `login.live.com` / `mail.live.com` loaded twice from VM (05:57:23Z and 05:59:20Z) but no login POST captured. May be a third anonymous email service considered but abandoned. Investigate whether any Hotmail account was used.
- **Lead 3:** `www.clintonfein.com` accessed at 06:01:26-27Z from VM. Clinton Fein publishes on First Amendment and harassment law — attacker may have researched legal consequences further.
- **Lead 4:** `fetch.download.aol.com` accessed at 06:05:10Z (stream 1727, last VM stream). Possible AOL software update or AIM connection attempt from within the VM at session close.
