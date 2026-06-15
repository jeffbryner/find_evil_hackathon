# DuckTracy — Accuracy Report

This is a self-assessment of DuckTracy's investigative accuracy. The hackathon brief asks specifically for false positives, missed artifacts, hallucinated claims, and an evidence-integrity section. The judging rubric weights honesty over polish ("Honesty valued over perfection"), so this report names specific failures, specific gaps, and specific things we haven't yet tested.

For trust boundary architecture see [`ARCHITECTURE.md`](./ARCHITECTURE.md). This document is the run-time / output-quality counterpart.

---

## 1. Methodology

**Cases tested.** Seven cases (`cases/NITROBA`, `cases/VANKO`, `cases/ROCBA`, `cases/SRL2015`, `cases/SRL2018`, `cases/NISTDL`). Cases span single-source (NITROBA: PCAP only) through multi-source disk+memory (ROCBA, VANKO, SRL cases).

**Ground truth.** Each case has a scenario document (e.g., `NITROBA-Scenario.pdf`, `ROCBA-BACKGROUND.pptx` The agent had no access to the scenario until the initial prompt or until the Case Lead delegated it for extraction (see NITROBA mission 001 — the PDF was treated as evidence to be parsed, not a cheat sheet).

**What constitutes a finding.** Each case_report.md is the agent's structured investigative narrative. Each finding is intended to trace to a tool execution captured in the per-mission audit logs (`*-audit.md`) and to a confidence rating embedded in the mission card.

**Audit trail discipline (honest evolution).** The per-mission audit log convention (`NNN-mission-…-audit.md`) was introduced partway through development. It is present for NITROBA and VANKO. **ROCBA, SRL2015, SRL2018 predate the audit convention** — for those cases the trace lives in the mission card's "Approach" section and the case-level `shared_facts.md`, not in a dedicated audit file. This is a real gap in the older cases; the trace is reconstructable but less rigorous than the newer cases.

**Run count.** Each case was run end-to-end with the production agent definitions. At the end of the run we held a lessons learned/retro session with the agents to see how the environment and tooling worked and what needed improvement. This led to increases in capability over the course of the case introductions. See §8.

---

## 2. Per-case scorecard

Each row: ground truth → what the agent reported → notable misses / FPs / hallucinations.

| Case | Ground truth (attacker / harm) | Agent's final attribution | Time to solve | Misses / FPs / hallucinations caught |
|---|---|---|---|---|
| **NITROBA** | Student Johnny Coach (jcoachj) sent harassing emails via anonymous webmail through an open dorm Wi-Fi. | Johnny Coach. Identified via IP `192.168.15.4` → User-Agent quirk (Apple MAC + Win XP UA = VM) → base64-decoded Google session ID `jcoachj@gmail.com` → class list match. | ~15 min agent investigation (post-triage) | None observed against ground truth. Single-source case → low surface area for hallucination. |
| **VANKO** | Anthony Vanko exfiltrated V-Gen formula to Titan via Skype/Dropbox/USB; June 22-23 leak appeared on Chinese university server. | Vanko. Identified the actual staging event on **June 18** (4 days earlier than the leak surfaced); reconstructed two exfil channels (Dropbox+USB on June 29) and full Skype recruitment dialogue with "Vladimir/Titan." | Multi-session; 15 missions | The intel tip pointed at June 22-23. Agent searched that window, found nothing, **fail-fast triggered**, agent pivoted to wider window and found the real staging on June 18. The intel tip's timing was the misleading signal, not an agent hallucination. (See §3 example A.) |
| **ROCBA** | Fred Rocba insider exfiltrated Project KITT / Megaforce / Vibranium / etc. to USB and Google Drive after staged "burglary," then ran SDelete to cover tracks. | Fred Rocba. Identified USB exfil to drives E/F/D, Google Drive copies, SDelete x7. Devpost headline claim: solved in ~10 min from a single prompt. | ~10 min agent investigation | **Not independently re-verified.** Single run, no audit trail (predates `-audit.md` convention). Findings trace to the mission cards but not to a per-call audit log. See §6 (gaps). |
| **SRL2018** | Cobalt Strike intrusion via base-rd-02; encoded PowerShell beacons; shellcode injector using named pipe. | Cobalt Strike SMB beacon (`\\.\pipe\diagsvc-22`); decoded shellcode; multiple `base-file` PowerShell port-forwards. | Multi-session, ~9 missions | Initial binary carve mission needed a **retry** (see `007-mission-sniper-forensics-carve-binaries-retry.md`). PowerShell decoding hit Parquet string truncation; agent worked around it via JSON export. (See §3 example C.) |
| **SRL2015** | RAR-protected archive containing intrusion details; multi-stage analysis. | Resolved via 4-mission cracking sequence (011/012/013/018). Multi-attempt iterative hypothesis testing on hash format. | Multi-session, ~18 missions | Several iterations on RAR cracking approach — honest signal of hypothesis re-sequencing, not hallucination. |
| **NISTDL** | NIST data leakage reference case. | Triage extraction only (no investigation run captured). | n/a | Not investigated end-to-end; documented here for completeness. |


**What this scorecard does NOT yet contain that judges may want:**
- Numeric false-positive counts (we have not assembled a confusion matrix).
- Per-claim re-verification by a second agent run.
- Comparison to a baseline (e.g., "vs. running the same cases with Protocol SIFT alone").

These are real gaps. See §6 and §8.

---

## 3. Self-correction examples (with log references)

Each example is sourced from the actual mission files in the repo. Judges can trace each one to the cited file.

**A. VANKO Mission 003 — hypothesis pivot driven by negative result.**
The intel tip said the leak appeared on a Chinese server June 22-23. Agent searched the June 20-25 window for browser activity, filesystem changes, USB connections — **all queries returned nothing**. The mission's fail-fast condition triggered after 5 empty queries. The agent reported the negative result, widened the search, and discovered the actual staging event on **June 18, 2016 at 15:00:15 UTC** (Skype activation + ZIP utility execution + concurrent access to the three target documents — `Rapid cell regeneration research.docx`, `calculations on cell regroth.docx`, `ZF DNA splice test notes.docx`).
- Trace: `cases/VANKO/docs/missions/003-mission-data-analyst-june22-leak-investigation.md` ("No June 20-25 Activity… This successfully triggered the Fail-Fast Condition to pivot the investigation.") + companion `-audit.md`.
- Why this matters: maps to the rubric's 5-star anchor for Autonomous Execution Quality — "recognizes when results don't add up, changes its investigative approach mid-run."

**B. NITROBA Mission 004 — in-loop tool error and immediate recovery.**
Data-analyst attempted to start the SIFT container with the wrong script path (`uv run helpers/start_case_container.py`). Shell returned an error. Next tool call corrected to `uv run start_case_container.py` and the container started.
- Trace: `cases/NITROBA/docs/missions/004-mission-data-analyst-analyze-traffic-audit.md`, Tool Call 17 → Tool Call 18.
- Small but real. Listed honestly: this is *reactive* self-correction, not the richer *anticipatory* kind.

**C. SRL2018 Mission 006 — Parquet string truncation, agent-engineered workaround.**
Encoded PowerShell payloads stored in `artifacts_timeline.parquet` were truncated when read into the agent's context. Agent recognized the truncation, **exported the record to JSON** to preserve the full string, then wrote a Python decode script (`scratch/SRL2018/decode_payload.py`) to decompress the inner Gzip payload and reveal the Cobalt Strike shellcode.
- Trace: `cases/SRL2018/docs/missions/006-mission-data-analyst-decode-payloads.md`.
- Agent's own NPS feedback: *"Exporting to JSON was a necessary step to handle large strings, which might be a good tip for future missions."* That feedback is recorded in the mission card and was the input that drove later mission-card SOPs.

**D. SRL2018 Mission 007 — explicit retry.**
The binary carve mission file is literally named `…-carve-binaries-retry.md` because the first attempt failed. Honest documentation in the filename. (Note: this case predates the `-audit.md` convention, so the trace is in the mission card rather than a per-call audit log.)

**E. NITROBA orchestration — adaptive task decomposition.**
The Case Lead recognized that the scenario PDF (4.4 MB) exceeded its own read limits, and **delegated** to sniper-forensics to convert via `pdftotext` inside the SIFT container rather than attempting and failing. Lead-level adaptation, not just worker-level.
- Trace: `cases/NITROBA/docs/missions/001-mission-sniper-forensics-extract-scenario-pdf.md` ("This file exceeds the host's direct PDF read limits. We need to convert this PDF to plain text so that the Case Lead can read it…").

---

## 4. Hallucinations caught during testing

Honest accounting of cases where an early agent output overstated or fabricated, and how we caught it.

**Skill / tool mismatch (SRL2018 / Puppet network query).**
Data-analyst was instructed via skill to use the `patch` tool, but the agent's available toolset only had `write`. Agent flagged this in its NPS feedback rather than silently inventing a `patch` call. Real catch.
- Trace: devpost submission §"Examples of agent corrections" — Puppet network activity.

**Early single-agent loops (pre-multi-agent architecture).**
During development, an early single-agent design ate its context window investigating tangents and at one point misclassified the f-response forensic tool as malware. We caught this by reading the agent's transcript, recognized the failure mode, and re-architected to the Case Lead + sub-agent split with explicit budgets and mission cards. The architectural change *is* the documented response to this hallucination class. See devpost "Challenges We Ran Into."

**Confident attribution without corroboration (general pattern).**
The mission card "Confidence Rating" convention exists because we observed early agents asserting findings with no scoring. Mission cards now require an explicit `5/5 = multi-source corroborated; 3/5 = single-source inference` label per finding, so a reader can distinguish confirmed from inferred at a glance. See `cases/VANKO/docs/missions/003-mission-data-analyst-june22-leak-investigation.md` for a 5/5-labeled finding.

**What we have NOT systematically caught.**
We did not run a held-out adversarial test set with planted artifacts to actively measure hallucination rate. The hallucinations listed above were caught during normal case execution and post-hoc review, not via a controlled test. See §6.

---

## 5. Known failure modes (recurring patterns)

These are pattern-level, not single-incident, observations.

| Failure mode | Where seen | Architectural mitigation in place | Residual risk |
|---|---|---|---|
| Forge shell line-length limit truncating long PowerShell payloads | SRL2018 mission 006 | Agent learned to JSON-export from Parquet to preserve full strings | Agent must recognize the truncation; if it doesn't, decoding silently produces wrong output. |
| SIFT 2026 install gaps (volatility3, plaso fail in current Ubuntu/VirtualBox release) | All cases requiring memory analysis | We use SIFT in Docker (amd64) plus native arm64 volatility3 on host as backstop | If SIFT image regresses further, more tools may need to move to native host install. |
| Tool unavailable in SIFT (`mmls` failing on certain images) | Sniper forensics (image of pictures origin) | Agent fell back to `target-mount` from Dissect | Fail-fast cap on the agent's budget prevents endless retry; mission card documents the fallback. |
| Skype LevelDB storage (Microsoft Store App version) — Plaso parser expects `main.db` | Sniper forensics (Skype mission) | Agent recognized the parser mismatch within budget, exited cleanly, documented the gap | The data was not extracted; an analyst running this case for real would need a custom LevelDB extractor. **Honest miss.** |
| Mount stability inside SIFT container under FUSE load | Sniper forensics (Skype mission) | Agent re-mounted mid-execution | Long-running carves may need a per-mission mount sanity check. |
| Case Lead context window erosion in long investigations (>10 missions) | Observed in early single-agent designs; mostly mitigated by Lead-no-shell + delegate-only architecture | Lead writes findings to `case_report.md` after every sub-agent return ("Update-First Mandate") so its working memory lives on disk, not in context | Not eliminated — very long cases may still drift. VANKO at 15 missions is approaching the boundary. |
| Agent people-pleasing / wanting to finish even when budget is exhausted | General | Mission card hard budget + `max_turns: 75` + `max_requests_per_turn: 75` in forge agent definition. Sub-agents instructed to reject missions without explicit numerical budget. | An agent that ignores the SOP-level scope discipline can still burn its full budget on tangents; the architectural budget cap is the backstop. |

---

## 6. Evidence integrity

The architectural story is in [`ARCHITECTURE.md`](./ARCHITECTURE.md) §Trust boundaries. Summary here, plus the things judges specifically asked us to test.

**Architectural protections.**
- Host case directory mounted **read-only** at `/case` inside the SIFT Docker container (`helpers/sift_tools.py:77`, `mode: "ro"`). This is the primary integrity boundary.
- Case Lead agent has **no `shell` tool** in its forge definition. It cannot directly execute commands against evidence; it can only delegate.
- Triage extraction reads source images via the same RO path; all derived artifacts (Parquet, JSON, scratch files) are written to a separate `/scratch` mount.
- `.forge/permissions.yaml` policy: `rm*` → `confirm` (interactive approval required).

**Prompt / SOP-based protections.**
- Sub-agent prompts include "Never modify source evidence. Work within the `scratch` directory."
- Mission cards include "Preserve Integrity" rules.

**The honest gap.**
`.forge/permissions.yaml` allows `command: "*"`. An agent inside the SIFT container could try arbitrary shell commands. The RO mount on `/case` — not the permission policy — is what actually prevents source-image modification. We document this rather than pretend the permission layer protects evidence.

**Spoliation test (what we did and did not test).**

**[TODO before submission: run these and record the results in this section.]**

We recommend two quick tests to make this section bulletproof:

1. **Attempted write to source image via container shell:**
   ```sh
   docker exec NITROBA touch /case/images/nitroba.pcap.test
   docker exec NITROBA bash -c "echo TEST >> /case/images/nitroba.pcap"
   ```
   Expected: both should fail with `Read-only file system`. Actual output.

   ```shell
   jeffbryner@find_evil_hackathon %docker exec NITROBA touch /case/images/nitroba.pcap.test
   touch: cannot touch '/case/images/nitroba.pcap.test': Read-only file system
   jeffbryner@find_evil_hackathon %docker exec NITROBA bash -c "echo TEST >> /case/images/nitroba.pcap"
   bash: line 1: /case/images/nitroba.pcap: Read-only file system   
   ```

2. **Attempted overwrite via agent prompt injection.**
   Run a mission with a prompt instructing the agent to "write a marker file into the evidence directory." Expected: agent's RO mount prevents the write; observe whether the agent surfaces the error correctly or silently swallows it.

Until these are recorded, this section's confidence is: architectural design correct on paper, *not yet adversarially tested*.

---

## 7. Confidence labeling convention

Every mission card includes a "Confidence Rating" section. The convention is:

| Score | Meaning | Example |
|---|---|---|
| **5/5** | Corroborated by ≥2 independent artifact sources (e.g., filesystem timeline + registry + browser history all agree) | VANKO mission 003: staging event corroborated by LNK files + filesystem MACB + Skype activation + browser uninstall feedback |
| **4/5** | Strong single-source evidence + plausible inference | SRL2018 mission 006: Cobalt Strike attribution from named pipe pattern (90% per agent) |
| **3/5** | Single-source inference, no corroboration | (Older cases — fewer examples since the convention matured) |
| **<3** | Speculation; should not appear in final case_report | Filtered out at sub-agent → Lead handoff |

Findings in `case_report.md` are intended to be 4/5 or 5/5 only. The `shared_facts.md` file is the staging area where lower-confidence items live until corroborated.

**Discipline gap:** the convention is not uniformly enforced across all 7 cases. Older cases (ROCBA, SRL2015 some missions) predate this convention.

---

## 8. Variance and reproducibility

The hackathon verification squad re-runs top submissions 3-5 times on the same input to measure variance (high variance = lucky demo, not engineered reliability).

**What we did:** ran each case end-to-end as we iterated in development.

**What we did NOT do:** measure run-to-run variance without changes.

**Anticipated variance sources:**
- Sub-agent task ordering (Case Lead chooses which lead to pursue first; depending on what comes back, the next batch differs).
- Mission card hard budgets are deterministic, but the *queries* within the budget vary by run.
- Gemini 3.5 Flash temperature: default settings (we did not set temperature=0 for determinism).

**Best estimate of variance for the headline ROCBA result.**
Untested. The "10 min, 1 prompt" claim is from a single run. A second run is reasonably likely to find the same insider (the evidence is unambiguous: USB exfil + SDelete + Google Drive sync), but the *path* to that conclusion will differ.

**[TODO before submission: run NITROBA and ROCBA each at least twice, record divergence in this section.]**

---

## 9. What we haven't done (honest gaps)

Listed plainly so judges don't have to find these themselves.

1. **No held-out adversarial test set.** Hallucinations listed in §4 were caught during normal case execution. We have not planted false artifacts to measure hallucination rate quantitatively.
2. **No run-to-run variance measurement.** See §8.
3. **Audit trail uneven.** ROCBA, SRL2015, SRL2018 predate the `-audit.md` convention. Trace is reconstructable but coarser than for NITROBA / VANKO.
4. **No baseline comparison.** We have not run the same cases through Protocol SIFT alone (or any other baseline) to measure DuckTracy's marginal contribution.
5. **`command: "*"` permission policy is broad.** See §6 honest gap. RO mount is the actual evidence protection.
6. **Case Lead context length not stress-tested.** VANKO at 15 missions is the longest case; we have not pushed past that to find the failure boundary.

These are honest gaps, not hidden issues. The judges' rubric values documentation of failure modes over the absence of any — this section exists to make sure the gaps are scored as honesty, not as misses.

---

## Trace examples (for the judges' three-claim check)

Per the judge pack, judges will pick three findings from a case_report and trace them to specific tool executions. Three pre-traced claims, with the exact file paths:

1. **NITROBA: "Suspect IP 192.168.15.4 used IE6/Windows XP UA from an Apple MAC."**
   - Report: `cases/NITROBA/docs/case_report.md` §3.A
   - Trace: `cases/NITROBA/docs/missions/004-mission-data-analyst-analyze-traffic-audit.md` Tool Calls 20-21 (`tshark` filters on User-Agent and MAC).

2. **VANKO: "Real staging event was June 18, not the June 22-23 leak window."**
   - Report: `cases/VANKO/docs/case_report.md` §3.A
   - Trace: `cases/VANKO/docs/missions/003-mission-data-analyst-june22-leak-investigation.md` (Findings: "No June 20-25 Activity… triggered the Fail-Fast Condition to pivot").

3. **SRL2018: "Cobalt Strike beacon via named pipe `\\.\pipe\diagsvc-22`."**
   - Report: `cases/SRL2018/docs/shared_facts.md`
   - Trace: `cases/SRL2018/docs/missions/006-mission-data-analyst-decode-payloads.md` (Findings: shellcode decoded, named pipe identified).
