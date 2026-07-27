# ⭐ CASE CONCLUSION — CLOSED (19 missions, 2026-07-01)

**SENDER OF THE HARASSING EMAILS: `jcoachj@gmail.com` — CHEM109 student "Johnny Coach". Confidence: HIGH.**

| Element | Finding |
|---|---|
| Sending host | `192.168.15.4` — Apple MacBook1,1, S/N `4H6242CSVMN`, hostname "Obsidian", MAC `00:17:f2:e2:c0:ce` |
| Sending environment | **Windows XP VMware guest** on that laptop. TCP SYN window **64240 / wscale 0** (Mac host = 65535 / wscale 1–3). VM lifetime **05:41:26–06:05:10 UTC** (23m44s) |
| Identities inside the VM | **EXACTLY ONE: `jcoachj@gmail.com`** (cookie `OL_SESSION=jcoachj@gmail.com-cal` set 06:01:08, 109 s before threat #1) |
| Statement of intent | Google search **"i want to harass my teacher"** at **05:58:07** (VM, stream 1473) |
| Threat #1 | 06:02:57 — sendanonymousemail.net, spoofed `the_whole_world_is_watching@nitroba.org`, subj "Your class stinks" — DELIVERED |
| Threat #2 | 06:04:24 — willselfdestruct.com, subj "you can't find us", *"Stop teaching. Start running."* — DELIVERED |
| **EXCLUDED** | `amy789smith` (Amy Smith), `beth@bethr.org`, Flickr `89101607@N00`, `mylady.ixchel@gmail.com` — **all on the Mac host stack, never in the VM** |
| Laptop ownership | **UNDETERMINED** by network evidence (M018/M019). mDNS/NBNS/LLMNR = 0 packets — capture point was upstream of the AP. Requires legal process (Absolute Software TagId `268698586`) |

**Methodological warnings for any future work on this case:**
- **DO NOT use User-Agent strings to separate the two execution environments.** This produced a false conclusion in M012 (Adium/libpurple hard-codes Windows YM version `8.1.0.249` from a Mac). Use TCP SYN window + window-scale, validated against known-provenance control streams (M013/M015).
- M012's VM-start time of 05:02:05 is **WRONG**. Correct value: **05:41:26** (M017).
- TTL-based OS fingerprinting **does not work here** — VMware NAT rewrites TTL (M013).

Full analysis: `cases/NITROBA/docs/case_report.md`.

---

# Data Inventory
- PATH: `cases/NITROBA/images/nitroba.pcap` TYPE: Packet capture (network evidence) SIZE: 56,180,821 bytes (≈54 MB) MTIME: 2026-06-03 13:39:12 UTC MD5: 9981827f11968773ff815e39f5458ec8 SHA1: 65656392412add15f93f8585197a8998aaeb50a1 SHA256: 2b77a9eaefc1d6af163d1ba793c96dbccacb04e6befdf1a0b01f8c67553ec2fb PACKET_COUNT: 94,410 CAPTURE_START: 2008-07-22T01:51:07.095278+00:00 CAPTURE_END: 2008-07-22T06:13:47.046029+00:00 DURATION: 15,759.95 seconds (~4h 22m) FILE_TYPE: Wireshark/tcpdump pcap Ethernet STATUS: Inventoried by Mission 001 (2026-07-26); capinfos metadata extracted and Parquet converted by Mission 003 (2026-07-26)
- PATH: `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` TYPE: Parquet (queryable packets table) ROWS: 94,410 TABLE_NAME: packets COLUMNS: timestamp, source_ip, dest_ip, source_port, dest_port, protocol, length, info, filename_path, imagename MIN_TIMESTAMP: 2008-07-22T01:51:07.095278+00:00 MAX_TIMESTAMP: 2008-07-22T06:13:47.046029+00:00 STATUS: Created by Mission 003 (2026-07-26); ready for SQL hunting
- PATH: `cases/NITROBA/docs/NITROBA-Scenario.pdf` TYPE: Case scenario document (4,401,268 bytes) STATUS: Text extraction pending Mission 002

# Case Background / Scenario
*(Extracted from NITROBA-Scenario.pdf — Mission 002, 2026-07-26)*

**Summary:** Harassment investigation at Nitroba State University (NSU).

**Victim:** Lily Tuckrige — teaches Chemistry CHEM109 (summer session). Personal email: lilytuckrige@yahoo.com. She has been receiving harassing emails and suspects one of her students.

**Key IP:** 140.247.62.34 — resolves to G24.student.nitroba.org (a campus dorm room).

**Dorm Room G24 Occupants:** Alice, Barbara, and Candice.
- Barbara's boyfriend Kenny installed an open (no-password) Wi-Fi router in the room.
- Nitroba provides 10 Mbps Ethernet per room (no campus Wi-Fi).

**Evidence Collected:** NSU IT set up a packet sniffer; captured network traffic is in `nitroba.pcap`.

**CHEM109 Class List (potential suspects):**
- Amy Smith, Burt Greedom, Tuck Gorge, Ava Book, Johnny Coach, Jeremy Ledvkin, Nancy Colburne, Tamara Perkins, Esther Pringle, Asar Misrad, Jenny Kant

**Investigative Questions (from scenario):**
1. Map the Nitroba dorm room network.
2. Find the TCP flow containing the hostile email to lilytuckrige@yahoo.com and identify the sending browser/client.
3. Identify other TCP connections belonging to the attacker.
4. Find identifying information in those connections to attribute the harassment to a specific person.

## Device Map
*(Built by Mission 005, 2026-07-26 — SQL triage of packets table)*

### Network Topology
- **NSU Router (gateway):** 192.168.1.254 — MAC `00:1d:6b:99:98:68`; ARP-sweeps wired LAN; DNS forwarder
- **Kenny's Wi-Fi Router:** 192.168.1.64 (WAN, MAC `00:1d:d9:2e:4f:61`) / 192.168.15.1 (LAN, MAC `00:1d:d9:2e:4f:60`); consecutive MACs confirm same device; bridges wired 192.168.1.0/24 to wireless 192.168.15.0/24

### Local Host Inventory
| IP | MAC | Pkts Sent | First Seen UTC | Last Seen UTC | Device Evidence |
|---|---|---|---|---|---|
| 192.168.15.4 | 00:17:f2:e2:c0:ce | 34,582 | 04:29:51 | 06:13:47 | TOP TALKER; Apple Bonjour/DNS-SD; Akamai CDN; weather.com; dual-stack IPv6 |
| 192.168.1.64 | 00:1f:f3:5a:77:9b / 00:1d:d9:2e:4f:61 | 7,060 | 01:51:07 | 06:12:13 | Apple MobileMe (idisk.mac.com); weather.com; active full capture |
| 192.168.1.254 | 00:1d:6b:99:98:68 | 4,969 | 01:51:07 | 06:11:38 | NSU router (ARP sweep; DNS resolver) |
| 192.168.15.1 | 00:1d:d9:2e:4f:60 | 2,218 | 03:05:29 | 06:13:44 | Kenny's Wi-Fi router — LAN interface |
| 192.168.15.5 | (unknown) | 72 | 04:29:54 | 06:12:47 | Minor wireless client |
| 192.168.1.5 | 00:0a:95:69:38:cc | 49 | 01:53:13 | 06:06:55 | Low-activity wired client |
| 10.0.1.5 | (unknown) | 37 | 04:33:57 | 04:37:01 | Possible VPN/tunnel endpoint |
| 192.168.15.8 | (unknown) | 13 | 06:11:52 | 06:13:44 | Transient wireless client (capture end) |
| 192.168.15.7 | (unknown) | 11 | 04:37:29 | 04:37:39 | Transient wireless client |
| 10.0.1.200 | (unknown) | 8 | 06:11:47 | 06:11:49 | Possible VPN/tunnel |
| 192.168.15.2 | (unknown) | 2 | 02:12:58 | 03:19:56 | Minimal activity |

### Key Device Observations
- **192.168.15.4** (Apple device, MAC `00:17:f2:e2:c0:ce`): Only active 04:29–06:13 UTC, generates 36% of all capture traffic; strong Bonjour/DNS-SD indicates Mac OS X or iPhone (2008 era).
- **192.168.1.64** (Apple device): Queries `idisk.mac.com` (MobileMe) and weather.com; active entire 4h22m capture.
- **User-Agent**: NOT extractable from `packets.info` column — requires sniper packet reconstruction for H3.
- **DHCP/NBNS/MDNS**: Not captured as named protocols; Bonjour proxy via DNS only.

# Compromised Accounts

# Known Malicious IPs & Domains
- IP: 69.80.225.91 DOMAIN: www.sendanonymousemail.net DESCRIPTION: Anonymous email service; POST /send.php sent from 192.168.15.4 at 2008-07-22T06:02:57Z. Status: possible failed attempt (CAPTCHA reload observed).
- IP: 69.25.94.22 DOMAIN: www.willselfdestruct.com DESCRIPTION: Anonymous email service (self-destructing); POST /secure/submit sent from 192.168.15.4 at 2008-07-22T06:04:24Z. SUCCESS confirmed by GET /secure/success. PRIME CANDIDATE for hostile email delivery.
- IP: 209.53.113.23 DOMAIN: search.namequery.com DESCRIPTION: Received 333 HTTP POST / packets from 192.168.15.4; possible DNS hijacking/surveillance tool. Needs investigation.

# Suspicious Files & Staging Directories

# Decoded Payloads & Scripts

# Confirmed Exfiltrated/Accessed Data

## Hostile Emails Sent to Victim (lilytuckrige@yahoo.com) — Mission 007 (2026-07-26)

**Email 1 — stream 1631, frame 80614, 2008-07-22T06:02:57Z, sendanonymousemail.net**
- To: lilytuckrige@yahoo.com
- Sender field: the_whole_world_is_watching@nitroba.org
- Subject: "Your class stinks"
- Full message: "Why do you persist in teaching a boring class? We don't like it. We don't like you."
- Result: CONFIRMED SENT — HTTP 200 OK + "Thank You Your message has been sent!"
- Session cookie: PHPSESSID=762adba03236142ccec305f6a20aaffa

**Email 2 — stream 1701, frame 83601, 2008-07-22T06:04:24Z, willselfdestruct.com**
- To: lilytuckrige@yahoo.com
- From: (empty — anonymous)
- Subject: "you can't find us"
- Full message: "and you can't hide from us. Stop teaching. Start running."
- Result: CONFIRMED SENT — HTTP 302 → /secure/success

# Attacker Attribution

*(Mission 007, 2026-07-26 — stream reassembly validation)*

- **Suspect name:** Johnny Coach (CHEM109 class member)
- **Email account:** jcoachj@gmail.com — confirmed active at 06:01:08Z on 192.168.15.4 (URL param gausr=jcoachj%40gmail.com; Set-Cookie OL_SESSION=jcoachj@gmail.com-cal in stream 1601)
- **Device:** Apple MacBook1,1 — hostname "Obsidian" — serial 4H6242CSVMN — HDD NW81T6325527 (primary), K3376NB5022 (secondary)
- **IP:** 192.168.15.4 (Wi-Fi, Kenny's router 192.168.15.0/24)
- **MAC:** 00:17:f2:e2:c0:ce (Apple; active 04:29–06:13 UTC 2008-07-22)
- **Computrace/Absolute beacon:** frame 22757, stream 468, 2008-07-22T04:36:48Z — src IP 192.168.15.4, src MAC 00:17:f2:e2:c0:ce — CONFIRMED device identity
- **User-Agent (hostile sends and Gmail):** Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) — CONFIRMED PER-FRAME (Mission 009, 2026-07-26): frame 80614 (stream 1631, sendanonymousemail.net POST), frame 83601 (stream 1701, willselfdestruct.com POST), streams 1601/1602 (Google Calendar jcoachj@gmail.com) — all IE6/WinXP UA. Runs in Windows XP VM inside Mac (VMware vmnet8 NAT IP 192.168.194.1). M006 claim of Firefox/2.0.0.16 REFUTED — Firefox (922 send-window requests) was used only for Mac-side eBay/shopping browsing, NEVER for hostile sends. M007 was CORRECT.
- **Activity timeline:**
  - 04:36:48 — Computrace beacon from 192.168.15.4 (device fingerprint)
  - 06:01:08 — Gmail/GCal session for jcoachj@gmail.com
  - 06:02:57 — Hostile email 1 sent (sendanonymousemail.net)
  - 06:04:24 — Hostile email 2 sent (willselfdestruct.com)

## Mission 011 YMSG Key-Value Analysis (2026-07-26) — Amy Smith Role Determination

- **YMSG KEY 1 = amy789smith CONFIRMED**: Raw hex bytes from stream 1865 YMSG payload: `31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80` — Key `1` (ASCII "31") → delimiter `c0 80` → value `amy789smith`. YMSG key 1 = the logged-in local user's own Yahoo ID. Amy Smith was the AUTHENTICATED local Yahoo Messenger user at 192.168.15.4 at 06:09:59 UTC.
- **KEY 5 ABSENT**: No remote peer (key 5) or sender-for-inbound (key 4) found in the YMSG packet. Recipient identity cannot be determined from this packet alone.
- **SOURCE MAC CONFIRMED**: Frame 90455 (TCP SYN, first frame of stream 1865): `Ethernet II, Src: Apple_e2:c0:ce (00:17:f2:e2:c0:ce)`. No second physical device. Same MacBook Obsidian responsible for hostile emails.
- **AMY SMITH STATUS**: CO-EQUAL SUSPECT. Both `jcoachj@gmail.com` (06:00–06:04 UTC, hostile emails) and `amy789smith` (06:09:59 UTC, Yahoo Messenger) were active on 192.168.15.4 (MAC `00:17:f2:e2:c0:ce`) within a 9-minute window on 2008-07-22. The existing case theory (Johnny Coach sole sender) is challenged but not refuted — the hostile POSTs carry jcoachj credentials; the Yahoo activity 5m35s later carries amy789smith credentials.
- **YAHOO SESSION**: No separate login stream captured. Session pre-authenticated via T= cookie. No evidence session predates MacBook joining network at 04:29:51 UTC.
- **NEW LEAD**: YMSG port-5050 traffic may contain Key 5 (recipient ID) for the file transfer initiated by amy789smith — spawning a follow-up search is recommended.

# Pending Investigative Leads
- LEAD: Wi-Fi attacker IP 192.168.15.4 — enumerate ALL TCP connections from this IP to build full activity profile for attribution (Mission 004 finding).
- LEAD [RESOLVED by Mission 007]: Reassemble TCP stream 192.168.15.4:35876 → 69.80.225.91:80 — email confirmed sent (HTTP 200 + "Thank You Your message has been sent!").
- LEAD [RESOLVED by Mission 007]: Reassemble TCP stream 192.168.15.4:36044 → 69.25.94.22:80 — lilytuckrige@yahoo.com confirmed as recipient; full message extracted.
- LEAD [RESOLVED by Mission 008]: Gmail session from 192.168.1.64 → mail.google.com (74.125.19.19), session key ik=4233eca8e4, 03:44:36 UTC — account confirmed as `mylady.ixchel@gmail.com` (from gausr= URL param). IP 192.168.1.64 was in Kenny's router WAN MAC era (00:1d:d9:2e:4f:61) at this time; traffic was NAT'd from 192.168.15.x wireless subnet. Identity likely one of dorm occupants (Alice/Barbara/Candice). Reassemble stream for inbox/sent content.
- LEAD: DNS queries to mail.bethr.org (→208.97.132.20), mail.dreamhost.com (→208.113.200.13), _telnet._tcp.mail.m57.biz — investigate as possible additional email accounts or mail servers used by suspects.
- LEAD: search.namequery.com:80 (209.53.113.23) — 333 HTTP POST / packets from 192.168.15.4 starting ~04:36 UTC. Investigate as possible DNS hijacking or rogue DNS tool.
- LEAD [RESOLVED by Mission 008]: m57jean AOL SyncML session (stream 266, 01:56 UTC) on 192.168.1.64 — falls in Kenny's router WAN MAC era 1 (00:1d:d9:2e:4f:61); traffic NAT'd from 192.168.15.x Wi-Fi subnet. Not directly from the Apple device 00:1f:f3:5a:77:9b.
- LEAD [Mission 008 NEW]: Gmail account `mylady.ixchel@gmail.com` — active on 192.168.1.64 at 03:44:36 UTC. Behind Kenny's router. Dorm-room identity candidate. Spawn stream reassembly mission.
- LEAD [Mission 008 NEW]: Apple device MAC `00:1f:f3:5a:77:9b` — briefly on wired LAN (192.168.1.0/24), answered ARP for 192.168.1.64 at 03:09:08 UTC. Identity unknown. Investigate what traffic this device sent while on the wired segment.
- LEAD: Reassemble Gmail session streams (192.168.15.4, stream 1601-1617 range, 06:00-06:03 UTC) to extract full jcoachj@gmail.com activity log.
- LEAD: Reassemble Absolute agent stream 468 for owner registration info.
- LEAD: Reassemble Yahoo Messenger stream 1865 to identify Yahoo username.

## Mission 008 Findings (2026-07-26) — Exclusivity + Dual-MAC Resolution
- **EXCLUSIVITY CONFIRMED**: During send window 05:58–06:08 UTC, 192.168.15.4 sent 6,043 packets (exclusive HTTP POST sender); all other local hosts sent ONLY ARP/UPnP SSDP/DNS infrastructure traffic. Zero alternative senders for hostile email POSTs.
- **DUAL-MAC RESOLVED**: IP 192.168.1.64 held by Kenny's router WAN MAC `00:1d:d9:2e:4f:61` in Era 1 (01:51–01:58) and Era 3 (03:43+). Brief Era 2 at 03:09:08 UTC when Apple device `00:1f:f3:5a:77:9b` directly answered ARP on wired LAN. Router went offline ~02:08–03:09 (reboot, consistent with 192.168.15.1 first-seen at 03:05:29 from Mission 005).
- **GMAIL-IK IDENTITY**: Session key `ik=4233eca8e4` = account `mylady.ixchel@gmail.com` (URL param gausr= at 03:44:36 UTC; 192.168.1.64; Era 3 router WAN MAC). Traffic NAT'd from 192.168.15.x wireless subnet.
- **m57jean ERA**: SyncML at 01:56 UTC falls in Era 1 (router WAN MAC `00:1d:d9:2e:4f:61`); traffic NAT'd from 192.168.15.x wireless subnet.

## H3 Identity Artifact Findings (Mission 006, 2026-07-26)
- **PRIME SUSPECT**: `jcoachj@gmail.com` = Johnny Coach (CHEM109 class member). Gmail account observed actively logged in on 192.168.15.4 at 06:00-06:01 UTC (frames 79732, 77710-77711) immediately before hostile email POSTs. Google Calendar also loaded for `jcoachj@gmail.com`.
- **HOSTILE EMAIL 1 CONFIRMED**: Frame 80614, 2008-07-22T06:02:57Z, stream 1631 — POST to www.sendanonymousemail.net/send.php from 192.168.15.4: `email=lilytuckrige@yahoo.com`, `sender=the_whole_world_is_watching@nitroba.org`, `subject=Your class stinks`.
- **HOSTILE EMAIL 2 CONFIRMED**: Frame 83601, 2008-07-22T06:04:24Z, stream 1701 — POST to www.willselfdestruct.com/secure/submit from 192.168.15.4: `to=lilytuckrige@yahoo.com`, `subject=you can't find us`, `message=...Stop teaching. Start running.`
- **DEVICE FINGERPRINT**: Apple MacBook1,1, serial `4H6242CSVMN`, hostname `Obsidian`, HDD serial `NW81T6325527`, VMware NIC `vmnet8` (192.168.194.1). Source: Absolute persistence agent POST to search.namequery.com, stream 468, 04:36:48 UTC.
- **WINDOWS VM ON ATTACKER MAC**: 192.168.15.4 emits MSIE 6.0/Windows NT 5.1 UA (475 requests) and Windows-Update-Agent (10 requests) — Windows XP VM running inside Mac OS X.
- **AOL ACCOUNT**: `m57jean` — wired host 192.168.1.64, SyncML contact sync to sync.aol.com/m57jean (stream 266, 01:56 UTC).
- **FACEBOOK** [RESOLVED by Mission 010]: 192.168.15.4, stream 624 — user active on Facebook at 04:51-04:52 UTC (Mac OS X Firefox). Registered email: `beth@bethr.org`, user ID `588141158`. NOT on CHEM109 roster. Accepted "Adopt Me!" app invite from peer `533253664`.
- **YAHOO MESSENGER** [RESOLVED by Mission 010]: 192.168.15.4, stream 1865 — file transfer to filetransfer.msg.yahoo.com at 06:09:59 UTC (Windows XP IE 5.5 / VMware VM). Yahoo screen name: **`amy789smith`** = **Amy Smith, CHEM109 student**. Transferring PNG file `057f280df74aeda1a8aada6a0f218871b5417eb3.png`. Activity occurs 5m35s AFTER second hostile email.
- LEAD: Reassemble Gmail session streams (192.168.15.4, stream 1601-1617 range, 06:00-06:03 UTC) to extract full jcoachj@gmail.com activity log.
- LEAD: Reassemble Absolute agent stream 468 for owner registration info.
- LEAD [RESOLVED by Mission 010]: Reassemble Yahoo Messenger stream 1865 to identify Yahoo username → `amy789smith` = Amy Smith (CHEM109).
- LEAD: Gmail session on 192.168.1.64 (key ik=4233eca8e4, stream 347, 03:44 UTC) — identify account (separate from attacker).

## Mission 010 Non-Google Identity Sweep Findings (2026-07-26)
- **FACEBOOK IDENTITY on 192.168.15.4**: Email `beth@bethr.org`, Facebook UID `588141158`, active 04:51–04:52 UTC via Mac OS X Firefox. "Beth" is NOT on the CHEM109 class roster. The `bethr.org` domain appears in prior leads (mail.bethr.org). This identity does NOT corroborate Johnny Coach.
- **YAHOO MESSENGER IDENTITY on 192.168.15.4**: Screen name `amy789smith`, active 06:09:59 UTC via Windows XP IE 5.5 (VMware VM). **Amy Smith is on the CHEM109 class roster**. Activity is 5m35s post-hostile-email. This does NOT corroborate Johnny Coach.
- **THREE IDENTITIES on one device**: The MacBook "Obsidian" (192.168.15.4) hosted: `beth@bethr.org` (Facebook/Mac OS X, 04:51), `jcoachj@gmail.com` (Gmail+hostile email/Windows XP VM, 06:00-06:04), and `amy789smith` (Yahoo Messenger/Windows XP VM, 06:09). Multi-identity device suggests shared/borrowed usage.
- **VERDICT (Mission 010)**: Non-Google artifacts are INCONCLUSIVE/PARTIALLY CONTRADICTING as to Johnny Coach. Google attribution (`jcoachj@gmail.com` sending hostile emails) remains valid. Amy Smith (`amy789smith`) is now a PRIME ALTERNATE SUSPECT who requires dedicated investigation.
- **NEW SUSPECT**: Amy Smith — CHEM109 student, Yahoo Messenger `amy789smith`, active on attacker device 06:09:59 UTC.
- LEAD [NEW - Mission 010]: Amy Smith (`amy789smith`) Yahoo Messenger active on 192.168.15.4 at 06:09:59 UTC. Spawn mission to analyze her full activity on device.
- LEAD [NEW - Mission 010]: Flickr user `89101607@N00` — accessed three times from 192.168.15.4 (04:49, 04:51, 05:21 UTC). Real-name resolution pending.
- LEAD [NEW - Mission 010]: Windows Live (Hotmail) login page loaded at 05:57 and 05:59 UTC from 192.168.15.4. No POST credentials captured — investigate additional streams.

## Mission 014 Yahoo Messenger Session Reconstruction (2026-07-26)

- **YAHOO SESSION VERDICT: LONG-RUNNING BACKGROUND/AUTO-LOGIN.** `amy789smith` Yahoo! Messenger session was active on 192.168.15.4 since **at least 04:43:46Z** — 86+ minutes before the first hostile email (06:02:57Z). Auto-login does NOT prove Amy Smith was at the keyboard during the sends.
- **amy789smith LITERAL STRING**: First occurrence frame 90388 at **06:09:59Z**; last frame 90580 at **06:10:00Z**. NO occurrences anywhere else in the 94,410-frame capture.
- **PORT 5050 YMSG FIRST PACKET**: Frame 90372, **06:09:58Z** (TCP SYN → 66.163.181.179:5050). New connection initiated 5m34s after second hostile email. Full auth exchange: YMSG service 0x0057 (verify) then 0x0054 (auth challenge).
- **YM EARLY SESSION EVIDENCE**: Frame 24700 (04:43:49Z) — `img.avatars.yahoo.com` buddy avatar downloads (5 unique buddy photos: YM loads these on login). Frame 48627 (05:02:05Z) — `address.yahoo.com/yab?prog=ymsgr&prog-ver=8.1.0.249&diffs=1` with T= auth cookie and UA `MSIE 5.5` — YM already authenticated.
- **CLIENT IDENTIFIED**: Yahoo! Messenger for Windows **version 8.1.0.249** running in Windows XP VMware VM (UA: `Mozilla/4.0 (compatible; MSIE 5.5)`). NOT Adium/libpurple.
- **OTHER YM SCREEN NAMES**: None found. No buddy screen names captured.
- **NEW CRITICAL LEAD**: Frame 74920 (05:58:32Z, stream 1540) — Yahoo Answers search: **`"can I go to jail for harassing my teacher?"`** — searched from 192.168.15.4 exactly **4 minutes and 25 seconds before the first hostile email**. Extremely high evidentiary value.
- **OUTPUT FILES**: `/scratch/nitroba.pcap/m014_amy_all_frames.txt`, `/scratch/nitroba.pcap/m014_yahoo_traffic.txt`

## Mission 013 TCP Stack Fingerprinting Findings (2026-07-26)

- **TTL METHOD INVALID**: VMware NAT on the host Mac resets TTL to Mac default (64); after one hop through Kenny's router all packets from 192.168.15.4 arrive at TTL 63. No bimodal split. TTL histogram: 33,392@63, 1,161@64, 1@126. Control validation FAILS — both known-Mac frames (32229, 22757) show TTL 63, identical to known-VM frames (80614, 83601, 77508). UA vs TTL: every UA (Mac and Windows) appears at TTL 63 with no distinction.
- **TCP SYN WINDOW FINGERPRINT VALID**: Initial SYN window size separates stacks cleanly: Mac OS X=65535, Windows XP VM=64240. Both Mac controls validate (streams 468/624: window=65535). Both hostile-email streams validate (1631/1701: window=64240).
- **FRAME 90504 (amy789smith Yahoo) = MAC OS X NATIVE**: Stream 1865 SYN window=65535, matching Mac controls. M010/M012 classification of this as "Windows XP IE 5.5 (VMware VM)" is REFUTED by TCP stack evidence. Confidence: High.
- **MSIE 5.5 UA IS MAC-SIDE**: `Mozilla/4.0 (compatible; MSIE 5.5)` (3 requests, frame 90504/stream 1865) has Mac-native SYN signature (window=65535). It is a hardcoded application UA (consistent with Adium/Mac Yahoo client), NOT a genuine Windows browser. Prior attribution of amy789smith to Windows XP VM is incorrect.
- **HOSTILE EMAILS CONFIRMED VM**: Streams 1631 (sendanonymousemail.net, frame 80614) and 1701 (willselfdestruct.com, frame 83601) have SYN window=64240 → Windows XP VM. Confirms jcoachj@gmail.com acted from the Windows VM environment.
- **AMY SMITH REVISED**: amy789smith Yahoo Messenger activity (frame 90504, stream 1865, 06:09:59 UTC) originated from Mac OS X native stack, NOT the Windows XP VM. Amy Smith used the Mac-side Adium/Yahoo client, not IE in the VM. The hostile email sender (jcoachj VM) and Amy Smith (Mac-side) represent two separate environments on the same device.

## Mission 015 TCP Stack Reconciliation — DEFINITIVE CLASSIFICATION (2026-07-26)

**M013 CONFIRMED / M014 REJECTED (TCP-stack grounds only).**

- **STREAM 1865 SYN CONFIRMED CAPTURED**: Frame 90455, window=65535, wscale=3, TSval=936586659, options MSS|NOP|WScale|NOP|NOP|Timestamps|SACK. M013 read the correct SYN. M014's "Windows VM" conclusion was based solely on the `prog-ver=8.1.0.249` User-Agent string — explicitly disallowed reasoning. It is now falsified by primary stack evidence.

- **FRAME 48627 = STREAM 1045** (address.yahoo.com/yab?prog=ymsgr&prog-ver=8.1.0.249, 05:02:05 UTC). SYN frame 48624, window=65535, wscale=1 → **Mac OS X**. The `prog-ver=8.1.0.249` request originated from the Mac, not the VM. `prog-ver` is a Yahoo YMSG protocol-version field hard-coded by Mac clients (Adium/libpurple) for server compatibility — NOT evidence of a Windows build.

- **COMPLETE SYN CLASSIFICATION TABLE** (two discriminators: window size + wscale):
  | Stream | SYN Frame | What | Window | WScale | TSval | OS |
  |--------|-----------|------|--------|--------|-------|----|
  | 468 | 22528 | Computrace (Mac ctrl) | 65535 | 3 | ~936M | Mac OS X |
  | 624 | 33784 | Facebook (Mac ctrl) | 65535 | 1 | ~734M | Mac OS X |
  | 1045 | 48624 | Yahoo sync prog-ver=8.1.0.249 | 65535 | 1 | ~734M | Mac OS X |
  | 1540 | 74913 | Yahoo Answers "go to jail" | 64240 | 0 | ~644M | Windows XP VM |
  | 1601 | 77503 | Gmail/jcoachj (VM ctrl) | 64240 | 0 | ~644M | Windows XP VM |
  | 1631 | 80611 | Hostile email 1 (VM ctrl) | 64240 | 0 | ~644M | Windows XP VM |
  | 1701 | 83597 | Hostile email 2 (VM ctrl) | 64240 | 0 | ~644M | Windows XP VM |
  | 1861 | 90372 | YMSG 5050 amy789smith | 65535 | 3 | ~936M | Mac OS X |
  | 1864 | 90423 | Yahoo addr sync amy789smith | 65535 | 3 | ~936M | Mac OS X |
  | 1865 | 90455 | filetransfer amy789smith | 65535 | 3 | ~936M | Mac OS X |

- **STREAM 1540 (Yahoo Answers "go to jail for harassing my teacher?" 05:58:32 UTC) = WINDOWS XP VM**: Window=64240, wscale=0. The incriminating search was performed from the same Windows XP VM that sent both hostile emails, 4m25s before email 1.

- **DEFINITIVE VERDICT**: The Windows XP VM was used exclusively by `jcoachj@gmail.com` (Johnny Coach) for: Yahoo Answers search (1540), Gmail (1601), hostile email 1 (1631), hostile email 2 (1701). Amy Smith's `amy789smith` Yahoo session (streams 1861/1864/1865) ran on **Mac OS X native** — a separate environment. **The Windows XP VM contained exactly ONE human identity: Johnny Coach. Attribution is decisive.** Confidence: HIGH.

- **M012 CORRECTION**: Prior classification of amy789smith as "Windows XP VM" based on MSIE 5.5 UA is SUPERSEDED. TCP stack is the primary evidence. Stream 1865 SYN is Mac OS X.

## Mission 012 Identity ↔ UA Matrix Findings (2026-07-26)
- **DECISIVE VERDICT: NO** — `jcoachj@gmail.com` is NOT the only human identity inside the Windows XP VM (MSIE 6.0/WinNT5.1 + MSIE 5.5 UAs) across the entire capture.
- **VM Identity 1 (CONFIRMED):** `jcoachj@gmail.com` — frames 77508/78571/78575, 06:00:44-06:00:56 UTC, MSIE 6.0/WinNT5.1, gausr= URI param on Google Calendar + Gmail. Hostile emails sent 06:02:57 and 06:04:24 UTC.
- **VM Identity 2 (CONFIRMED):** `amy789smith` (Amy Smith, CHEM109) — frame 90504, 06:09:59 UTC, MSIE 5.5 (Windows-only UA, VMware VM per M010), Yahoo Messenger YMSG POST body, 5m35s after hostile sends.
- **VM Anonymous:** Windows Live (Hotmail) login page loaded at 05:57:24 and 05:59:21 UTC from VM (MSIE 6.0/WinNT5.1); no credentials captured in GET URIs — possible third VM identity, unconfirmed.
- **Mac Identity 1 (CONFIRMED):** `beth@bethr.org` (Facebook UID 588141158) — frame 32229, 04:50:30 UTC, Firefox/2.0.0.16 Mac.
- **Mac Identity 2:** Flickr `89101607@N00` — frames 31901/33498/64503, 04:49-05:21 UTC, Firefox/2.0.0.16 Mac.
- **ATTRIBUTION IMPLICATION:** VM was shared by at least two human identities (jcoachj + amy789smith). Network evidence alone is INSUFFICIENT to name a single sender. The jcoachj session immediately preceded hostile sends (strongest temporal correlation), but Amy Smith's VM access 5.5 min post-sends proves the VM was not exclusively used by one person.
- **VM Corpus:** 490 requests, 05:02:05-06:09:59 UTC: MSIE 6.0/WinNT5.1 (475), Windows-Update-Agent (10), MSIE 5.5 (3), Firefox/3.0.1/WinNT5.1 (2).
- **Output files:** `scratch/nitroba.pcap/m012_vm_only_requests.txt`, `m012_vm_identities.txt`, `m012_mac_identities.txt`, `m012_vm_hosts.txt`

## Mission 017 Windows XP VM Definitive Activity Profile (2026-07-26)

- **VM TRUE ACTIVE WINDOW (CORRECTED):** 2008-07-22T05:41:26Z – 2008-07-22T06:05:10Z (23m44s). M012's "05:02:05–06:09:59" is SUPERSEDED — that window included Mac OS X streams (1045, 1865) incorrectly identified via User-Agent. Stack-verified via TCP SYN window=64240/wscale=0.
- **FIRST VM STREAM:** stream 1095, frame 51957, 2008-07-22T05:41:26Z.
- **LAST VM STREAM:** stream 1727, frame 84644, 2008-07-22T06:05:10Z.
- **VM STREAM COUNT:** 147 unique streams (window=64240, wscale=0).
- **VM HTTP ACTIVITY:** 480 HTTP requests across 63 distinct hosts.
- **COMPLETE SEARCH/RESEARCH TRAIL (URL-decoded, chronological):**
  1. 05:57:38Z — "how to annoy people" (Google, stream 1473)
  2. 05:58:01Z — "sending anonymous mail" (Google, stream 1473)
  3. 05:58:07Z — "i want to harass my teacher" (Google, stream 1473)
  4. 05:58:32Z — "can I go to jail for harassing my teacher?" (Yahoo Answers, stream 1540)
  5. 05:59:34Z — "google calendar" (Google, stream 1574, navigating to jcoachj Gmail/GCal)
  6. 06:01:24Z — "send anonymous mail" (Google, stream 1602, seeking second anonymiser)
- **IDENTITY VERDICT (STACK-VERIFIED):** `jcoachj@gmail.com` is the ONE AND ONLY human identity in the Windows XP VM. `amy789smith`, `beth@bethr.org`, and `mylady.ixchel@gmail.com` are NOT present in any VM HTTP URI. Attribution to **Johnny Coach** is DEFINITIVE.
- **ANTI-FORENSIC:** sendanonymousemail.net and willselfdestruct.com used (confirmed). Windows Live (Hotmail) login page loaded twice (05:57:23Z and 05:59:20Z) but no login POST captured — possible third anonymous email service attempted then abandoned. No Tor, no proxy, no VPN detected.
- **OUTPUT FILES:** `/scratch/nitroba.pcap/m017_vm_streams.txt` (147 streams), `m017_vm_http_requests.txt` (480 requests), `m017_vm_hosts.txt` (63 hosts), `m017_vm_search_trail.txt` (6 search queries), `m017_vm_identities.txt`.

## Mission 016 "Go To Jail" Search Reconstruction (2026-07-26)

- **SEARCH PHRASE CONFIRMED VERBATIM (dual-method):** Frame 74920, stream 1540, 2008-07-22T05:58:32.660583Z — 192.168.15.4 issued Yahoo Answers search: **`can I go to jail for harassing my teacher?`** Confirmed by: (1) TCP stream follow (`-z follow,tcp,ascii,1540`) and (2) tshark field extraction (`-T fields -e http.request.full_uri`). Both methods agree exactly.
- **HTTP REQUEST LINE:** `GET /search/search_result;_ylt=A9FJui4Od4VIL5QANivD7BR.;_ylv=3?p=can+I+go+to+jail+for+harassing+my+teacher%3F HTTP/1.1` Host: `answers.yahoo.com`
- **REFERER CHAIN:** Frame 74920 Referer = `http://answers.yahoo.com/question/index?qid=20080606160229AA5Exnf&show=7` — user was already browsing a specific Yahoo Answers Q&A page before issuing the search. Navigation: prior Q&A (qid=20080606160229AA5Exnf) → search for "can I go to jail for harassing my teacher?"
- **COOKIE IDENTITY:** Only anonymous cookies present: `B=drcsgu548atoe&b=3&s=2p` (Yahoo browser fingerprint) and `answers=...` (Yahoo Answers session). NO `Y=` or `T=` cookies — **user NOT logged into any Yahoo account**. Search is attributable to the device only, not a named Yahoo user.
- **STREAM 1549 (f3.yahoofs.com, 05:58:40Z):** Auto-loaded profile image `/mingle/46181210z983efe2a/profile/__sr_/2796.jpg` for Yahoo user ID `46181210` — content rendering from results page, not a standalone navigation. Referer: Yahoo Answers question `qid=20061027171536AARz2Zv`. No attacker identity in this URL.
- **ELAPSED TIME:** 05:58:32Z (search) → 06:02:57Z (hostile email #1) = **4 minutes 25 seconds**. Demonstrates premeditation and consciousness of guilt immediately preceding the attack.
- **UA (observation only — environment deferred to M015):** `Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)`
- **OUTPUT FILES:** `/scratch/nitroba.pcap/m016_stream_1540_yahoo_answers.txt`, `/scratch/nitroba.pcap/m016_frame_74920_fields.txt`, `/scratch/nitroba.pcap/m016_all_http_5950_0602.txt` (1182 lines, unfiltered sweep for follow-up)

## Mission 018 Device Ownership Analysis (2026-07-26)

- **COMPUTRACE BEACON (stream 468, TagId 268698586):** All owner/registrant fields empty (ComputerAsset0/1, ComputerUUID, OSProductKey, BatteryDeviceID all value=""). No customer name or account identifier visible in network payload. Hardware confirmed: MacBook1,1, S/N 4H6242CSVMN, HDD NW81T6325527 / K3376NB5022, ComputerName=Obsidian. Owner must be determined via Absolute Software subpoena referencing TagId 268698586.
- **DEVICE HOSTNAME:** "Obsidian" — custom non-default Mac hostname. In 2008, Mac OS X defaults to "<First Name>'s MacBook." The use of "Obsidian" means the owner deliberately renamed the device; NO first-name inferred from hostname. Bonjour/mDNS personal name: NOT FOUND in extracted streams.
- **MAC-SIDE PRIMARY IDENTITY:** beth@bethr.org (Facebook UID 588141158). bethr.org is a personal domain (DreamHost-hosted, MX mail.bethr.org → 208.97.132.20). Browser Accept-Language includes Hebrew (he;q=0.3). Facebook account active since Nov 2007. Display name NOT recoverable (gzip-compressed responses). "Beth" is NOT on CHEM109 roster; NOT named as G24 dorm occupant.
- **mylady.ixchel@gmail.com (stream 347, 03:44 UTC, 192.168.1.64):** No display name recoverable. Dorm occupant candidate only.
- **m57jean (stream 266, 01:56 UTC, 192.168.1.64):** No display name recoverable. Dorm occupant candidate only.
- **OWNERSHIP VERDICT (INFERENCE):** Most probable owner of MacBook "Obsidian" is a person named "Beth" (linked to beth@bethr.org, Facebook UID 588141158, Flickr 89101607@N00). She is NOT on CHEM109 roster and NOT named as a G24 occupant. Johnny Coach used a Windows XP VM on this Mac — he either owns the machine (with Beth and Amy having accounts) or borrowed it. Network evidence is INSUFFICIENT to determine ownership definitively. Confidence: LOW-MEDIUM (INFERENCE).
- **SEIZURE IDENTIFIERS:** S/N 4H6242CSVMN, HDD NW81T6325527 (primary), K3376NB5022 (secondary), MAC 0016cbbf89d6 (Wi-Fi en1), MAC 00:17:f2:e2:c0:ce (active in capture)
- **LEGAL PROCESS TARGETS:** (1) Absolute Software — TagId 268698586 → registered owner; (2) Facebook — UID 588141158 → real name of beth@bethr.org; (3) Yahoo! — amy789smith → Amy Smith subscriber info; (4) Google — jcoachj@gmail.com, mylady.ixchel@gmail.com → subscriber info; (5) DreamHost — bethr.org registrant
- **OUTPUT FILES:** /scratch/nitroba.pcap/m018_computrace_owner.txt, m018_device_names.txt, m018_beth_identity.txt

## Mission 019 Bonjour/mDNS Ownership Sweep (2026-07-26)

- **mDNS/Bonjour (UDP/5353): 0 packets** — No Bonjour/DNS-SD traffic present anywhere in the 94,410-frame capture. FACT.
- **NBNS (UDP/137): 0 packets** — No NetBIOS name broadcasts from any host. FACT.
- **LLMNR (UDP/5355): 0 packets** — No LLMNR traffic. FACT.
- **CAPTURE ARCHITECTURE NOTE (INFERENCE, HIGH CONFIDENCE):** The NSU sniffer was placed outside the 192.168.15.0/24 Wi-Fi broadcast domain. mDNS is link-local multicast (224.0.0.251) and does not traverse routers. Bonjour name strings broadcast by "Obsidian" (192.168.15.4) within Kenny's Wi-Fi subnet were never recorded by the capture. This is a capture-architecture gap, not evidence that Bonjour was disabled.
- **OWNERSHIP VERDICT (Mission 019):** OWNER NOT IDENTIFIED via Bonjour/mDNS. No new hard indicators to add. Best inference remains Mission 018: owner is likely "Beth" (beth@bethr.org, Facebook UID 588141158). Subpoena paths: Absolute Software TagId 268698586, Facebook UID 588141158, DreamHost (bethr.org registrant).
- **OUTPUT FILE:** `cases/NITROBA/scratch/nitroba.pcap/m019_mdns_names.txt` (zero-results confirmation file)

# Known Forensic Artifacts (IGNORE)
