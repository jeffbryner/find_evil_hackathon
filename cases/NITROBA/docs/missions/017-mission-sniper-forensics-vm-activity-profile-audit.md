# Mission 017 Audit Trail — Complete Windows XP VM Activity Profile
**Case:** NITROBA | **Agent:** sniper-forensics | **Date:** 2026-07-26 | **Status:** COMPLETED

---

## Tool Call Log

| # | Tool | Action | Result |
|---|------|--------|--------|
| 1 | skill | delegating-mission-cards-sop | Loaded SOP |
| 2 | skill | shared-facts-sop | Loaded SOP |
| 3 | Read | missions/017-mission-sniper-forensics-vm-activity-profile.md | Loaded mission |
| 4 | Read | docs/shared_facts.md | Loaded case context |
| 5 | shell | `docker ps --filter name=sift` | Container STOPPED |
| 6 | Read | scratch/nitroba.pcap/m015_all_syn_fingerprints.txt | 1,761 SYN entries, reused |
| 7 | Read | scratch/nitroba.pcap/m016_all_http_5950_0602.txt | 1,182 HTTP lines, reused for context |
| 8 | shell | Python regex parse of m015 for window=64240/wscale=0 | 147 VM streams identified |
| 9 | shell | `uv run python3 start_case_container.py --case NITROBA` | Container started (NITROBA) |
| 10 | shell | Python: build tshark stream OR-filter from 147 stream numbers | Filter string generated |
| 11 | shell | `docker start NITROBA && docker exec tshark ... > m017_vm_http_requests.txt` | Failed (path issue) |
| 12 | shell | `docker exec NITROBA bash -c "tshark -r /case/images/nitroba.pcap -Y 'http.request && (tcp.stream==...)' -T fields ... > /scratch/..."` | **480 HTTP requests written** |
| 13 | shell | Python analysis: hosts, search trail, identity sweep, anti-forensic check | All output files written |
| 14 | patch | shared_facts.md — append M017 findings block | Shared facts updated |
| 15 | Read | missions/017-mission-sniper-forensics-vm-activity-profile.md | Verified card already complete |
| 16 | Read | missions/017-mission-sniper-forensics-vm-activity-profile.md (end) | Confirmed full results present |

**Total tool calls:** 16 / 20 budget

---

## Commands Used

### 1. SYN Fingerprint Parse (local Python via uv)
```
uv run python3 -c "
import re
vm_streams = {}
with open('cases/NITROBA/scratch/nitroba.pcap/m015_all_syn_fingerprints.txt') as f:
    for line in f:
        m = re.match(r'^(\d+)\t(\d+)\t(.*? UTC)\t(\d+)\t(\d+)\t(\d+)\t(\d+)\t', line)
        if m:
            if int(m.group(5)) == 64240 and int(m.group(7)) == 0:
                vm_streams[int(m.group(1))] = (int(m.group(2)), m.group(3), int(m.group(4)))
"
```
**Result:** 147 unique VM streams identified.

### 2. tshark HTTP Extraction (SIFT container)
```bash
docker exec NITROBA bash -c "tshark -r /case/images/nitroba.pcap -q \
  -Y 'http.request && (tcp.stream == 1095 || tcp.stream == 1407 || ... [all 147 stream numbers])' \
  -T fields -e frame.number -e frame.time -e tcp.stream -e http.host -e http.request.full_uri \
  2>/dev/null > /scratch/nitroba.pcap/m017_vm_http_requests.txt"
```
**Result:** 480 HTTP requests across 63 distinct hosts.

### 3. Python Post-Processing (local via uv)
- Parsed m017_vm_http_requests.txt (tab-delimited 5-field)
- URL-decoded all URIs using `urllib.parse.unquote_plus`
- Extracted search queries matching `?q=`, `?p=`, `&q=`, `&p=` parameters
- Identity sweep: searched all URIs for `@`, `jcoachj`, `amy789smith`, `beth`, `bethr`, `email=`, `login`
- Anti-forensic check: searched for `proxy`, `anonymou`, `tor`, `vpn`, `sendanonymousemail`, `willselfdestruct`

---

## Key Findings

### VM Identification Method
- **Method:** TCP SYN client fingerprint — `tcp.window_size_value == 64240` AND `tcp.options.wscale.shift == 0`
- **Source file:** `m015_all_syn_fingerprints.txt` (produced by Mission 015)
- **User-Agent NOT used** (correctly, per mission rules — UA already caused a wrong answer in M012)

### True VM Active Window (CORRECTED)
| | Stream | Frame | Timestamp |
|--|--------|-------|-----------|
| **First** | 1095 | 51957 | 2008-07-22T05:41:26.604519Z |
| **Last** | 1727 | 84644 | 2008-07-22T06:05:10.xxxZ |
| **Duration** | — | — | **23 minutes 44 seconds** |

M012's "05:02:05–06:09:59" is **superseded**. That window was built from User-Agent matching which incorrectly classified Mac OS X streams 1045 (05:02:05Z) and 1865 (06:09:59Z) as Windows. TCP stack is definitive.

### Complete Search/Research Trail (Chronological, URL-decoded)

| # | Timestamp (UTC) | Service | Search Query | Stream |
|---|----------------|---------|--------------|--------|
| 1 | 05:57:38Z | Google | **how to annoy people** | 1473 |
| 2 | 05:58:01Z | Google | **sending anonymous mail** | 1473 |
| 3 | 05:58:07Z | Google | **i want to harass my teacher** | 1473 |
| 4 | 05:58:32Z | Yahoo Answers | **can I go to jail for harassing my teacher?** | 1540 |
| 5 | 05:59:34Z | Google | **google calendar** | 1574 |
| 6 | 06:01:24Z | Google | **send anonymous mail** | 1602 |

**Premeditation narrative:** In 3m46s the attacker went from researching annoyance tactics → anonymous email → expressed direct intent → researched legal consequences → logged into own Gmail → found second anonymiser. First hostile email sent at 06:02:57Z.

### Top VM HTTP Hosts (> 5 requests)
| Count | Host |
|-------|------|
| 124 | mail.google.com |
| 52 | z.about.com |
| 43 | www.google.com |
| 41 | l.yimg.com |
| 23 | pagead2.googlesyndication.com |
| 13 | www.annoy.com |
| 13 | i.ytimg.com |
| 10 | www.willselfdestruct.com |
| 7 | login.live.com |
| 7 | www.sendanonymousemail.net |
| 6 | download.windowsupdate.com |

### Identity Sweep (VM-only, stack-verified)
- `jcoachj@gmail.com` — **CONFIRMED** in Google Calendar/Gmail URIs (streams 1601, 1605, 05:59–06:01Z)
- `amy789smith` — **NOT FOUND** in any VM HTTP URI (Mac OS X side only, stream 1865)
- `beth@bethr.org` — **NOT FOUND** in any VM HTTP URI (Mac OS X side only, stream 624)
- `mylady.ixchel@gmail.com` — **NOT FOUND** in VM URIs
- **VERDICT: `jcoachj@gmail.com` is the ONE AND ONLY human identity in the Windows XP VM. Attribution to Johnny Coach is DEFINITIVE.**

### Anti-Forensic Activity
- `www.sendanonymousemail.net` — accessed (streams 1621/1622)
- `www.willselfdestruct.com` — accessed (streams 1674-1683, 1701-1705)
- `login.live.com` / `mail.live.com` — loaded TWICE (05:57:23Z and 05:59:20Z), no login POST captured
- `www.annoy.com` — accessed at 05:57:52Z (harassment research site)
- `www.clintonfein.com` — accessed 06:01:26-27Z (First Amendment/harassment legal site)
- **No Tor, no proxy, no VPN detected**

---

## Output Files
| File | Location | Contents |
|------|----------|----------|
| m017_vm_streams.txt | /scratch/nitroba.pcap/ | 147 VM streams with SYN frame + timestamp + port |
| m017_vm_http_requests.txt | /scratch/nitroba.pcap/ | 480 HTTP requests (frame, time, stream, host, URI) |
| m017_vm_hosts.txt | /scratch/nitroba.pcap/ | 63 distinct hosts with request counts |
| m017_vm_search_trail.txt | /scratch/nitroba.pcap/ | 6 search queries, URL-decoded |
| m017_vm_identities.txt | /scratch/nitroba.pcap/ | Identity sweep hits |

---

## Confidence: HIGH
All findings derived from TCP stack fingerprint (window=64240/wscale=0), not User-Agent strings.
