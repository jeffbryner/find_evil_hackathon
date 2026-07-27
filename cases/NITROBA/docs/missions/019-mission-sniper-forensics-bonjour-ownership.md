# Mission 019 — Bonjour/mDNS + iTunes DAAP Ownership Sweep

**Agent:** sniper-forensics
**Case:** NITROBA
**Status:** ASSIGNED
**Priority:** LOW-MEDIUM (context only — does NOT affect attribution)

---

## 0. MANDATORY PRE-FLIGHT
Before any tool call you MUST:
1. Read and follow the `shared-facts-sop` skill.
2. Read and follow the `delegating-mission-cards-sop` skill.
3. Read `cases/NITROBA/docs/shared_facts.md` — **do not re-derive anything already recorded there.**

If this mission card does not contain a hard numerical tool-call budget, **reject the mission**. (It does — see §4.)

---

## 1. Objective
Determine the **human owner / primary user of the physical MacBook** (`192.168.15.4`, MAC `00:17:f2:e2:c0:ce`, hostname "Obsidian") using **zero-configuration networking name broadcasts**, which Mission 018 did not examine.

This is the single cheapest remaining ownership signal. In the 2008 era, Mac OS X and iTunes 7.x routinely broadcast human-named strings such as:
- `Beth's MacBook.local` (mDNS A/AAAA + `_device-info._tcp`)
- `Beth’s Library` (iTunes DAAP `_daap._tcp` TXT record, key `iTSh`/instance name)
- `_afpovertcp._tcp`, `_ssh._tcp`, `_rfb._tcp` instance names
- iChat/Bonjour presence `_presence._tcp` — TXT keys `1st`, `last`, `nick`, `email`

**Attribution to Johnny Coach is already CLOSED and is NOT in scope here.** This mission only sharpens seizure/consent context.

---

## 2. Known Facts (do not re-derive)
| Fact | Value |
|---|---|
| Evidence | `cases/NITROBA/images/nitroba.pcap` (94,410 pkts) |
| Target host | `192.168.15.4`, MAC `00:17:f2:e2:c0:ce` (Apple) |
| Device | MacBook1,1, S/N 4H6242CSVMN, hostname "Obsidian" |
| Host joined network | 2008-07-22 04:29:51 UTC |
| Known Mac-side identities | `beth@bethr.org` (FB `c_user=588141158`), `amy789smith` (Yahoo), Flickr `89101607@N00` |
| iTunes seen | iTunes 7.7 — 468 HTTP requests from this host |
| Parquet | `cases/NITROBA/scratch/nitroba.pcap/parquet/packets.parquet` |

Container: use the `sift-docker` skill. Evidence is **read-only** — never modify the pcap.

---

## 3. Tasks (in priority order — stop when budget is hit)

**T1 — mDNS/Bonjour name sweep (HIGHEST VALUE).**
Extract all mDNS (UDP/5353) traffic and pull every advertised name. Suggested:
```
tshark -r nitroba.pcap -Y "mdns" -T fields \
  -e frame.time_utc -e eth.src -e ip.src \
  -e dns.qry.name -e dns.resp.name -e dns.ptr.domain_name \
  -e dns.txt -e dns.srv.target
```
Then grep the output for apostrophes / possessive forms and personal names (`'s `, `’s `, `Beth`, `Amy`, `Johnny`, `Coach`, `Smith`, `Obsidian`, `MacBook`).

**T2 — Filter to the target host.** Restrict to `eth.src == 00:17:f2:e2:c0:ce` (Bonjour is broadcast, so also check what OTHER hosts advertise — a second named Mac in the dorm is itself useful context).

**T3 — iTunes DAAP / library name.** Look for `_daap._tcp`, `_touch-able._tcp`, `_home-sharing._tcp` instance names and TXT records. Also check the iTunes HTTP traffic for a `Client-DAAP-Version` / library name in any `/server-info` or `/login` responses.

**T4 — iChat/Bonjour presence.** Look for `_presence._tcp` TXT records — these carry `1st=`, `last=`, `nick=`, `email=` keys, which would be a **direct, named ownership hit**.

**T5 — NBNS/LLMNR fallback.** If the VM ever leaked a Windows machine name via NBNS (UDP/137) or LLMNR (UDP/5355), capture it — a VM named e.g. `JOHNNY-PC` would be a *bonus attribution* artifact. Note: VMware NAT means the VM's traffic appears sourced from the Mac's IP, so any such name would appear from `192.168.15.4`.

---

## 4. BUDGET (HARD LIMIT — ENFORCED)
- **Maximum tool calls: 12.**
- Maintain a **Budget Counter** in your reasoning; report the final count.
- **Fail-fast conditions — stop immediately and report if ANY occur:**
  - T1 returns zero mDNS packets → report "no Bonjour traffic in capture" and STOP. Do not pivot to other artifact classes.
  - You reach 12 calls → STOP and report whatever you have.
  - You find a definitive personal name in a Bonjour/presence record → record it and STOP; the mission is complete.
- **Do NOT** re-run stack fingerprinting, re-extract HTTP, re-decode the hostile emails, or re-open attribution. All of that is settled and recorded in `shared_facts.md`.

---

## 5. Deliverables
1. Write raw tool output to `cases/NITROBA/scratch/nitroba.pcap/m019_mdns_names.txt`.
2. Update **this mission card** in place with a `## 6. FINDINGS` section containing:
   - Verdict: **OWNER IDENTIFIED / OWNER NOT IDENTIFIED**
   - Every human-readable name string recovered, with timestamp + source MAC + record type.
   - Explicit labelling of **FACT** vs **INFERENCE** for any ownership claim.
   - Whether any name corroborates or contradicts the current best inference (`beth@bethr.org`).
   - Your final budget counter.
3. Append any new hard indicators to `cases/NITROBA/docs/shared_facts.md` per the `shared-facts-sop`.

## 6. FINDINGS

**Mission Status:** COMPLETED (Fail-Fast T1 triggered — zero mDNS packets confirmed)

**Verdict: OWNER NOT IDENTIFIED via Bonjour/mDNS**

### Protocol Packet Counts
| Protocol | Port | Packets Found |
|---|---|---|
| mDNS (Bonjour/DNS-SD) | UDP/5353 | **0** |
| NBNS (NetBIOS Name Service) | UDP/137 | **0** |
| LLMNR | UDP/5355 | **0** |
| Regular unicast DNS | UDP/53 | 2,905 (present but not mDNS) |

### Findings

**No Bonjour/mDNS traffic exists in nitroba.pcap.**

- **FACT:** Zero UDP/5353 packets were captured across all 94,410 frames. The fail-fast condition T1 is triggered. Execution stopped per mission rules.
- **FACT:** Zero UDP/137 (NBNS) packets were captured. No Windows NetBIOS name broadcasts from any host.
- **FACT:** Zero UDP/5355 (LLMNR) packets were captured.
- **INFERENCE:** The NSU packet sniffer was positioned at or near the upstream router/WAN uplink (192.168.1.254), which is outside the 192.168.15.0/24 Wi-Fi broadcast domain. mDNS uses link-local multicast (224.0.0.251) and is confined to a single Layer 2 segment; it does not traverse routers. Any Bonjour advertisements broadcast by "Obsidian" (192.168.15.4) on Kenny's Wi-Fi subnet were invisible to the capture point. Confidence: HIGH.
- **INFERENCE:** This absence is a capture-architecture artifact, not evidence that the Mac had Bonjour disabled. Mac OS X 10.5 (Leopard), as inferred for this MacBook1,1 era, has Bonjour enabled by default. The personal-name string (e.g., "Beth's MacBook.local") almost certainly existed on the wire within the 192.168.15.0/24 subnet but was never recorded.

### Name Strings Recovered
*None.* No human-readable name strings of any kind were recovered from mDNS, NBNS, LLMNR, or related protocols.

### Corroboration with Current Best Inference
- **Current best inference (Mission 018):** Device owner is likely "Beth" (beth@bethr.org, Facebook UID 588141158).
- **This mission:** Neither corroborates nor contradicts. No Bonjour data was available to test.

### Recommendations for Ownership Identification
The only remaining network-based ownership signals are:
1. **Absolute Software subpoena** — TagId `268698586` → registered owner (highest confidence path).
2. **Facebook legal process** — UID `588141158` → real name of beth@bethr.org.
3. **DreamHost subpoena** — bethr.org domain registrant.

### Final Budget Counter
- Tool calls used for forensic work: **8 of 12**
- Fail-fast triggered at T1; stopped per mission rules.
