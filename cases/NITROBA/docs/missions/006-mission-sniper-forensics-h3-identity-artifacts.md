# Mission: H3 — Identity Artifact Sweep (tshark: keywords, User-Agents, POST payloads)
**Target Agent:** sniper-forensics

## Purpose
Harvest identity-bearing artifacts from the raw pcap: occurrences of the victim's email / class-list surnames in payloads, the full browser User-Agent inventory, and all HTTP POST form payloads. These artifacts let us later tie the hostile flow to a named person.

## Background
Case NITROBA: capture of dorm G24 uplink, 2008-07-22 01:51:07→06:13:47 UTC, 94,410 packets, mostly 2008-era unencrypted HTTP. SIFT container is running (id in `cases/NITROBA/scratch/container_id.txt`); pcap is at `/case/images/nitroba.pcap` inside the container; write outputs ONLY to `/scratch/` (host: `cases/NITROBA/scratch/`). Victim: `lilytuckrige@yahoo.com`. Class list surnames: Smith, Greedom, Gorge, Book, Coach, Ledvkin, Colburne, Perkins, Pringle, Misrad, Kant. Consult `analyze-network-traffic` skill for tshark recipes.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 20 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** Two-strike rule per command. Do NOT follow/reassemble entire TCP streams (that is the next mission once flows are chosen). Do NOT export HTTP objects. Keep outputs as field extractions to /scratch text files.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] Keyword sweep (single tshark pass preferred): for keywords `tuckrige`, `lilytuckrige`, and each class surname — combined OR filter; saved to `/scratch/nitroba.pcap/h3_keyword_hits.txt` (67 data lines)
  - **`tuckrige`/`lilytuckrige`**: Frames 80614 (sendanonymousemail.net POST, stream 1631) and 83601 (willselfdestruct.com POST, stream 1701) — CONFIRMED hostile email delivery
  - **`Coach`**: Frames 77710-77711 (Google Calendar, base64 `jcoachj@gmail.com`), 79732 (Gmail channel bind `jcoachj@gmail.com`) — SUSPECT IDENTIFIED
  - Other keyword hits in streams 430/464 (Yahoo, ~04:35 UTC), streams 894/960 (Yahoo, ~04:55 UTC), streams 1140/1205/1206 (IHG/Orbitz hotel searches, ~05:43-05:48), streams 1743/1997/2000 (upstream responses ~06:05-06:10) — likely surname matches in page content/responses
- [x] User-Agent inventory: saved to `/scratch/nitroba.pcap/h3_user_agents.txt` (31 unique entries)
  - **192.168.15.4 UAs (attacker Wi-Fi host)**:
    - 2463 × `Mozilla/5.0 (Macintosh; U; Intel Mac OS X; en-US; rv:1.8.1.16) Gecko/20080702 Firefox/2.0.0.16` ← PRIMARY browser
    - 632 × `Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_4; en-us) AppleWebKit/525.18 ... Safari/525.20.1`
    - 475 × `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)` ← **Windows VM running inside Mac!**
    - 468 × `iTunes/7.7 (Macintosh; U; Intel Mac OS X 10.5.4)`
    - 10 × `Windows-Update-Agent` ← **confirms Windows VM**
    - 2 × `Adium/1.2.7 (Mac OS X)` ← IM client (AIM/Jabber)
    - 2 × `Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.1) Gecko/2008070208 Firefox/3.0.1` ← Windows Firefox
  - **192.168.1.64 UAs (wired Mac host)**:
    - 218 × iTunes/7.7 Mac Intel; 40 × Apple-PubSub; 28 × Safari 3.1.2 PPC Mac; 26 × Firefox 2.0.0.16 PPC Mac
    - 7 × MSIE 6.0 / AIM Browser 1.0 / Windows NT 5.1 ← also has Windows VM or AIM browser
    - 4 × DAVKit/2.0 iCal 3.0.4 (calendar sync); 1 × Python-urllib/1.17
- [x] HTTP POST payload dump: saved to `/scratch/nitroba.pcap/h3_post_payloads.txt` (372 data lines); notable POSTs:
  - **PRIME — Frame 80614, 06:02:57 UTC, stream 1631**: 192.168.15.4 → 69.80.225.91 (www.sendanonymousemail.net /send.php) — `email=lilytuckrige@yahoo.com&sender=the_whole_world_is_watching@nitroba.org&subject=Your+class+stinks&message=Why+do+you+persist+in+teaching+a+boring+class%3F...`
  - **PRIME — Frame 83601, 06:04:24 UTC, stream 1701**: 192.168.15.4 → 69.25.94.22 (www.willselfdestruct.com /secure/submit) — `to=lilytuckrige@yahoo.com&from=&subject=you+can%27t+find+us&message=and+you+can%27t+hide+from+us.%0D%0A%0D%0AStop+teaching.%0D%0A%0D%0AStart+running.`
  - **IDENTITY — Frame 79732, 06:01:17 UTC, stream 1601-ish**: Gmail channel bind `req0_value=jcoachj%40gmail.com%2F475090` → **jcoachj@gmail.com = Johnny Coach** (CHEM109 student!)
  - **IDENTITY — Frames 77710-77711, 06:00:45 UTC, stream 1602**: Google Calendar `dtid=amNvYWNoakBnbWFpbC5jb20` (base64 → `jcoachj@gmail.com`)
  - **DEVICE — Frame 22757, 04:36:48 UTC, stream 468**: Absolute persistence agent POST to search.namequery.com — payload: Apple MacBook1,1, serial `4H6242CSVMN`, hostname `Obsidian`, HDD serial `NW81T6325527`, MACs `0016cb...`, VMware NIC present (`vmnet8`, IP `192.168.194.1`)
  - **AOL SYNC — Frame 10217, 01:56:23 UTC, stream 266**: 192.168.1.64 → sync.aol.com/m57jean SyncML — AOL username `m57jean` on wired host
  - **GMAIL SESSION 1 — Frame 17299, 03:44:46 UTC, stream 347**: 192.168.1.64 → mail.google.com session key `ik=4233eca8e4` (different Gmail account, wired host)
  - **FACEBOOK — Frames 34052/34230, 04:52 UTC, stream 624**: 192.168.15.4 → www.facebook.com; user accepts platform invite (app_id 15015611585, from_id 533253664); post_form_id `f8e0bcbdf5dfc695429fbdf8e04bdfba`
  - **HOTEL SEARCH — Frames 55107/55826/56279, 05:43-05:45 UTC, stream 1140**: IHG hotel search for Sacramento CA Oct 10-11 2008, iata=99502222 (travel agent code)
  - **YAHOO FT — Frame 90504, 06:09:59 UTC, stream 1865**: Yahoo Messenger file transfer to filetransfer.msg.yahoo.com — YMSG protocol (username likely in stream payload)
- [x] Append key artifacts to `cases/NITROBA/docs/shared_facts.md` under `# Pending Investigative Leads`
- [x] Update this mission card with results
- [x] Write chronological technical log to `-audit.md` file

## Results & Post-Mortem
*(Completed 2026-07-26 by sniper-forensics)*
- **Approach:** Single-pass combined keyword tshark sweep OR-filtering all 13 keywords simultaneously; parallel UA inventory and POST payload extraction. All outputs saved to `/scratch/nitroba.pcap/`. Budget-efficient parallel execution.
- **Findings:**
  - **SUSPECT IDENTIFIED**: Gmail account `jcoachj@gmail.com` observed in POST payloads from 192.168.15.4 (attacker Wi-Fi IP) at 06:00-06:01 UTC, placing Johnny Coach as logged-in user immediately before sending hostile emails.
  - **HOSTILE EMAILS CONFIRMED**: Both anonymous mailer POSTs contain `lilytuckrige@yahoo.com` as recipient in clear-text form fields.
  - **DEVICE FINGERPRINTED**: Absolute theft-tracking agent reveals attacker device = Apple MacBook1,1 serial `4H6242CSVMN`, hostname `Obsidian`, with VMware virtualization running Windows XP.
  - **AOL ACCOUNT**: `m57jean` on wired host 192.168.1.64 (separate device, possibly room occupant).
  - **No class surname other than Coach** produced a confirmed attacker-linked keyword hit; other surname hits appear incidental (page content/hotel search forms).
- **Confidence Rating:** VERY HIGH — direct POST payload extraction with plaintext `lilytuckrige@yahoo.com` and `jcoachj@gmail.com` in captured HTTP traffic.
- **Budget Tally:** 15 tool calls total (5 orientation + 7 execution + 3 reporting; self-termination trigger not reached).
- **NPS / Feedback:** Mission design was efficient; parallel tshark execution saved ~3 tool calls vs sequential. The Absolute agent POST (stream 468) to search.namequery.com was an unexpected bonus yielding full device fingerprint — warrants its own mission for full stream reassembly.

## Discovered Leads (For Followup)
- **Lead 1:** `jcoachj@gmail.com` — Johnny Coach (CHEM109 class member) logged into Gmail on 192.168.15.4 at 06:00-06:01 UTC just before sending hostile emails. Reassemble Gmail session streams for full account activity.
- **Lead 2:** `m57jean` — AOL account on wired host 192.168.1.64 (stream 266, SyncML to sync.aol.com/m57jean). Identify which room occupant (Alice, Barbara, Candice) owns this account.
- **Lead 3:** Apple MacBook serial `4H6242CSVMN`, hostname `Obsidian` — Absolute persistence agent confirmed. Full Absolute beacon stream 468 should be reassembled to extract owner registration name/email if present.
- **Lead 4:** Yahoo Messenger file transfer (frame 90504, stream 1865, 192.168.15.4 → filetransfer.msg.yahoo.com) — reassemble to identify Yahoo IM username and file content.
- **Lead 5:** Facebook session (stream 624) — `post_form_id=f8e0bcbdf5dfc695429fbdf8e04bdfba`; user ID in cookies or profile requests may further corroborate Johnny Coach identity.
- **Lead 6:** Gmail session on 192.168.1.64 (key `ik=4233eca8e4`, stream 347, 03:44 UTC) — different Gmail account on wired host. Decode which account this is (separate suspect or room occupant).
