# Case Report: NITROBA

> **🚨 CURRENT INVESTIGATIVE STATE:** **INVESTIGATION COMPLETE — 19 missions closed.** Attribution is settled: **Johnny Coach (`jcoachj@gmail.com`)** sent both harassing emails from a Windows XP VMware guest running on MacBook "Obsidian" (192.168.15.4) at 06:02:57 and 06:04:24 UTC on 2008-07-22, preceded by a self-declared statement of intent (*"i want to harass my teacher"*) and a legal-consequence check. Amy Smith and the room's occupants are **affirmatively excluded**. Ownership of the physical laptop remains undetermined by network evidence (M018/M019 — a capture-architecture limit, documented in §3.18) and requires legal process. Report is final: summary, timeline, MITRE mapping, recommendations and chain of custody complete below.

## 1. Executive Summary

**Conclusion: the harassing emails were sent by CHEM109 student `jcoachj@gmail.com` — "Johnny Coach".** Confidence: **HIGH**.

Nitroba State University professor **Lily Tuckrige** (CHEM109) received harassing emails at `lilytuckrige@yahoo.com`, traced to dorm G24's public IP **140.247.62.34** — a room shared by Alice, Barbara and Candice behind an **unsecured, passwordless Wi-Fi router** installed by Barbara's boyfriend Kenny. Because the router NATs everyone behind one address, the university's own logs could go no further than the room. IT captured the room's uplink (`nitroba.pcap`, 94,410 packets, 2008-07-22 01:51–06:14 UTC) and a new hostile message was sent during the capture.

**What happened.** At 04:29:51 UTC an Apple **MacBook1,1** (S/N `4H6242CSVMN`, hostname **"Obsidian"**, MAC `00:17:f2:e2:c0:ce`) joined the open Wi-Fi as **192.168.15.4**. At 05:41:26 the operator started a **Windows XP guest inside VMware** on that laptop — an isolated compartment with its own browser, its own cookie jar and its own TCP/IP stack. Inside that VM, over 54 seconds, he researched his attack:

> *"how to annoy people"* → *"sending anonymous mail"* → **"i want to harass my teacher"** → *"can I go to jail for harassing my teacher?"*

He then read up on harassment law (`clintonfein.com`), and at **06:02:57** and **06:04:24** used two throwaway web remailers to deliver both messages to the victim — the second reading *"you can't find us / and you can't hide from us. **Stop teaching. Start running.**"* Both servers confirmed delivery. The whole VM was shut down 46 seconds after the last send.

**How he was caught.** The compartmentalisation was good, but incomplete. At **06:01:08 UTC — 109 seconds before the first threat** — the same VM browser loaded Google Calendar while still logged in to his personal account, writing `gausr=jcoachj%40gmail.com` and `Set-Cookie: OL_SESSION=jcoachj@gmail.com-cal` in cleartext. The searches, the login and both sends all originate from streams bearing an identical, non-Apple TCP SYN signature (window **64240**, wscale **0**), while every other identity on the machine sits on the Mac's native stack (window **65535**, wscale 1/3). That split was validated against two known controls and independently corroborated by a distinct TCP-timestamp clock range — so it does not rely on any spoofable User-Agent string.

**Who is excluded.** Three other identities were present on the laptop — `beth@bethr.org` (Facebook), `amy789smith` (Yahoo Messenger) and Flickr user `89101607@N00` — plus concurrent eBay shopping. **All of them ran on the Mac host side, never inside the VM.** `amy789smith` (Amy Smith, also a CHEM109 student) initially looked incriminating, but her only activity is a background auto-login IM session and a file transfer at **06:09:59 — 4m49s after the VM had already closed**. She is affirmatively excluded, as are the room's occupants (`mylady.ixchel@gmail.com` on a different host, 192.168.1.64).

**Bottom line.** The "open Wi-Fi / shared laptop" defence explains the *machine*; it does not explain the *virtual machine*. Across the entire capture the VM contained exactly one human identity, and that identity announced its intent in writing five minutes before the attack.

## 2. Timeline of Events
*All times UTC.*

| Timestamp | MITRE Category | Event Details |
|-----------|----------------|---------------|
| 2008-07-22 01:51:07 | (Evidence Collection) | Packet capture begins on dorm G24 uplink (`nitroba.pcap`) |
| 2008-07-22 01:56 | (Context — 3rd party) | AOL SyncML contact sync for account `m57jean` via Kenny's router WAN IP 192.168.1.64 (stream 266). NAT'd from the Wi-Fi subnet; attacker's MacBook not yet present [M006, M008] |
| 2008-07-22 ~02:08–03:09 | (Context) | Kenny's Wi-Fi router offline/rebooting; returns with LAN interface 192.168.15.1 first seen 03:05:29 [M005, M008] |
| 2008-07-22 03:44:36 | (Context — 3rd party) | Gmail session `ik=4233eca8e4` for **`mylady.ixchel@gmail.com`** via 192.168.1.64 (URL param `gausr=`). A dorm-occupant identity (Alice/Barbara/Candice), NOT the attacker [M008] |
| 2008-07-22 04:29:51 | Initial Access (T1078 / open Wi-Fi) | Apple MacBook (MAC `00:17:f2:e2:c0:ce`) joins Kenny's unsecured Wi-Fi, obtains **192.168.15.4**; becomes top talker (34,582 pkts, 36% of capture) [M005] |
| 2008-07-22 04:36:48 | Attribution Evidence (device fingerprint) | Computrace/Absolute agent on 192.168.15.4 beacons to search.namequery.com (209.53.113.23), leaking **MacBook1,1, S/N 4H6242CSVMN, hostname "Obsidian", HDD NW81T6325527/K3376NB5022, VMware vmnet8 192.168.194.1** (frame 22757, stream 468) [M006, M007] |
| 2008-07-22 04:43:46–05:02:05 | (Context — Mac side) | Yahoo Messenger client already authenticated as `amy789smith`: buddy-avatar downloads, then address-book sync (`prog-ver=8.1.0.249`, `T=` cookie). **Mac stack** (stream 1045 SYN window 65535/wscale 1) — a long-running background session, NOT someone sitting down [M014, M015] |
| 2008-07-22 04:49:57–05:21:18 | (Context — Mac side) | Flickr feed for user `89101607@N00` pulled 3× via Mac Firefox [M010] |
| 2008-07-22 04:50:30 | (Context — Mac side identity) | Facebook `/ajax/precog.php?email=beth%40bethr.org`, `c_user=588141158` → identity **`beth@bethr.org`** ("Beth"), NOT on the CHEM109 roster. **Mac stack** (stream 624, window 65535) [M010, M015] |
| 2008-07-22 04:51–04:52 | (Context — Mac side) | Same Facebook session accepts an "Adopt Me!" platform invite from peer `533253664` [M010] |
| **2008-07-22 05:41:26** | **Defense Evasion (T1564 — compartmentalisation)** | **Windows XP VM session BEGINS** — first stream with VM stack signature (stream 1095, frame 51957, window 64240/wscale 0). VM runs 23m44s total. Supersedes M012's incorrect 05:02:05 figure [M017] |
| 2008-07-22 05:55–06:10 | (Context — concurrent, Mac side) | Mac-side Firefox browses eBay (leather laptop bags, toroleather.com) throughout the entire attack — 922 requests, none to any anonymizer. **Two environments in use simultaneously** [M009] |
| **2008-07-22 05:57:38** | **⭐ Reconnaissance (T1593)** | **VM Google search: *"how to annoy people"*** (stream 1473) — start of the research trail [M017] |
| 2008-07-22 05:57:52 | Reconnaissance | VM visits `www.annoy.com` (13 requests) — harassment resource site [M017] |
| **2008-07-22 05:58:01** | **⭐ Reconnaissance (T1593)** | **VM Google search: *"sending anonymous mail"*** (stream 1473) [M017] |
| **2008-07-22 05:58:07** | **⭐⭐ STATEMENT OF INTENT** | **VM Google search: *"i want to harass my teacher"*** (stream 1473) — explicit, self-declared intent, 4m50s before the first threat [M017] |
| **2008-07-22 05:58:32** | **⭐⭐ Consciousness of Guilt** | **VM Yahoo Answers search: *"can I go to jail for harassing my teacher?"*** (frame 74920, stream 1540, window 64240 = VM). Referer proves he was **already reading** Yahoo Answers question `qid=20080606160229AA5Exnf`. Cookies anonymous. **4m25s before threat #1** [M014, M015, M016] |
| 2008-07-22 05:58:38–05:58:40 | Reconnaissance | Results page renders; browser auto-fetches a Yahoo profile image from `f3.yahoofs.com` (stream 1549) — page-rendering artifact, not attacker identity [M016] |
| 2008-07-22 05:59:34 | Reconnaissance | VM Google search: *"google calendar"* (stream 1574) — leads directly to the OPSEC failure below [M017] |
| **2008-07-22 06:01:08** | **⭐⭐⭐ ATTRIBUTION (T1078 Valid Accounts)** | **VM logs into Google as `jcoachj@gmail.com`** — URL param `gausr=jcoachj%40gmail.com` + `Set-Cookie: OL_SESSION=jcoachj@gmail.com-cal` (streams 1601/1602, window 64240 = **VM**). The attacker checked his own personal account inside the otherwise-anonymous VM [M007, M013, M015] |
| 2008-07-22 06:01:24–06:01:26 | Reconnaissance (T1593) | VM Google search *"send anonymous mail"*; also visits `clintonfein.com` (First Amendment / harassment law); DNS `www.sendanonymousemail.net` → 69.80.225.91 [M004, M017] |
| **2008-07-22 06:02:57** | **⛔ Impact (T1585 / harassment)** | **THREAT #1 DELIVERED.** VM POSTs `/send.php` to sendanonymousemail.net → `lilytuckrige@yahoo.com`, spoofed sender `the_whole_world_is_watching@nitroba.org`, subject **"Your class stinks"**. Server: HTTP 200 + *"Your message has been sent!"* (frame 80614, stream 1631) [M004, M007] |
| 2008-07-22 06:03:43 | Reconnaissance | VM browses `email.about.com` article on anonymous email; DNS `www.willselfdestruct.com` → 69.25.94.22; loads submit form [M004] |
| **2008-07-22 06:04:24** | **⛔ Impact (T1585 / threat to safety)** | **THREAT #2 DELIVERED.** VM POSTs `/secure/submit` to willselfdestruct.com → `lilytuckrige@yahoo.com`, subject **"you can't find us"**, body *"and you can't hide from us. Stop teaching. Start running."* Server: HTTP 302 → `/secure/success` (frame 83601, stream 1701) [M004, M007] |
| 2008-07-22 06:05:10 | Defense Evasion | **Last VM stream** (1727, `fetch.download.aol.com`) — the Windows XP VM session ends 46 seconds after the second threat [M017] |
| 2008-07-22 05:58–06:08 | (Exclusivity control) | Across the entire send window 192.168.15.4 is the **sole** host issuing HTTP POSTs (6,043 pkts); every other local host emits only ARP/SSDP/DNS. No alternative sender exists [M008] |
| 2008-07-22 06:09:59 | (Context — different user, Mac side) | Yahoo Messenger file transfer, YMSG key 1 = **`amy789smith`** (Amy Smith, also CHEM109). **Mac stack** (stream 1865 SYN window 65535/wscale 3) — a different environment from the one that sent the threats, and 4m49s after the VM had already closed [M010, M011, M013, M015] |
| 2008-07-22 06:13:47 | (Evidence Collection) | Packet capture ends (94,410 packets, ~4h22m). Host still online at capture end |

## 3. Findings & Analysis
### 3.1 Evidence Inventory (Mission 001)
- `nitroba.pcap`: 56,180,821 bytes; MD5 `9981827f11968773ff815e39f5458ec8`; SHA1 `65656392412add15f93f8585197a8998aaeb50a1`. Packet count & capture window pending (capinfos/tshark unavailable on host; SIFT container required).
- No prior extractions exist in `scratch/` (clean start).

### 3.2 Scenario (Mission 002)
- Full text extracted to `cases/NITROBA/scratch/NITROBA-Scenario.txt`.
- Suspect pool (CHEM109 class list): Amy Smith, Burt Greedom, Tuck Gorge, Ava Book, Johnny Coach, Jeremy Ledvkin, Nancy Colburne, Tamara Perkins, Esther Pringle, Asar Misrad, Jenny Kant.
- Known network facts: dorm has 10 Mbps Ethernet uplink; open Wi-Fi router NATs an unknown number of clients behind 140.247.62.34.

### 3.3 Stage 1 Extraction (Mission 003)
- Capture window: **2008-07-22 01:51:07.095278 UTC → 2008-07-22 06:13:47.046029 UTC** (15,759.95s ≈ 4h22m); 94,410 packets; Ethernet encapsulation; SHA256 `2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb`.
- Queryable table `packets` at `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` (columns: timestamp, source_ip, dest_ip, source_port, dest_port, protocol, length, info, filename_path, imagename). Row count verified = packet count (100%).

### 3.4 H1 — Hostile Email Flow (Mission 004, SQL triage)
- **No SMTP anywhere in capture** (zero packets on 25/465/587) → harassment sent via web services over HTTP.
- Attacker host: **192.168.15.4** (Wi-Fi client behind the open router; wired host 192.168.1.64 is a distinct machine).
- PRIME flow #1 (CONFIRMED SEND): `192.168.15.4:36044 → 69.25.94.22:80` POST `/secure/submit` (www.willselfdestruct.com) at 06:04:24.311700Z, followed by GET `/secure/success`.
- PRIME flow #2 (**also CONFIRMED SENT** — corrected by M007): `192.168.15.4:35876 → 69.80.225.91:80` POST `/send.php` (www.sendanonymousemail.net) at 06:02:57.548149Z. The CAPTCHA reload seen after the POST was a *second* compose attempt; the first POST returned HTTP 200 with "Your message has been sent!"

### 3.5 H3 — Identity & Device Artifacts (Mission 006, tshark field extraction)
- **Hostile payloads recovered in plaintext:**
  - Frame 80614 (stream 1631, 06:02:57): `email=lilytuckrige@yahoo.com&subject=Your+class+stinks` → sendanonymousemail.net
  - Frame 83601 (stream 1701, 06:04:24): `to=lilytuckrige@yahoo.com&message=...Stop+teaching.+Start+running.` → willselfdestruct.com
- **Identity on same host minutes before sends:** Google Calendar `dtid` (frame 77710, stream 1602) base64 `amNvYWNoakBnbWFpbC5jb20` = `jcoachj@gmail.com`; Gmail channel bind (frame 79732, stream 1601) `req0_value=jcoachj%40gmail.com`. Matches class-list student **Johnny Coach**.
- **Device fingerprint** (Absolute/Computrace beacon, frame 22757, stream 468): Apple **MacBook1,1**, serial **4H6242CSVMN**, hostname **"Obsidian"**, HDD `NW81T6325527`; VMware NIC `vmnet8` 192.168.194.1 present.
- **User-Agents on 192.168.15.4 (host-wide aggregate counts):** Firefox/2.0.0.16 Intel Mac (2,463), Safari 3.1.2 Mac 10_5_4 (632), **MSIE 6.0/Windows NT 5.1 (475)**, iTunes/7.7 Mac (468), Safari (Computrace agent, 333), Windows-Update-Agent (10). The presence of MSIE 6.0 + Windows-Update-Agent alongside Mac-native agents corroborates the VMware `vmnet8` interface in the Computrace XML: a **Windows XP VM running inside the MacBook**, NAT'd behind the same IP.
- **⚠️ Case-lead adjudication (UA of the sending browser) — RESOLVED by Mission 009:** M006 originally labelled Firefox/Mac "the sending browser family." That was an **inference from host-wide UA frequency, not from the hostile streams**. M009 dumped the User-Agent header **per frame** for the two hostile POSTs and confirmed both frames 80614 and 83601 carry `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`. **M007 is correct; M006 is refuted and superseded.** Root cause of the error: Firefox dominates by *volume* (922 requests in the send window vs 475 for IE6) because eBay listing pages pull hundreds of images per page — volume is not authorship.
- **Two browsers, one IP, running simultaneously (M009):** Firefox on the **Mac OS X host** was used *exclusively* for eBay/shopping and never once touched an anonymizer service; Internet Explorer 6 in the **Windows XP VM** was used for the Google session and both hostile sends. Only per-frame inspection separates them, because VMware NAT puts both behind 192.168.15.4.
- Other identities in capture (context, wired host 192.168.1.64): AOL account `m57jean` (SyncML, stream 266); separate Gmail session (`ik=4233eca8e4`, ~03:44 UTC).
- Artifact files: `cases/NITROBA/scratch/nitroba.pcap/h3_keyword_hits.txt`, `h3_user_agents.txt`, `h3_post_payloads.txt`.

### 3.6 H2 — Network Topology & Device Map (Mission 005, SQL triage)
- **Topology:** NSU wired LAN `192.168.1.0/24` (gateway 192.168.1.254, MAC `00:1d:6b:99:98:68`) + Kenny's open Wi-Fi `192.168.15.0/24`. Kenny's router = one device with consecutive MACs: WAN `192.168.1.64` (`00:1d:d9:2e:4f:61`) / LAN `192.168.15.1` (`00:1d:d9:2e:4f:60`).
- **Attacker host 192.168.15.4:** MAC `00:17:f2:e2:c0:ce` (Apple OUI — consistent with MacBook1,1 "Obsidian"); TOP TALKER (34,582 pkts); **active ONLY 04:29:51–06:13:47 UTC** (joined Wi-Fi ~95 min before the sends; still present at capture end).
- Other Wi-Fi clients: 192.168.15.5 (72 pkts), 15.7 (11 pkts), 15.8 (13 pkts, joins 06:11:52 — after the sends), 15.2 (2 pkts). Wired: 192.168.1.5 (49 pkts, Apple MAC `00:0a:95:69:38:cc`).
- **⚠️ Anomaly to resolve (Mission 008):** IP 192.168.1.64 shows TWO MACs — `00:1f:f3:5a:77:9b` (Apple) and `00:1d:d9:2e:4f:61` (router WAN). The earlier `m57jean`/Gmail-`ik` sessions attributed to "wired host 192.168.1.64" may actually be NAT'd Wi-Fi traffic or a distinct wired Mac; note the attacker's MacBook was NOT yet on the network at 03:44 UTC either way.
- 10.0.1.5 / 10.0.1.200 traffic (04:33–06:11) — possible VPN/ad-hoc tunnel, unresolved (low priority).

### 3.7 Stream-Level Validation (Mission 007, tshark `follow,tcp,ascii`)
Five streams reassembled end-to-end, converting inference into direct evidence:
- **Stream 1631** (sendanonymousemail.net): full form recovered — recipient, spoofed sender, subject, complete body — plus server response *"Thank You. Your message has been sent!"* and session cookie `PHPSESSID=762adba03236142ccec305f6a20aaffa`.
- **Stream 1701** (willselfdestruct.com): full form recovered, server response HTTP 302 → `/secure/success`.
- **Streams 1601 / 1602** (Google): `gausr=jcoachj%40gmail.com` in the URL and `Set-Cookie: OL_SESSION=jcoachj@gmail.com-cal` — an *authenticated, server-issued* session identifier, not a user-typed string.
- **Stream 468** (Computrace/Absolute): device XML confirmed originating from IP `192.168.15.4` / MAC `00:17:f2:e2:c0:ce` at 04:36:48Z. The Computrace agent uses a Mac-native Safari UA (it is the host OS reporting), while the browser streams use the XP-VM IE6 UA — internally consistent with one physical MacBook running a VM.
- **Continuity verdict:** byte-identical User-Agent across all four browser streams (1601, 1602, 1631, 1701), all from the same IP+MAC, spanning the identity session and both hostile sends within a 196-second window.

### 3.8 Exclusivity & Dual-MAC Resolution (Mission 008, SQL)
- **Exclusivity (rebuts "someone else on the open Wi-Fi did it"):** during 05:58–06:08 UTC, 192.168.15.4 sent 6,043 packets and was the **only** host issuing HTTP POSTs. Every other local host in that window emitted only ARP, UPnP/SSDP and DNS. There is no candidate alternative sender.
- **Dual-MAC anomaly resolved:** IP 192.168.1.64 was held by Kenny's router WAN interface (`00:1d:d9:2e:4f:61`) during Era 1 (01:51–01:58) and Era 3 (03:43+), with a brief Era 2 at 03:09:08 when a different Apple device (`00:1f:f3:5a:77:9b`) answered ARP directly on the wired LAN. The router was offline ~02:08–03:09 (reboot). Consequence: the `m57jean` and `mylady.ixchel@gmail.com` sessions seen "on 192.168.1.64" were **NAT'd Wi-Fi traffic**, not a separate wired machine.
- **Third identity recovered:** `mylady.ixchel@gmail.com` (03:44:36Z) — almost certainly a dorm occupant (Alice/Barbara/Candice), and importantly **not** the attacker: the attacker's MacBook had not yet joined the network at that time (first seen 04:29:51).

### 3.9 Browser Adjudication & Send-Window Narrative (Mission 009)
Per-frame `http.user_agent` extraction settled the M006/M007 conflict definitively:
- Frames **80614** and **83601** (the two hostile POSTs) both carry `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`. So do the `jcoachj@gmail.com` Google streams 1601/1602. **M007 confirmed, M006 refuted.**
- Send-window UA split (1,464 requests, 05:55–06:10): Firefox/Mac 922 (eBay shopping only), **IE6/XP-VM 475 (Google session + both hostile sends)**, iTunes 23, Safari 23, Windows-Update-Agent 9.
- **Behavioural picture:** while the Mac side was casually shopping for laptop bags on eBay, the operator switched into a Windows XP virtual machine, checked a Gmail account, searched *"send anonymous mail"*, and used two throwaway anonymizer services to send threats — then returned to eBay. The VM is best read as **deliberate compartmentalisation** (T1564 Hide Artifacts): a separate browser/OS with no personal cookies, used only for the attack. The single mistake was checking Gmail inside that same VM.

### 3.10 Corroborating Identity Sweep — CONFLICT RAISED (Mission 010)
The sweep was designed to rebut an "open Wi-Fi / borrowed laptop" defence. It did the opposite and must be reported honestly:
| Identity | Service | Time (UTC) | Side of the machine | On CHEM109 roster? |
|---|---|---|---|---|
| `beth@bethr.org` (FB uid 588141158) | Facebook | 04:50–04:52 | Mac OS X / Firefox | **No** |
| `jcoachj@gmail.com` | Gmail + Calendar | 06:01:08 | **Windows XP VM / IE6** | **Yes — Johnny Coach** |
| `amy789smith` | Yahoo Messenger | 06:09:59 | reported as XP VM (UA `MSIE 5.5`) | **Yes — Amy Smith** |
- Also seen: `login.live.com` loaded 05:57 & 05:59 (no credentials in cleartext); Flickr feed `89101607@N00` pulled 3× (04:49, 04:51, 05:21).
- **Assessment:** one physical laptop, at least three distinct human identities in ~80 minutes. This is entirely consistent with a shared dorm-room machine. It does **not** overturn the finding that the mail left this machine, but it does mean *"whose machine it is"* ≠ *"who sent it"*. Attribution must therefore rest on the **VM-side** evidence, not on machine ownership.
- **Note on `MSIE 5.5`:** that string is the User-Agent the Yahoo Messenger *client application* emits — it is not proof of a browser or of which OS. M011 is verifying whether `amy789smith` is the authenticated sender or merely the transfer peer.
### 3.11 The `amy789smith` Conflict (Missions 011 & 012) — ✅ RESOLVED in §3.14; M012's method REJECTED
**M011 (protocol-level):** Stream 1865 frames carry source MAC `00:17:f2:e2:c0:ce` — the same MacBook, **no second physical device**. Raw YMSG bytes `31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80` place `amy789smith` in **key 1 = the logged-in local user's own Yahoo ID**; peer keys 4 and 5 are absent. Transfer metadata: key 27 filename `057f280df74aeda1a8aada6a0f218871b5417eb3.png`, key 28 size 12,740, key 29 type PNG. So Amy Smith's Yahoo account was *authenticated on this laptop* 5m35s after the second threat. She cannot be dismissed as a mere chat peer.
- *Gap:* M011's capture-wide Yahoo sweep failed (tshark `-R` syntax incompatibility, two-strike rule triggered) — `m011_yahoo_all_hits.txt` is empty. We therefore do **not** yet know when the Yahoo session began or whether `amy789smith` appears elsewhere. Addressed by M014.

**M012 (identity↔UA matrix):** 490 VM-UA requests, 05:02:05–06:09:59. Matrix produced:
| Identity | Environment claimed | First seen | Evidence |
|---|---|---|---|
| `jcoachj@gmail.com` | VM (MSIE 6.0/WinNT5.1) | 06:00:44 | frames 77508/78571, `gausr=` param |
| `amy789smith` | VM (**MSIE 5.5 — disputed**) | 06:09:59 | frame 90504, YMSG POST body |
| (unknown) | VM (MSIE 6.0) | 05:57:24 | login.live.com loaded, no creds |
| `beth@bethr.org` | Mac (Firefox 2.0.0.16) | 04:50:30 | frame 32229, `email=` param |
| `89101607@N00` | Mac (Firefox 2.0.0.16) | 04:49:57 | Flickr RSS |

**⚠️ CASE-LEAD CHALLENGE TO M012's VERDICT.** M012 answered "NO — jcoachj is not the only VM identity," but that verdict rests entirely on assigning the Yahoo traffic to the VM because its UA `Mozilla/4.0 (compatible; MSIE 5.5)` is "Windows-only, no Mac equivalent." The agent's own post-mortem concedes this UA was not in the mission's VM list and was added by its own judgement. I assess the reasoning as **unsound**:
1. Genuine IE 5.5 on Windows emits a platform token (e.g. `; Windows NT 5.0`). A bare `MSIE 5.5` with **no platform token whatsoever** is characteristic of an application with a hardcoded UA, not of a real browser.
2. This host demonstrably ran **`Adium/1.2.7 (Mac OS X)`** — a Mac multi-protocol IM client that supports Yahoo and performs file transfers to `filetransfer.msg.yahoo.com`.
3. Absence of a Mac token is not evidence of Windows; it is absence of evidence.

The conflict is therefore **not yet resolved in either direction**, and the case cannot name a suspect until it is. Missions 013 (OS fingerprinting via TTL/TCP stack — independent of UA strings) and 014 (full Yahoo session reconstruction) are running.
### 3.12 OS Stack Fingerprinting (Mission 013) — UA-Independent Environment Split
**TTL method FAILED and was correctly discarded.** Every packet from 192.168.15.4 arrives at TTL **63**, including known-VM streams. Root cause: VMware NAT normalises the IP TTL to the Mac host's default (64), which then decrements once at Kenny's router. Only 1 packet in 34,554 showed TTL 126. The agent reported this honestly rather than forcing the expected 64/127 split — good practice.

**TCP SYN initial-window method SUCCEEDED and validated against both controls:**
| Stream | Anchor | SYN window | Environment |
|---|---|---|---|
| 468 | Computrace agent (**known Mac control**) | 65535 | Mac OS X ✓ |
| 624 | Facebook `beth@bethr.org` (**known Mac control**) | 65535 | Mac OS X ✓ |
| 1601 | Google `jcoachj@gmail.com` | **64240** | **Windows XP VM** |
| 1631 | Hostile POST 1 | **64240** | **Windows XP VM** |
| 1701 | Hostile POST 2 | **64240** | **Windows XP VM** |
| 1865 | `amy789smith` Yahoo transfer | 65535 | Mac OS X (**disputed — see 3.13**) |
- 64240 is the textbook Windows XP initial window (44 × MSS 1460); 65535 is the classic BSD/Mac OS X value. Both controls landed correctly, which is what makes the method credible.
- **Settled beyond dispute:** both threatening emails and the `jcoachj@gmail.com` session were issued from the **Windows XP VM**. The `MSIE 5.5` UA does *not* group with the VM streams, confirming my rejection of M012's reasoning on that specific point.

### 3.13 Yahoo Session Reconstruction (Mission 014) — MAJOR FIND; environment claim ✅ RESOLVED (refuted) in §3.14
**⭐ The single most incriminating artifact in the case:** at **05:58:32 UTC** the attacker host ran a Yahoo Answers search for ***"can I go to jail for harassing my teacher?"*** (frame 74920, stream 1540), with the results page loaded at 05:58:38 — **4 minutes 25 seconds before the first threatening email**. This is textbook consciousness-of-guilt: the operator researched the legal risk of harassing a teacher, then immediately researched how to send anonymous mail, then sent two threats to their teacher.

**Yahoo session scope:** the `amy789smith` client was already authenticated well before the attack — buddy avatars downloading from 04:43:46, address-book sync with a `T=` cookie at 05:02:05 — i.e. a **long-running background/auto-login session**, not someone freshly sitting down. The literal string `amy789smith` appears in only 9 frames, all inside 06:09:58–06:10:00. M014's own verdict: this **does not** place Amy Smith at the keyboard during the sends.

**⚠️ UNRESOLVED CONTRADICTION between M013 and M014.** M014 concludes the Yahoo client was **Yahoo! Messenger for Windows 8.1.0.249** (from `prog-ver=8.1.0.249`) running in the VM. M013 concludes stream 1865 came from the **Mac** stack (SYN window 65535). These are mutually exclusive. Assessment of each strand:
- M014's version string is strong, direct evidence — YM 8.1 was a Windows-only build.
- But M014's environment claim leans on frame 48627 being "VM", which came from **M012's UA-based classification that I have already rejected as circular**.
- M013's SYN-window method is UA-independent and validated against two controls, which makes it the stronger instrument — *provided* it read the correct SYN for stream 1865.
- The `T=` cookie at 05:02:05 also raises a live question: was that address-book sync even the same environment as the 06:09:59 transfer?

Mission 015 reconciled this. **See 3.14 — M013 was correct and M014's environment claim was wrong.**

### 3.14 Definitive Stack Reconciliation (Mission 015) — THE DECIDING ANALYSIS
M015 re-derived every client SYN from 192.168.15.4 using **two independent discriminators** (initial window size AND window-scale shift), plus TCP timestamp clock ranges as a third corroborating signal. All ten in-scope streams classified consistently, with no exceptions:

| Stream | SYN frame | What it carried | Window | WScale | Environment |
|---|---|---|---|---|---|
| 468 | 22528 | Computrace agent (**Mac control**) | 65535 | 3 | Mac OS X ✓ |
| 624 | 33784 | Facebook `beth@bethr.org` (**Mac control**) | 65535 | 1 | Mac OS X ✓ |
| 1045 | 48624 | `prog-ver=8.1.0.249` address-book sync | 65535 | 1 | **Mac OS X** |
| **1540** | **74913** | **"can I go to jail for harassing my teacher?"** | **64240** | **0** | **WINDOWS XP VM** |
| 1601 | 77503 | Gmail `jcoachj@gmail.com` | 64240 | 0 | Windows XP VM |
| 1631 | 80611 | Hostile email 1 | 64240 | 0 | Windows XP VM |
| 1701 | 83597 | Hostile email 2 | 64240 | 0 | Windows XP VM |
| 1861 | 90372 | YMSG :5050 `amy789smith` | 65535 | 3 | Mac OS X |
| 1864 | 90423 | Yahoo addr sync `amy789smith` | 65535 | 3 | Mac OS X |
| 1865 | 90455 | Yahoo filetransfer `amy789smith` | 65535 | 3 | Mac OS X |

**Findings:**
1. **M013 verified.** Stream 1865 *does* have a captured client SYN (frame 90455, window 65535, wscale 3, timestamps present). M013's classification stands; only its frame citation was loose.
2. **M014's environment claim refuted.** The `prog-ver=8.1.0.249` request sits in stream 1045, whose SYN is unambiguously Mac. The version string is real but is **not** evidence of Windows: Adium/libpurple hard-codes the Yahoo Messenger 8.1.0.249 protocol version for server compatibility. A genuine Windows process cannot emit a SYN with window 65535 + wscale 3 + Mac-pattern timestamps. *This is precisely the alternative explanation I advanced when rejecting M012's UA reasoning.*
3. **Independent clock corroboration:** Mac-side TSval clocks run ~734M–936M; VM-side ~644M — separate virtual/physical hardware clocks, a third signal agreeing with the split.
4. **⭐ The premeditation search was inside the VM.** Stream 1540 (window 64240, wscale 0) puts *"can I go to jail for harassing my teacher?"* in the **same isolated environment** that then held the `jcoachj@gmail.com` session and sent both threats, all within 6 minutes.

**Consequence — attribution is now decisive.** The Windows XP VM is a closed environment with its own cookie jar, and across the entire capture it contained **exactly one human identity: `jcoachj@gmail.com`**. Everyone else on the laptop (`beth@bethr.org`, `amy789smith`, Flickr, eBay) was on the Mac host side. The "shared open Wi-Fi / shared laptop" defence therefore fails: it explains the *machine*, but not the *virtual machine*.

### 3.15 The Premeditation Search — Court-Grade Verification (Mission 016)
The most legally significant artifact was verified **verbatim by two independent methods** (TCP stream reassembly and per-frame field extraction), which agree exactly:

**Frame 74920 — 2008-07-22 05:58:32.660583 UTC — stream 1540**
```
GET /search/search_result;_ylt=A9FJui4Od4VIL5QANivD7BR.;_ylv=3
    ?p=can+I+go+to+jail+for+harassing+my+teacher%3F HTTP/1.1
Host: answers.yahoo.com
Referer: http://answers.yahoo.com/question/index?qid=20080606160229AA5Exnf&show=7
User-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)
Cookie: B=drcsgu548atoe&b=3&s=2p; answers=rPr8rbs2YDe6N_jmMp5o...
```
URL-decoded query: **`can I go to jail for harassing my teacher?`**

- **The Referer deepens it:** he did not stumble onto this. He was **already reading a specific Yahoo Answers question** (`qid=20080606160229AA5Exnf`, answer #7) and then ran the broader search from that page. This is sustained deliberation about legal consequences, not an idle query.
- **Cookies are anonymous** — `B=` (browser fingerprint) and an `answers=` session cookie only; **no `Y=` or `T=` Yahoo auth token**. The VM's Yahoo browsing was unauthenticated, which is consistent with the VM being a clean, compartmentalised environment and is why this search carries no Yahoo identity of its own.
- **Environment: Windows XP VM**, established independently by M015's stack fingerprint (window 64240/wscale 0) and corroborated by the IE6 UA matching both hostile sends.
- **Elapsed: search → threat #1 = 4 minutes 25 seconds.**
- *Residual gap:* M016 exhausted its budget after extracting 1,182 HTTP request lines for 05:50–06:02 (`m016_all_http_5950_0602.txt`) without filtering them for other queries. The complete pre-attack research trail is being finished in M017.

### 3.16 The Complete Premeditation Trail (Mission 017) — CASE-DEFINING
M017 closed M016's residual gap by extracting **every** search query issued from 192.168.15.4 during the VM's lifetime and classifying each carrier stream by SYN fingerprint (the M015 method). The result is a contiguous, self-narrating research trail:

| Time (UTC) | Stream | Env | Query / Site |
|---|---|---|---|
| 05:57:38 | 1473 | VM | Google: **"how to annoy people"** |
| 05:57:52 | — | VM | visits `www.annoy.com` (13 requests) |
| 05:58:01 | 1473 | VM | Google: **"sending anonymous mail"** |
| **05:58:07** | **1473** | **VM** | **Google: "i want to harass my teacher"** |
| 05:58:32 | 1540 | VM | Yahoo Answers: **"can I go to jail for harassing my teacher?"** |
| 05:59:34 | 1574 | VM | Google: "google calendar" |
| **06:01:08** | **1601/1602** | **VM** | **Google login `jcoachj@gmail.com`** |
| 06:01:24 | — | VM | Google: "send anonymous mail"; visits `clintonfein.com` (First Amendment / harassment law) |
| **06:02:57** | **1631** | **VM** | **Threat #1 sent** |
| **06:04:24** | **1701** | **VM** | **Threat #2 sent** |

**Why this is decisive:**
1. **Explicit statement of intent.** *"i want to harass my teacher"* is not ambiguous, not a misclick, and not attributable to a third party — it is the attacker describing his own objective in his own words, **4 minutes 50 seconds** before the first threat landed.
2. **Rational escalation.** annoyance → anonymity mechanism → intent → legal-consequence check → law reading → execution. This is a deliberate, sequenced plan, which defeats any "prank/accident" characterisation and independently corroborates the *mens rea* implied by the Yahoo Answers query.
3. **Single environment, single identity.** All ten artifacts sit in the same isolated VM (window 64240 / wscale 0), whose only human identity in the entire capture is `jcoachj@gmail.com`. The searches and the sends cannot be split between two people.
4. **VM session bounded:** 05:41:26 → 06:05:10 (23m44s). The VM was opened ~16 minutes before the research began and closed **46 seconds after** the second threat — behaviour consistent with a purpose-built, disposable environment. This also **supersedes M012's erroneous 05:02:05 VM-start figure**, which was derived from the UA-based method I rejected.
5. **Concurrency.** Mac-side Firefox was shopping on eBay the whole time (M009). The operator was running the attack in a compartment while his normal session continued — the compartmentalisation was intentional.

### 3.17 Device Ownership — Unresolved (Mission 018)
Whose physical laptop was "Obsidian"? M018 attacked this from DHCP, NetBIOS/SMB, Computrace payloads, HTTP identity headers and per-identity stack classification, and returned an honest negative:

- **Hard facts:** Apple MacBook1,1, S/N **4H6242CSVMN**, hostname **"Obsidian"**, MAC `00:17:f2:e2:c0:ce`, HDD serials NW81T6325527 / K3376NB5022, VMware NAT `vmnet8 192.168.194.1`. The Computrace/Absolute beacon carries **device** telemetry only — no registered-owner, no user-account, no institution fields.
- **No DHCP hostname** was recoverable (the lease predates or falls outside the capture); **no NetBIOS/SMB** name broadcasts from the host.
- **Mac-side identities:** `beth@bethr.org` (Facebook, `c_user=588141158`), `amy789smith` (Yahoo Messenger, persistent auto-login), Flickr `89101607@N00`, plus eBay/iTunes 7.7 activity.
- **Most probable Mac-side primary user: `beth@bethr.org`** — *inference only*, based on the Facebook session being the most personal, interactive, browser-side identity present. **Not proven.** `amy789smith` is a plausible alternative (an always-on IM auto-login is equally consistent with the machine's habitual owner).
- **Not on the CHEM109 roster:** neither "Beth" nor Beth's Facebook ID. `amy789smith` **is** a roster match (Amy Smith).

**Investigative significance:** ownership does **not** alter attribution. The threats came from inside a VMware guest with its own cookie jar and its own TCP stack, whose sole identity was `jcoachj@gmail.com`. Whether Johnny Coach owned the MacBook, borrowed it, or used it in the dorm's open-Wi-Fi common area, the VM was his. Ownership matters only for **seizure planning and consent** — investigators should expect a lawful-process argument that a third party (Beth or Amy Smith) owns the hardware, and should be prepared to establish who had custody of it at 05:41–06:05 UTC on 2008-07-22.

**Residual gap → CLOSED by M019 (negative).** M019 swept the capture for zero-configuration name broadcasts and found **zero mDNS (UDP/5353), zero NBNS (UDP/137) and zero LLMNR (UDP/5355) packets** across all 94,410 frames (verified by two methods; 2,905 packets of ordinary unicast DNS confirm the filter was working). This is a **capture-architecture limitation, not an absence of behaviour**: the sniffer sat at/above the upstream router (192.168.1.254), outside the 192.168.15.0/24 wireless broadcast domain, and mDNS is link-local multicast (224.0.0.251) that does not cross a router boundary. Any "Beth's MacBook.local" or iTunes library name Obsidian was advertising was confined to Kenny's Wi-Fi segment and never reached the capture point. Ownership therefore **cannot be resolved from this evidence** and requires legal process (see §6).

### 3.18 Investigative Limits of This Evidence
Stating the boundaries plainly, so no conclusion is over-read:
- **Single evidence source.** This case rests entirely on one network capture. There is no disk image, no memory image, and no host-based artifact from the MacBook or the VM. Every finding is a network observation.
- **Capture point restricts visibility.** As M019 established, the sniffer was upstream of the dorm AP. Intra-subnet traffic (mDNS, ARP between wireless peers, link-local discovery) is largely invisible. Absence of such artifacts is **not** evidence of absence of the behaviour.
- **No TLS content.** Any encrypted session on the host is opaque. The attribution succeeded only because the 2008-era services involved (Google Calendar, the two remailers, Yahoo Answers) were plaintext HTTP.
- **What is NOT claimed:** we do not claim to know who owned the laptop, who else used it before 04:29:51, or that Johnny Coach was physically alone. We claim — and can demonstrate — that the environment which researched and sent the threats contained exactly one human identity.
- **What IS robust:** the attribution chain does not depend on any single artifact. It survives removal of the User-Agent evidence (M012's flawed method), and rests instead on TCP-stack fingerprinting validated against two known controls, corroborated by an independent TCP-timestamp clock split, and confirmed consistent across all ten in-scope streams.


## 4. Confirmed Exfiltrated/Accessed Data
No data was exfiltrated from the university. The "payload" in this case is the harassing content itself, recovered verbatim from the HTTP POST bodies and **confirmed delivered** by the receiving servers:

**Message 1 — 2008-07-22 06:02:57 UTC, via sendanonymousemail.net (stream 1631, frame 80614)**
- To: `lilytuckrige@yahoo.com`
- Spoofed sender: `the_whole_world_is_watching@nitroba.org`
- Subject: **"Your class stinks"**
- Body: *"Why do you persist in teaching a boring class? We don't like it. We don't like you."*
- Delivery: **CONFIRMED** — HTTP 200 + "Your message has been sent!"

**Message 2 — 2008-07-22 06:04:24 UTC, via willselfdestruct.com (stream 1701, frame 83601)**
- To: `lilytuckrige@yahoo.com`
- From: (empty — anonymous)
- Subject: **"you can't find us"**
- Body: *"and you can't hide from us. Stop teaching. Start running."*
- Delivery: **CONFIRMED** — HTTP 302 → `/secure/success`

*Note on severity: message 2 contains an implied threat to the victim's physical safety ("Stop teaching. Start running."), which elevates this above a student prank and may constitute criminal harassment/stalking depending on jurisdiction.*

## 5. MITRE ATT&CK Mapping

*Framework caveat: ATT&CK models adversary behaviour in enterprise intrusions. This is a targeted-harassment case by an unprivileged individual — there is no exploitation, no malware, no C2 and no lateral movement. Rows marked **(approx.)** are the closest available technique rather than an exact fit, and are labelled as such deliberately rather than forced.*

| Tactic | Technique | ID | Evidence in this case |
|---|---|---|---|
| Reconnaissance | Search Open Websites/Domains | **T1593** | Five attacker searches 05:57:38–06:01:24 UTC inside the VM: *"how to annoy people"*, *"sending anonymous mail"*, *"i want to harass my teacher"*, *"can I go to jail for harassing my teacher?"*, *"send anonymous mail"*; plus visits to `annoy.com`, `email.about.com` and `clintonfein.com` (harassment law) [M014, M016, M017] |
| Resource Development | Acquire Infrastructure: Web Services | **T1583.006** (approx.) | Selected and used two third-party anonymous-remailer web services — `sendanonymousemail.net` (69.80.225.91) and `willselfdestruct.com` (69.25.94.22) — as disposable sending infrastructure requiring no account [M004] |
| Initial Access | Hardware Additions | **T1200** (approx.) | Attacker's own MacBook joined the unsecured, passwordless dorm Wi-Fi at 04:29:51 UTC, obtaining 192.168.15.4 behind the room's NAT. No credential was required and no authorisation existed [M005] |
| Defense Evasion | Proxy: Multi-hop Proxy | **T1090.003** (approx.) | Both messages were relayed through third-party remailers so the victim's mail headers would show the remailer, not the sender — deliberately breaking the sender↔source link. This is the technique that defeated the university's first investigation [M004, M007] |
| Defense Evasion | Hide Artifacts | **T1564** (approx.) | A **Windows XP VMware guest** was used as a disposable, isolated compartment with its own browser profile, cookie jar and TCP/IP stack. VM lifetime 05:41:26–06:05:10 (23m44s), terminated 46 s after the final send, while the operator's normal Mac session continued concurrently [M015, M017] |
| Defense Evasion | Masquerading | **T1036** | Sender address on message 1 spoofed to `the_whole_world_is_watching@nitroba.org` — a fabricated university-domain address implying a group of senders rather than an individual [M004] |
| Defense Evasion | Impersonation | **T1656** (approx.) | Message text uses the collective *"we"/"us"* (*"We don't like you"*, *"you can't find us"*) to manufacture the impression of multiple hostile parties |
| — *(attribution artifact, not an attacker technique)* | Valid Accounts | **T1078** | The OPSEC failure: the attacker's own authenticated Google session (`gausr=jcoachj%40gmail.com`, `OL_SESSION=jcoachj@gmail.com-cal`) was carried into the anonymised VM at 06:01:08, 109 s before the first threat [M007, M013, M015] |
| Impact | Establish Accounts: Email Accounts | **T1585.002** (approx.) | **Not a true fit.** The terminal objective was neither theft nor disruption but **targeted harassment and an implied threat to personal safety** — conduct ATT&CK does not model. Recorded here for completeness; the substantive characterisation belongs to criminal law, not ATT&CK [M004] |

**Techniques deliberately NOT claimed:** no Execution, Persistence, Privilege Escalation, Credential Access, Discovery, Lateral Movement, Collection, C2 or Exfiltration activity was observed. No university system was compromised, no account was breached, and no data left the institution.

## 6. Recommendations

### 6.1 Immediate — Victim Safety (hours)
1. **Treat message 2 as a credible safety concern, not a prank.** *"Stop teaching. Start running."* is an implied threat to physical safety. Engage Campus Police/Title IX now; do not route this solely through academic discipline.
2. **Preserve the victim's mailbox.** Export full RFC-822 source (all headers) of every message received at `lilytuckrige@yahoo.com`, including any that predate the capture. The remailer relay IPs in those headers corroborate the two sends reconstructed here.
3. **Do not tip the subject.** Any notice to the student before device seizure invites destruction of the VM image — the single most valuable corroborating artifact remaining.

### 6.2 Immediate — Evidence Preservation (hours to days)
4. **Seize and image the MacBook "Obsidian"** (MacBook1,1, S/N `4H6242CSVMN`, MAC `00:17:f2:e2:c0:ce`) under appropriate legal authority. **Expect an ownership challenge** — network evidence could not establish the registered owner (§3.17, §3.18), and a third party (`beth@bethr.org` or Amy Smith) may claim it. Establish who had custody at **05:41–06:05 UTC on 2008-07-22** before or during seizure.
5. **Prioritise the VMware guest.** On imaging, target the `.vmdk`/`.vmem`/`.vmsn` files and the guest's IE6 profile: `index.dat`, TypedURLs, cookies, and the form-history/autocomplete entries for the two remailer forms. A VM snapshot would preserve the sending browser's state at the moment of the offence. Absence of the VM is itself probative given it demonstrably existed on 2008-07-22.
6. **Verify and re-hash `nitroba.pcap`** against the custody hashes supplied with the case, and record the verification. All analysis in this report was read-only; the evidence file was never modified.

### 6.3 Corroboration via Legal Process (days to weeks)
7. **Google/Gmail** — subpoena subscriber records and login IP history for **`jcoachj@gmail.com`**, specifically the session active at 2008-07-22 06:01:08 UTC. This ties the account to a named person and should show source IP `140.247.62.34`.
8. **The two remailers** — preserve/subpoena `sendanonymousemail.net` and `willselfdestruct.com` for submission logs on 2008-07-22 at 06:02:57 and 06:04:24 UTC. Both should show `140.247.62.34`, independently confirming the sends outside our packet capture.
9. **Absolute Software (Computrace)** — subpoena the registered owner for **TagId `268698586` / S/N `4H6242CSVMN`**. This is the strongest remaining path to laptop ownership, since Bonjour naming was unavailable (§3.17).
10. **Facebook** — subpoena UID `588141158` (`beth@bethr.org`) only if hardware ownership must be established. Note this identity is **not** implicated in the offence.
11. **Interview, do not accuse, `amy789smith` (Amy Smith)** — her account was logged in on the same laptop. She is affirmatively excluded as the sender, but she is well placed to say **who was using that machine**, whose laptop it is, and why her session was running on it.

### 6.4 Network Remediation (immediate, and independent of this case)
12. **Remove or secure Kenny's rogue router.** An unsecured AP NAT'ing an entire dorm room behind one university IP is precisely what made the first investigation fail and what would have let a genuinely careful attacker remain anonymous.
13. **Enforce WPA2-Enterprise (802.1X) with per-user credentials** on all residential Wi-Fi, so every session maps to an authenticated identity rather than to a room.
14. **Prohibit student-installed NAT devices** by policy, and scan for them — a rogue NAT collapses attribution for every device behind it.
15. **Retain DHCP and NAT-translation logs** with sufficient duration to map internal IP + MAC + timestamp to a user. Had this existed, attribution would have taken minutes, not a full packet capture.

### 6.5 Institutional / Process
16. **Record why the first investigation failed** — the university correctly traced the mail to the room and then stopped, because NAT hid the individual. The lesson is that IP-level attribution ends at the NAT boundary; identity-level attribution requires either authenticated network access or full content capture.
17. **Note the analytical lesson for future cases:** User-Agent–based host separation produced a **false conclusion** in this investigation (M012) and was overturned by TCP-stack fingerprinting validated against known controls (M013/M015). Where two environments share one IP, prefer non-spoofable transport-layer signals over application-layer strings.

## 7. Evidence / Chain of Custody

**Integrity statement.** The sole item of primary evidence, `cases/NITROBA/images/nitroba.pcap`, was treated as **read-only throughout**. All processing was performed by mounting the file read-only into a containerised SIFT workstation; no tool wrote to, reordered, or re-encoded the capture. Every derived artifact below was written to `cases/NITROBA/scratch/` and is reproducible from the original.

### 7.1 Derived Artifacts
| Artifact | How Discovered / Produced | Mission Card |
|----------|----------------|--------------|
| `cases/NITROBA/images/nitroba.pcap` | Provided as case evidence (94,410 packets, 2008-07-22 01:51:07–06:13:47 UTC) | [001](missions/001-mission-data-analyst-evidence-inventory.md) |
| `cases/NITROBA/docs/NITROBA-Scenario.pdf` | Provided as case scenario document | [002](missions/002-mission-sniper-forensics-extract-scenario-pdf.md) |
| `cases/NITROBA/scratch/NITROBA-Scenario.txt` | Text layer extracted from scenario PDF via pypdf | [002](missions/002-mission-sniper-forensics-extract-scenario-pdf.md) |
| `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` | Generated from nitroba.pcap via `helpers/pcap_to_parquet.py`; verified 94,410 rows | [003](missions/003-mission-sniper-forensics-pcap-to-parquet.md) |
| Hostile POST bodies (streams 1631, 1701) | `tshark` HTTP POST hunt for `lilytuckrige`, then full TCP stream follow | [004](missions/004-mission-data-analyst-h1-hostile-email-flow.md), [007](missions/007-mission-sniper-forensics-validate-attribution-streams.md) |
| Dorm device/MAC map | Endpoint + ARP/DHCP analysis over `packets.parquet` | [005](missions/005-mission-data-analyst-h2-device-mapping.md) |
| Computrace device fingerprint (frame 22757, stream 468) | Attribution sweep of 192.168.15.4 non-browser traffic | [006](missions/006-mission-sniper-forensics-h3-identity-artifacts.md), [007](missions/007-mission-sniper-forensics-validate-attribution-streams.md) |
| `jcoachj@gmail.com` Google session (streams 1601/1602) | Stream-level validation of identity artifacts | [007](missions/007-mission-sniper-forensics-validate-attribution-streams.md) |
| Send-window exclusivity proof | SQL aggregation over `packets.parquet` for 05:58–06:08 | [008](missions/008-mission-data-analyst-exclusivity-and-dualmac.md) |
| `h3_user_agents.txt` / send-window HTTP narrative | Per-frame User-Agent extraction | [009](missions/009-mission-sniper-forensics-ua-adjudication-send-window.md) |
| `beth@bethr.org`, `amy789smith`, Flickr identities | Corroborating identity sweep of 192.168.15.4 | [010](missions/010-mission-sniper-forensics-corroborating-identity-sweep.md), [011](missions/011-mission-sniper-forensics-yahoo-amy-conflict.md) |
| **TCP SYN stack classification (10 streams)** | Initial-window + window-scale + TCP-timestamp analysis, validated against two known Mac controls | [013](missions/013-mission-sniper-forensics-ttl-os-fingerprint.md), [015](missions/015-mission-sniper-forensics-stack-reconciliation.md) |
| Yahoo session reconstruction | YMSG protocol decode + Yahoo HTTP session follow | [014](missions/014-mission-sniper-forensics-yahoo-session-reconstruction.md) |
| *"can I go to jail…"* search (frame 74920) | Verbatim reassembly by two independent methods | [016](missions/016-mission-sniper-forensics-gotojail-search.md) |
| `m016_all_http_5950_0602.txt` | Bulk HTTP request extraction, 05:50–06:02 | [016](missions/016-mission-sniper-forensics-gotojail-search.md) |
| **Complete premeditation search trail + VM session bounds** | All search queries extracted and each carrier stream stack-classified | [017](missions/017-mission-sniper-forensics-vm-activity-profile.md) |
| Device-ownership analysis (negative) | DHCP / NetBIOS / Computrace payload / per-identity stack review | [018](missions/018-mission-sniper-forensics-device-ownership.md) |
| `m019_mdns_names.txt` (negative result) | mDNS/NBNS/LLMNR sweep — 0 packets, confirmed by two methods | [019](missions/019-mission-sniper-forensics-bonjour-ownership.md) |

### 7.2 How the Central Conclusion Was Reached
The attribution rests on four independent legs; no single artifact carries it:

1. **Content** — both hostile POST bodies were recovered verbatim from the capture, with server-side delivery confirmations (HTTP 200 "Your message has been sent!"; HTTP 302 → `/secure/success`). *[M004, M007]*
2. **Source host** — both POSTs originate from 192.168.15.4, and that host is the **sole** HTTP-POST emitter on the network across the entire send window. *[M008]*
3. **Execution environment** — the sends, the `jcoachj@gmail.com` login and every premeditation search share one TCP-stack signature (window 64240 / wscale 0) distinct from the Mac host's (65535 / wscale 1–3). The method was validated against two streams of known provenance and corroborated by a separate TCP-timestamp clock range. *[M013, M015]*
4. **Identity** — that environment contained exactly one human identity for the whole capture: `jcoachj@gmail.com`, whose session cookie was set 109 seconds before the first threat. *[M007, M015]*

Motive and intent are supplied independently by the attacker's own searches, notably *"i want to harass my teacher"* at 05:58:07. *[M017]*

### 7.3 Corrections Made During the Investigation
Recorded for transparency, since two intermediate conclusions were **wrong and were overturned**:
- **M012** classified execution environments using **User-Agent strings** and concluded the VM contained a second identity (`amy789smith`). This was rejected as circular — a UA is an application-layer string, trivially inconsistent across clients, and the specific anomaly was explained by Adium/libpurple hard-coding the Windows Yahoo Messenger version `8.1.0.249`. M012's VM start time (05:02:05) was likewise wrong; the correct value is **05:41:26** *[M017]*.
- **M014** correctly decoded the YMSG protocol but inherited M012's environment classification and therefore placed `amy789smith` in the VM. **M015** re-derived every SYN and refuted this: stream 1045 is unambiguously Mac.
- **M013's** TTL-based approach failed outright (VMware NAT rewrites TTL) and was **reported as failed** rather than fudged; its SYN-window findings were retained and independently re-verified by M015.
- **M019** returned a clean negative and correctly attributed it to capture-point architecture rather than to device behaviour.
