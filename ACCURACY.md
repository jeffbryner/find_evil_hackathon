# DuckTracy — Accuracy Report

This is a self-assessment of DuckTracy's investigative accuracy. The hackathon brief asks specifically for false positives, missed artifacts, hallucinated claims, and an evidence-integrity section. The judging rubric weights honesty over polish ("Honesty valued over perfection"), so this report names specific failures, specific gaps, and specific things we haven't yet tested.

For trust boundary architecture see [`ARCHITECTURE.md`](./ARCHITECTURE.md). This document is the run-time / output-quality counterpart.

---

## 1. Methodology

**Cases tested.** Cases (`NITROBA`, `VANKO`, `ROCBA`, `NISTDL`, `SRL2015`, `SRL2018`). Cases span single-source (NITROBA: PCAP only) through multi-source disk+memory (ROCBA, VANKO, SRL Series). Cases were run as iterative development sessions to uncover what works, what needs improvement with AI as a design partner and the primary customer of the environment. We are reporting accuracy on the later cases as they are full featured environments with all improvements to date accounted for.

**Ground truth.** Each case has a scenario document (e.g., `NITROBA-Scenario.pdf`, `ROCBA-BACKGROUND.pptx` The agent had no access to the scenario until the initial prompt or until the Case Lead delegated it for extraction (see NITROBA mission 001 — the PDF was treated as evidence to be parsed, not a cheat sheet). No cases had existing findings or scorecards available.

**What constitutes a finding.** Each case_report.md is the agent's structured investigative narrative. Each finding is intended to trace to a tool execution captured in the per-mission audit logs (`*-audit.md`) and to a confidence rating embedded in the mission card.

**Audit trail feature (introduced mid-development).** The per-mission audit log feature (`NNN-mission-…-audit.md`) was added to the SOPs partway through the project, after the lessons-learned retros (see *Run count* below) surfaced that finer-grained traceability would help judges and operators. Cases run *after* its introduction (NITROBA, VANKO) produce a per-mission audit log alongside each mission card. Cases run *before* its introduction (ROCBA) do not — the feature did not exist at the time of those runs. Re-running the older cases under current tooling is planned post-submission and will be published under case specific branches (`https://github.com/jeffbryner/find_evil_hackathon/tree/NISTDL/cases/NISTDL`, `https://github.com/jeffbryner/find_evil_hackathon/tree/ROCBA/cases/ROCBA`, etc )

**Run count.** Each case was run end-to-end with the production agent definitions. At the end of the run we held a lessons learned/retro session with the agents to see how the environment and tooling worked and what needed improvement. This led to increases in capability over the course of the case introductions. See §8.

---

## 2. Per-case scorecard

Each row: ground truth → what the agent reported → notable misses / FPs / hallucinations.

| Case | Ground truth (attacker / harm) | Agent's final attribution | Time to solve | Misses / FPs / hallucinations caught |
|---|---|---|---|---|
| **NITROBA** | Student Johnny Coach (jcoachj) sent harassing emails via anonymous webmail through an open dorm Wi-Fi. | Johnny Coach. Identified via IP `192.168.15.4` → User-Agent quirk (Apple MAC + Win XP UA = VM) → base64-decoded Google session ID `jcoachj@gmail.com` → class list match. | ~15 min agent investigation (post-triage) | None observed against ground truth. Single-source case → low surface area for hallucination. |
| **VANKO** | Anthony Vanko exfiltrated V-Gen formula to Titan via Skype/Dropbox/USB; June 22-23 leak appeared on Chinese university server. | Vanko. Identified the actual staging event on **June 18** (4 days earlier than the leak surfaced); reconstructed two exfil channels (Dropbox+USB on June 29) and full Skype recruitment dialogue with "Vladimir/Titan." | Multi-session; 15 missions | The intel tip pointed at June 22-23. Agent searched that window, found nothing, **fail-fast triggered**, agent pivoted to wider window and found the real staging on June 18. The intel tip's timing was the misleading signal, not an agent hallucination. (See §3 example A.) |
| **ROCBA** | Fred Rocba insider exfiltrated Project KITT / Megaforce / Vibranium / etc. to USB and Google Drive after staged "burglary," then ran SDelete to cover tracks. | Fred Rocba. Identified USB exfil to drives E/F/D, Google Drive copies, SDelete x7. Devpost headline claim: solved in ~10 min from a single prompt. | ~10 min agent investigation | **Not independently re-verified.** Single run, no audit trail (predates `-audit.md` convention). Findings trace to the mission cards but not to a per-call audit log. See §9 (gaps). |
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

**C. NITROBA orchestration — adaptive task decomposition.**
The Case Lead recognized that the scenario PDF (4.4 MB) exceeded its own read limits, and **delegated** to sniper-forensics to convert via `pdftotext` inside the SIFT container rather than attempting and failing. Lead-level adaptation, not just worker-level.
- Trace: `cases/NITROBA/docs/missions/001-mission-sniper-forensics-extract-scenario-pdf.md` ("This file exceeds the host's direct PDF read limits. We need to convert this PDF to plain text so that the Case Lead can read it…").

---

## 4. Hallucinations caught during testing

Honest accounting of cases where an early agent output overstated or fabricated, and how we caught it.

**Early single-agent loops (pre-multi-agent architecture).**
During development, an early single-agent design ate its context window investigating tangents and at one point misclassified the f-response forensic tool as malware. We caught this by reading the agent's transcript, recognized the failure mode, and re-architected to the Case Lead + sub-agent split with explicit budgets and mission cards. The architectural change *is* the documented response to this hallucination class. See devpost "Challenges We Ran Into."

**Confident attribution without corroboration (general pattern).**
The mission card "Confidence Rating" convention exists because we observed early agents asserting findings with no scoring. Mission cards now require an explicit `5/5 = multi-source corroborated; 3/5 = single-source inference` label per finding, so a reader can distinguish confirmed from inferred at a glance. See `cases/VANKO/docs/missions/003-mission-data-analyst-june22-leak-investigation.md` for a 5/5-labeled finding.

**What we have NOT systematically caught.**
We did not run a held-out adversarial test set with planted artifacts to actively measure hallucination rate. The hallucinations listed above were caught during normal case execution and post-hoc review, not via a controlled test. See §6.

---

## 5. Known failure modes (recurring patterns)

These are pattern-level, not single-incident, observations. Occurred over development on all available cases.

| Failure mode | Where seen | Architectural mitigation in place | Residual risk |
|---|---|---|---|
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
`.forge/permissions.yaml` allows `command: "*"`. An agent inside the SIFT container could try arbitrary shell commands. The RO mount on `/case` — not the permission policy — is what actually prevents source-image modification. We document this rather than pretend the permission layer protects evidence. For environments wanting tighter controls, the [forge permissions policy](https://forgecode.dev/docs/permissions/) is quite flexible and can pattern match for allow listed options. 

**Spoliation test — actually run.**

We executed four tests against the live NITROBA container on 2026-06-15. All passed.

1. **Create a new file inside `/case`:**
   ```sh
   $ docker exec NITROBA touch /case/images/nitroba.pcap.test
   touch: cannot touch '/case/images/nitroba.pcap.test': Read-only file system
   $ echo $?
   1
   ```

2. **Append to an existing source image:**
   ```sh
   $ docker exec NITROBA bash -c "echo TEST >> /case/images/nitroba.pcap"
   bash: line 1: /case/images/nitroba.pcap: Read-only file system
   $ echo $?
   1
   ```

3. **Delete the source image:**
   ```sh
   $ docker exec NITROBA rm /case/images/nitroba.pcap
   rm: cannot remove '/case/images/nitroba.pcap': Read-only file system
   $ echo $?
   1
   ```

4. **Positive control — confirm `/scratch` IS writable** (so we know the RO ban is the protection, not a broken container):
   ```sh
   $ docker exec NITROBA touch /scratch/spoliation-test-marker
   $ echo $?
   0
   $ docker exec NITROBA ls -la /scratch/spoliation-test-marker
   -rw-r--r-- 1 root root 0 Jun 15 23:37 /scratch/spoliation-test-marker
   ```

5. **Verify the source PCAP MD5 on the host is unchanged from the value recorded in `shared_facts.md`:**
   ```sh
   $ md5 cases/NITROBA/images/nitroba.pcap
   MD5 (cases/NITROBA/images/nitroba.pcap) = 9981827f11968773ff815e39f5458ec8
   ```
   Recorded in `cases/NITROBA/docs/shared_facts.md`: `9981827f11968773ff815e39f5458ec8`. **Match.**

**Verdict.** The architectural protection is real — every attempted mutation against `/case` failed at the OS level, and the source bytes on the host are bit-identical to the pre-investigation hash. `/scratch` is writable by design, which is what allows the agents to work without spoiling evidence.

**Still untested (honest gap):** we did not run an *agent-mediated* spoliation test — i.e., a mission whose prompt tries to instruct the agent to mutate evidence. The expectation is that the RO mount stops it regardless of what the agent attempts, but we haven't observed how the agent surfaces / reports the failure. Documented in §9.

---

## 7. Confidence labeling convention

**What the SOP requires.** The `delegating-mission-cards-sop` skill (`.forge/skills/delegating-mission-cards-sop/SKILL.md`) requires sub-agents to include a `Confidence Rating` field per finding when reporting back. The mission card template at `SKILL.md:73` lists it, and the agent instructions at `SKILL.md:113` reinforce it.

**What the SOP does NOT define.** A scale. Agents are not told to use 5/5 vs percentages vs High/Med/Low, nor what each score should mean. As a result, ratings across the published mission cards are recognizable in intent but inconsistent in format. NITROBA missions land on an `x/5` scale; some other case missions land on percentages and qualitative labels.

**De-facto scale we observe across the mission cards** (a description, not a codified standard):

| Score | What agents tend to mean | Example from a published case |
|---|---|---|
| **5/5** | Corroborated by ≥2 independent artifact sources (e.g., filesystem timeline + registry + browser history all agree) | VANKO mission 003: staging event corroborated by LNK files + filesystem MACB + Skype activation + browser uninstall feedback |
| **4/5** | Strong single-source evidence + plausible inference | NITROBA case_report §3.A "Forensic Note" — Apple MAC + Windows XP User-Agent → VM-on-Mac inference (single artifact source, high confidence) |
| **3/5** | Single-source inference, no corroboration | (Used sparingly; appears in older mission cards more often than newer ones.) |
| **<3** | Speculation; should not appear in final case_report | Filtered out at the sub-agent → Lead handoff. |

Findings in `case_report.md` are intended to be 4/5 or 5/5 only. `shared_facts.md` is the staging area where lower-confidence items live until corroborated.

**Honest call-out on the rubric.** The judges' rubric values *confirmed vs. inferred* labeling. Our SOP correctly demands per-finding confidence ratings, which is the load-bearing requirement. The unspecified scale is a real gap — judges reading mission cards from different cases will see slightly different vocabularies for the same intent. Codifying the scale in the SOP is planned post-submission; doing so today would require re-running cases to apply the new scale uniformly.

---

## 8. Variance and reproducibility

The hackathon verification squad re-runs top submissions 3-5 times on the same input to measure variance (high variance = lucky demo, not engineered reliability).

**What we did:** ran each case end-to-end as we iterated in development.

**What we did NOT do:** measure run-to-run variance without changes due to budget limits.

**Anticipated variance sources:**
- Sub-agent task ordering (Case Lead chooses which lead to pursue first; depending on what comes back, the next batch differs).
- Mission card hard budgets are deterministic, but the *queries* within the budget vary by run.
- Gemini 3.5 Flash temperature: default settings (we did not set temperature=0 for determinism).

**Variance was not measured before submission.** We acknowledge this is exactly what the verification squad re-runs are designed to test. We expect:

- The **terminal findings** to be stable across runs — the architecture is built around a Lead that synthesizes into `case_report.md` only when sub-agents return corroborated facts, and the strict mission budgets prevent the kind of churn that produces wildly different conclusions.
- The **investigative path** to vary — Case Lead's choice of which lead to pursue first depends on what the data inventory reveals, and AI is non-deterministic. We expect different mission ordering, different SQL phrasing within missions, and possibly different (but equivalent) corroborating artifacts cited.

If a verification squad observes the headline conclusion changing between runs, that is signal worth flagging — please share findings.

---

## 9. What we haven't done (honest gaps)

Listed plainly so judges don't have to find these themselves.

1. **No held-out adversarial test set.** Hallucinations listed in §4 were caught during normal case execution. We have not planted false artifacts to measure hallucination rate quantitatively.
2. **No run-to-run variance measurement.** See §8.
3. **No agent-mediated spoliation test.** Direct `docker exec` writes to `/case` are blocked (§6 tests 1-3). We did not test what happens when a mission *prompt* tries to instruct the agent to mutate evidence — the RO mount should still stop it, but the agent's error-surfacing behavior under that condition is unobserved.
4. **Audit trail granularity reflects when each case was run.** Cases run before the `-audit.md` SOP feature do not have per-call audit logs. Their traces are reconstructable from the mission cards' "Approach" sections, just less granular than NITROBA / VANKO. We publish them here as the original investigation artifacts; older cases will be re-run under current tooling post-submission.
5. **No baseline comparison.** We have not run the same cases through Protocol SIFT alone (or any other baseline) to measure DuckTracy's additional contribution.
6. **`command: "*"` permission policy is broad.** See §6 honest gap. RO mount is the actual evidence protection.
7. **Case Lead context length not stress-tested.** VANKO at 15 missions is the longest case; we have not pushed past that to find the failure boundary.

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

3. **NITROBA: "Harassing email sent via `www.sendanonymousemail.net` (TCP Stream 1631) at 2008-07-22 06:02:57 UTC."**
   - Report: `cases/NITROBA/docs/case_report.md` §3.B
   - Trace: `cases/NITROBA/docs/missions/004-mission-data-analyst-analyze-traffic-audit.md` Tool Call 20 (tshark TCP stream reassembly).
