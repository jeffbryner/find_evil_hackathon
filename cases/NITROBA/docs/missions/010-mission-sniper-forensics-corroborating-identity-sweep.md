# Mission: Corroborating Identity Sweep — Who Was Physically at the Keyboard?
**Target Agent:** sniper-forensics

## Purpose
We have attributed two harassing emails to the machine at 192.168.15.4 and, via a Google session, to the account `jcoachj@gmail.com` (CHEM109 student **Johnny Coach**). The obvious defence is: *"it was an open Wi-Fi network in a dorm room — anyone could have been on that laptop, and a logged-in Gmail cookie only proves a browser was logged in, not who was typing."*

Your mission is to defeat or confirm that defence by recovering **independent, non-Google identity artifacts** from the same host during the same session. If Facebook, Yahoo Messenger, or any other personal service on that machine also resolves to Johnny Coach, attribution becomes multi-source and near-irrefutable. **If they resolve to a different person, that is a finding of equal or greater importance and you must report it loudly** — it would mean the Gmail session belonged to someone whose laptop was borrowed, and the case theory changes.

## Background
Case NITROBA (2008 harassment investigation, network-only evidence).
- Evidence: `/case/images/nitroba.pcap` inside SIFT (host: `cases/NITROBA/images/nitroba.pcap`).
- Host of interest: **192.168.15.4** / MAC `00:17:f2:e2:c0:ce` — Apple MacBook1,1 "Obsidian", online 04:29:51–06:13:47 UTC on 2008-07-22. Runs a Windows XP VM (VMware NAT) alongside Mac OS X, so multiple User-Agents share the IP.
- Known leads from M006/M007 (do not re-derive, go straight to them):
  - **Stream 624** — Facebook activity ~04:52 UTC (user accepting a platform invite).
  - **Stream 1865** — Yahoo Messenger file transfer to filetransfer.msg.yahoo.com, 06:09:59 UTC.
- 2008-era traffic is largely unencrypted HTTP, so display names, profile IDs, usernames and email addresses are frequently visible in cleartext.
- Suspect pool (CHEM109 roster) — match against this list: Amy Smith, Burt Greedom, Tuck Gorge, Ava Book, **Johnny Coach**, Jeremy Ledvkin, Nancy Colburne, Tamara Perkins, Esther Pringle, Asar Misrad, Jenny Kant.
- Write ALL output to `/scratch/nitroba.pcap/` (host: `cases/NITROBA/scratch/nitroba.pcap/`). Do NOT modify the pcap.

## Budget & Rules of Engagement
- **Orientation Budget:** 4 tool calls
- **Execution Budget:** 12 tool calls
- **Reporting Budget:** 4 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of the 20-call total), stop active forensics and use the remainder to write partial findings and exit cleanly.
- **Fail-Fast Condition:** Two-strike rule per command. Reassemble only the named streams plus the ONE bounded keyword sweep below. If a stream yields no identity data, record "no identity data" and move on — do not go fishing through unrelated streams.
- Batch tshark commands into single shell calls where possible.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` and execute the `shared-facts-sop` skill; execute the `delegating-mission-cards-sop` skill.
- [x] Follow **stream 624** → `/scratch/nitroba.pcap/m010_stream_624_facebook.txt`. COMPLETE.
- [x] Follow **stream 1865** → `/scratch/nitroba.pcap/m010_stream_1865_yahoo.txt`. COMPLETE.
- [x] **Bounded identity keyword sweep** → `/scratch/nitroba.pcap/m010_identity_params.txt`. COMPLETE (200 lines, capped).
- [x] Cross-reference recovered identities against CHEM109 roster. COMPLETE.
- [x] **Verdict** stated below.
- [x] Append confirmed facts to `cases/NITROBA/docs/shared_facts.md`. COMPLETE.
- [x] Update this mission card's **Results & Post-Mortem** section. COMPLETE.
- [x] Write chronological technical log to `010-mission-sniper-forensics-corroborating-identity-sweep-audit.md`. COMPLETE.

## Results & Post-Mortem
- **Approach:** Ran three tshark commands in a single batched `docker exec` call against the NITROBA container. Read all three output files, extracted cleartext identity artifacts, decoded URL-encoded cookies, and cross-referenced all usernames/emails against the CHEM109 roster and dorm-room occupant list.

- **Findings:**

  **Stream 624 — Facebook (04:51–04:52 UTC, Mac OS X Firefox, 192.168.15.4):**
  - `login_x` cookie decoded → registered Facebook email: **`beth@bethr.org`**
  - Confirmed by: `/ajax/precog.php?email=beth%40bethr.org` (frame 32229, 04:50:30 UTC)
  - Facebook user ID (c_user cookie): **`588141158`**
  - Action taken: accepted a "Adopt Me!" platform invite from peer `533253664`
  - User-Agent: `Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.16) Gecko/20080702 Firefox/2.0.0.16` (Mac OS X Firefox — NOT the Windows XP IE UA used for hostile emails)
  - Roster cross-reference: **"beth@bethr.org" is NOT on the CHEM109 roster.** No match to Amy Smith, Burt Greedom, Tuck Gorge, Ava Book, Johnny Coach, Jeremy Ledvkin, Nancy Colburne, Tamara Perkins, Esther Pringle, Asar Misrad, or Jenny Kant.
  - Note: `bethr.org` domain previously flagged in leads as `mail.bethr.org`; this Facebook account belongs to a person named "Beth."

  **Stream 1865 — Yahoo Messenger (06:09:59 UTC, Windows XP IE 5.5 / VMware VM, 192.168.15.4):**
  - YMSG binary payload (cleartext fields): **`amy789smith`** appears in both field-1 and field-0 (sender/initiator username)
  - This is the logged-in Yahoo Messenger screen name making the file transfer POST
  - File being transferred: `057f280df74aeda1a8aada6a0f218871b5417eb3.png`
  - Destination: `filetransfer.msg.yahoo.com` (Yahoo's P2P file transfer relay)
  - Timestamp: 06:09:59 UTC — **5 minutes and 35 seconds AFTER** the second hostile email was sent (06:04:24 UTC)
  - Roster cross-reference: **`amy789smith` = Amy Smith — DIRECT MATCH to CHEM109 suspect pool.** First name "Amy" + last name "Smith" + numeric suffix is a textbook username construction.

  **Bounded Identity Sweep (m010_identity_params.txt):**
  - Top identity hit: frame 32229 — `www.facebook.com /ajax/precog.php?email=beth%40bethr.org` → confirms `beth@bethr.org`
  - Flickr feed repeatedly accessed: `api.flickr.com /services/feeds/photos_public.gne?id=89101607@N00` — Flickr user ID `89101607@N00` (not directly tied to a named person without lookup, flagged as lead)
  - `login.live.com` (Hotmail/Windows Live) accessed at 05:57:24 UTC and 05:59:20 UTC — login page loaded but no credentials visible in cleartext (no form POST captured)
  - Gmail session visible at 06:00:58+ UTC — consistent with known `jcoachj@gmail.com` session

- **VERDICT: INCONCLUSIVE / PARTIALLY CONTRADICTING JOHNNY COACH**
  - The non-Google artifacts do NOT corroborate Johnny Coach; instead they introduce two additional identities:
    1. **`beth@bethr.org`** (Facebook, 04:51 UTC, Mac OS X side) — identity unknown from CHEM109 roster; no match.
    2. **`amy789smith`** (Yahoo Messenger, 06:09 UTC, Windows XP VM side) — **Amy Smith, CHEM109 student**, DIRECT match.
  - The device 192.168.15.4 ("Obsidian" MacBook) had AT LEAST THREE distinct identities active during the session: `beth@bethr.org` (Facebook), `jcoachj@gmail.com` (Gmail/hostile emails), and `amy789smith` (Yahoo Messenger).
  - The Gmail session (`jcoachj@gmail.com`) and both hostile emails remain fully confirmed on 192.168.15.4 via prior missions. The Google-based attribution to Johnny Coach is unaffected.
  - The presence of `amy789smith` (Amy Smith) on the SAME device AFTER the hostile emails suggests either: (a) Amy Smith was on the device concurrently or shortly after, (b) Amy Smith's YM was auto-logged-in on a shared/borrowed device, or (c) Amy Smith is a co-conspirator or the actual sender. This materially complicates single-person attribution.
  - **Amy Smith should be elevated to prime alternate suspect** and a new mission should be spawned to examine her in depth.

- **Confidence Rating:** HIGH confidence in raw artifact extraction (cleartext, unambiguous). MEDIUM confidence in interpretation — the presence of `amy789smith` post-hostile-email is genuinely ambiguous as to whether she is victim, co-user, or co-conspirator.

- **Budget Tally:** 14 tool calls used (4 orientation + 7 execution + 3 reporting write-outs). Within 20-call budget.

- **NPS / Feedback:** Batching all three tshark commands into a single `docker exec` call was highly efficient. The mission design was well-scoped. Recommend spawning a dedicated mission to: (1) establish Amy Smith's full activity log on the device, (2) determine who `89101607@N00` (Flickr) maps to, and (3) investigate `beth@bethr.org` Facebook identity.

## Discovered Leads (For Followup)
- **Lead 1 — AMY SMITH (HIGH PRIORITY):** Yahoo Messenger screen name `amy789smith` active on 192.168.15.4 at 06:09:59 UTC — 5m35s after second hostile email. Matches CHEM109 student Amy Smith. Needs dedicated mission to establish full YM session timeline and determine if she was co-user or co-conspirator.
- **Lead 2 — beth@bethr.org Facebook identity:** Facebook user `588141158`, email `beth@bethr.org`, active on 192.168.15.4 at 04:51–04:52 UTC (Mac OS X Firefox). Identity not in CHEM109 roster. Investigate who "Beth" is and relationship to dorm room occupants or device owner.
- **Lead 3 — Flickr user `89101607@N00`:** Accessed three times from 192.168.15.4 (04:49, 04:51, 05:21 UTC). Flickr user ID may resolve to a real-name account. Investigate via Flickr API or public profile.
- **Lead 4 — Windows Live (Hotmail) login page:** Loaded twice at 05:57 and 05:59 UTC from 192.168.15.4 but no credentials captured. May have been aborted or used HTTPS for credential submission. Check for additional streams to login.live.com.
