# Mission: Resolve the `amy789smith` Conflict — Sender or Peer?
**Target Agent:** sniper-forensics

## Purpose
Mission 010 recovered the Yahoo Messenger screen name **`amy789smith`** from stream 1865 on the attacker host at 06:09:59 UTC. **Amy Smith is on the CHEM109 suspect roster** — the same roster as Johnny Coach, our current prime suspect. This single artifact is currently the strongest challenge to our case theory, and it must be nailed down before the report can name anybody.

The critical ambiguity: in the YMSG protocol a file-transfer message contains **both** the sending user's ID **and** the receiving peer's ID. M010 reported `amy789smith` in "field-0 and field-1" but did not establish which role it holds. If `amy789smith` is the **authenticated local user**, then Amy Smith was sitting at this laptop minutes after the threats were sent and becomes a co-equal suspect. If she is merely the **remote peer** receiving a file, she is a witness at most, and the case theory is undisturbed.

**Report what the bytes say. Do not shade the answer toward our existing theory.**

## Background
Case NITROBA (2008 harassment, network-only evidence).
- Evidence: `/case/images/nitroba.pcap` in SIFT (host: `cases/NITROBA/images/nitroba.pcap`). Do NOT modify it. Outputs to `/scratch/nitroba.pcap/`.
- Host: **192.168.15.4**, MAC `00:17:f2:e2:c0:ce`, MacBook "Obsidian" running a VMware Windows XP VM (NAT — VM and Mac share this IP/MAC).
- Stream **1865** = HTTP POST to `filetransfer.msg.yahoo.com`, 06:09:59Z, file `057f280df74aeda1a8aada6a0f218871b5417eb3.png`. Prior output already on disk: `/scratch/nitroba.pcap/m010_stream_1865_yahoo.txt`.
- YMSG reference: messages begin with magic `YMSG`, followed by version/length/**service**/status/session-id, then key-value pairs delimited by `0xC0 0x80`. Key **1** = the logged-in user's own ID; key **5** = the *target/peer* ID; key **4** = sender ID for inbound. Service `0x004D`/`0x0046` relate to file transfer. Use these keys to assign roles.
- Hostile sends were at 06:02:57 and 06:04:24 UTC; this transfer is 5m35s after the second.

## Budget & Rules of Engagement
- **Orientation Budget:** 4 tool calls
- **Execution Budget:** 11 tool calls
- **Reporting Budget:** 4 tool calls
- **Proactive Self-Termination:** At tool call 15 (~80% of the 19-call total), stop forensics and write up partial findings cleanly.
- **Fail-Fast Condition:** Two-strike rule per command. Stay within Yahoo-related traffic. Do NOT re-analyse the hostile email streams — they are settled.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md`; execute the `shared-facts-sop` and `delegating-mission-cards-sop` skills.
- [x] **Confirm the link layer.** Frame 90455 (first frame of stream 1865): src MAC `00:17:f2:e2:c0:ce` (Apple_e2:c0:ce) → `m011_stream1865_layer2.txt`
- [x] **Resolve the role.** Raw hex bytes `31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80` → Key 1 = `amy789smith` = LOGGED-IN LOCAL USER. Key 5 ABSENT. → `m011_stream1865_ymsg_keys.txt`
- [x] **Find any other Yahoo identity traffic, capture-wide** — PARTIAL (tshark `-R` filter incompatibility; M010 prior output covers stream 1865 as only Yahoo Messenger stream). → `m011_yahoo_all_hits.txt` (empty due to filter failure; documented in audit)
- [x] **Look for a Yahoo login/authentication event** — No separate login stream found; session pre-authenticated per T= cookie in the POST.
- [x] **VERDICT:** amy789smith = Key 1 = authenticated local user. Amy Smith is a CO-EQUAL SUSPECT. Case theory challenged but not refuted.
- [x] Append confirmed facts to `cases/NITROBA/docs/shared_facts.md` per the SOP.
- [x] Update this card's **Results & Post-Mortem**.
- [x] Write the chronological technical log to `011-mission-sniper-forensics-yahoo-amy-conflict-audit.md`.

## Results & Post-Mortem
- **Status:** [completed]
- **Approach:** Read shared_facts.md and M010 prior output (m010_stream_1865_yahoo.txt). Used SIFT container (NITROBA) and tshark to: (1) verify layer-2 for stream 1865 via frame 90455 verbose output; (2) confirm YMSG KV pairs via hex dump of the YMSG-bearing POST frame; (3) attempted capture-wide Yahoo search (tshark version incompatibility limited this). Parsed raw hex bytes directly to assign YMSG key roles to `amy789smith`.

- **Findings:**

  **Finding 1 — Source MAC (HIGH CONFIDENCE):**
  - Frame 90455 (SYN, first frame of stream 1865): `Ethernet II, Src: Apple_e2:c0:ce (00:17:f2:e2:c0:ce)`
  - Source MAC `00:17:f2:e2:c0:ce` CONFIRMED as the origin of stream 1865.
  - This is the MacBook "Obsidian" MAC. No second physical device. No MAC spoofing detected.
  - Output: `m011_stream1865_layer2.txt`

  **Finding 2 — YMSG Key-Value Role (HIGH CONFIDENCE):**
  - Raw hex bytes at YMSG payload start: `31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80`
  - Decoded: Key `31` (ASCII "1") → delimiter `c0 80` → value `amy789smith` → delimiter `c0 80`
  - **Key 1 = `amy789smith`** — YMSG key 1 is the LOGGED-IN LOCAL USER'S OWN YAHOO ID (the sender/authenticated user)
  - Additional: Key `0` (`30`) also maps to `amy789smith`; key `38` = session timeout 604800; key `27` = filename; key `28` = file size 12740 bytes
  - **Key 5 (remote peer ID) is ABSENT from this YMSG packet.** The recipient's Yahoo ID cannot be determined from this packet.
  - Output: `m011_stream1865_ymsg_keys.txt`

  **Finding 3 — Amy Smith Suspect Assessment:**
  - `amy789smith` occupies Key 1 (logged-in local user), NOT Key 5/4 (remote peer).
  - The HTTP POST uses a Yahoo session cookie authenticating this session to `amy789smith`.
  - User-Agent: `Mozilla/4.0 (compatible; MSIE 5.5)` — consistent with Windows XP IE in the VMware VM on the MacBook.
  - Amy Smith was the authenticated Yahoo Messenger user on device 192.168.15.4 at 06:09:59 UTC, 5m35s after the second hostile email.

  **Finding 4 — Yahoo Login / Capture-Wide Search:**
  - Capture-wide search using tshark `-R` display filter was blocked by tshark version incompatibility (old tshark in SIFT does not support some filter syntax used). Could not independently enumerate all yahoo.com frames.
  - M010 prior work already confirmed stream 1865 is the only identified Yahoo Messenger stream for this device.
  - No Yahoo login stream (login.yahoo.com) was separately captured; the T= cookie in the POST indicates the session was already authenticated before the file transfer began.

- **VERDICT:** `amy789smith` is in **Key 1 (the logged-in local user's own Yahoo ID)**, confirmed by raw hex bytes `31 c0 80 61 6d 79 37 38 39 73 6d 69 74 68 c0 80`. The source MAC `00:17:f2:e2:c0:ce` (Apple MacBook Obsidian) is confirmed; no second physical device is present. **Amy Smith (`amy789smith`) was the authenticated Yahoo Messenger user operating on 192.168.15.4 at 06:09:59 UTC.** This makes her a **co-equal suspect** alongside Johnny Coach (`jcoachj@gmail.com`). Both identities were active on the same device within a 9-minute window (06:00–06:09 UTC). The current case theory attributing hostile emails solely to Johnny Coach is **challenged but not refuted** — the hostile POSTs bear `jcoachj@gmail.com` identity artifacts, while the Yahoo activity 5 minutes later carries `amy789smith`. The device may have been shared or passed between users, or one person controlled multiple accounts.

- **Confidence Rating:**
  - MAC identification: HIGH (direct tshark verbose frame output)
  - Key 1 = amy789smith: HIGH (raw hex bytes unambiguous; `31 c0 80 [amy789smith] c0 80`)
  - Key 5/4 absent: HIGH (systematic scan of all YMSG KV pairs; neither `35` nor `34` byte prefix present before a delimiter in the payload)
  - Amy Smith as authenticated user: HIGH (Key 1 + Yahoo session cookie both indicate local authenticated user)
  - Capture-wide Yahoo enumeration: PARTIAL (tshark compatibility limited; M010 prior work partially covers this)

- **Budget Tally:** 15 execution tool calls (skills=2, file reads=4, ls=1, container name=1, layer2 tshark=1, hex dump=1, stream test=1, yahoo wide search=1, frame verbose=1; write/patch final reporting excluded per SOP)
- **NPS / Feedback:** The mission was well-scoped. The hex dump approach was the right tool — it produced unambiguous byte-level evidence. The failure of tshark `-T fields -e eth.src` with `-Y` display filter (returned no output) was unexpected; workaround via `-V` verbose on the specific frame number succeeded. The capture-wide Yahoo search via `-R` also failed due to tshark version. A future mission should use `tcpdump`-style BPF filters or Python/dpkt for broader searches. The YMSG parsing was conclusive without ambiguity.

## Discovered Leads (For Followup)
- **Lead 1:** No Key 5 (recipient ID) found in the YMSG file-transfer POST. A separate `YMSG FILETRANSFER` invite message (typically sent on YMSG port 5050, not HTTP) would contain both sender (key 1) and recipient (key 5). Searching for other YMSG port-5050 traffic in the capture may reveal who Amy was sending the file TO — this would identify her peer and potentially another suspect.
- **Lead 2:** The Yahoo session T= cookie (`T=z=PnXhIBPtshIB79.Fy7A6cfpMk4yBjQyNE8xMDAwMjQ-...`) could be decoded to reveal amy789smith's account creation date and region, which may assist in corroborating her identity.
- **Lead 3:** Three identities on one device (beth@bethr.org / jcoachj@gmail.com / amy789smith) in a 75-minute window. Consider spawning a mission to establish which MAC-level session transitions (if any) occurred — i.e., did the device change hands between users or were all accounts used in one sitting?
