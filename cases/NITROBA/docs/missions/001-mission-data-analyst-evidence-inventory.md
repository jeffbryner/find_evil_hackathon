# Mission: Evidence Inventory & Extraction Status for Case NITROBA
**Target Agent:** data-analyst

## Purpose
Establish the authoritative Data Inventory for case NITROBA: what evidence exists, its integrity hashes, and what (if anything) has already been extracted to scratch/parquet.

## Background
New case. Known evidence so far: a single packet capture at `cases/NITROBA/images/nitroba.pcap`. No extractions are believed to exist yet in `cases/NITROBA/scratch/`. The case scenario PDF is being handled by a separate mission — DO NOT touch the PDF.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 10 tool calls
- **Reporting Budget:** 5 tool calls
- **Proactive Self-Termination:** At tool call 16 (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** If the pcap file cannot be found or read after 2 attempts, stop and report. Do NOT begin content analysis of the pcap (no protocol/conversation analysis) — inventory only.

## Task Checklist
- [x] Read `cases/NITROBA/docs/shared_facts.md` (execute `shared-facts-sop` skill)
- [x] List contents of `cases/NITROBA/images/` and `cases/NITROBA/scratch/` (record all files, sizes)
- [x] Compute MD5 and SHA1 of `cases/NITROBA/images/nitroba.pcap`
- [x] Determine basic pcap metadata ONLY — `capinfos` and `tshark` both unavailable locally (2 attempts); recorded file size and mtime per fail-fast condition.
- [x] Record all results under `# Data Inventory` in `cases/NITROBA/docs/shared_facts.md` (append via patch)
- [x] Update this mission card with results
- [x] Write a chronological technical log of 100% of executed queries and commands to the `-audit.md` file

## Results & Post-Mortem
*(Completed 2026-07-26 by data-analyst)*

- **Approach:** Read mission card and skills, ingested existing shared_facts.md, listed directory contents, computed cryptographic hashes, attempted pcap metadata retrieval via capinfos and tshark (both unavailable locally), then recorded all findings to shared_facts.md and mission card.

- **Findings:**
  | Artifact | Detail |
  |---|---|
  | **File** | `cases/NITROBA/images/nitroba.pcap` |
  | **Size** | 56,180,821 bytes (≈54 MB) |
  | **File Modified (mtime)** | 2026-06-03 13:39:12 UTC |
  | **MD5** | `9981827f11968773ff815e39f5458ec8` |
  | **SHA1** | `65656392412add15f93f8585197a8998aaeb50a1` |
  | **Packet Count** | Unknown — capinfos/tshark unavailable locally |
  | **Capture Start/End** | Unknown — capinfos/tshark unavailable locally |
  | **Scratch directory** | Contains only `container_id.txt`; no parquet extractions exist yet |
  | **PDF** | `cases/NITROBA/docs/NITROBA-Scenario.pdf` (4,401,268 bytes) — out of scope for this mission |

- **Confidence Rating:** HIGH for file size, mtime, MD5, SHA1 (directly computed). LOW for packet count / capture timespan (tools unavailable; SIFT container recommended for Mission 002+ if deep pcap metadata required).

- **Budget Tally:** 11 active tool calls (3 orientation/skill loads + 2 dir listings + 2 hash/metadata + 2 capinfos/tshark attempts + 2 patch/reporting) — well within 20-call budget. Final audit + mission card writes excluded per SOP.

- **NPS / Feedback:** Mission scope was well-defined and achievable. Recommend adding a capinfos/tshark availability check as a pre-flight step in future pcap inventory missions. Suggest spawning a follow-up mission using the SIFT container to obtain packet count, capture start/end time, and link-layer type.

## Discovered Leads (For Followup)
- **Lead 1:** SIFT container (`container_id.txt` present in scratch/) may have `capinfos`/`tshark` available — recommend Mission 002 use the container to extract pcap timing metadata (packet count, capture start UTC, capture end UTC, link-layer type) before deep protocol analysis begins.
