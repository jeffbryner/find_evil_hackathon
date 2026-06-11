---
name: delegating-mission-cards-sop
description: Standard operating procedure delegating missions to subagents. Always use this skill when delegating tasks or receiving tasks.
---
# Mission Cards

## Overview
To standardize the way tasks are delegated and executed across multiple agents, follow this standard operating procedure to coordinate tasks through mission cards.

### ⚠️ CRITICAL DISTINCTION: Evidence vs. Action
To maintain strict forensic standards, agents must separate "What the Suspect Did" from "What the Investigator Did":
*   **The Mission Card & Shared Facts (`.md`):** This is the **Evidence Report**. It documents Vanko's activities, timelines, threat actors, and motives. Do NOT put detailed tool execution history or raw SQL query strings here.
*   **The Audit Trail (`-audit.md`):** This is the **Investigator Log**. It documents your exact technical actions, exact SQL queries, shell commands, tool parameters, and execution outcomes. Do NOT write a high-level summary of the case evidence here.

## When to use
All agents **MUST** use this skill to properly delegate and execute tasks while setting appropriate context and returning meaningful results.
- When delegating a task
- When starting a task
- When completing a task

## Rules
  - Never remove mission cards, they are a record of all delegated tasks.
  - Never remove sections, append new content instead.
  - Keep entries concise and agent/parsing friendly (markdown todo lists for example)
  - Budget in increments of 5 tool calls to stay parsable and easy to understand at a glance. 
  - Execution budgets should be between 10-20 tool calls. Design the mission to meet the budget. SIMPLE tasks are better than multi-stage complex tasks.
  - **Single Responsibility Principle for Missions (SRP-M):** A single mission card should have exactly ONE clear forensic objective. Never combine extraction, parsing, and deep-dive analysis/searching into a single mission.
  - **The Three-Stage Mission Funnel:** When dealing with raw databases or complex artifacts, split the work into separate, sequential missions:
    1. *Stage 1: Extraction Mission (sniper-forensics):* Extract or carve raw files/databases from the disk image to scratch space.
    2. *Stage 2: Ingestion & Parsing Mission (sniper-forensics/data-analyst):* Run parsing tools (e.g., `pffexport`, `parse_emails.py`) to convert raw files into structured queryable tables (e.g., Parquet).
    3. *Stage 3: Analysis & Hunting Mission (data-analyst):* Execute SQL queries and search the tables for keywords, timelines, and motives.
  - Orientation and reporting budgets should be between 5-10 tool calls.
  - **The Living Mission Card Rule (Step-by-Step Checkpointing):** Target agents **MUST** use the `patch` or `write` tool to update the mission card and audit trail file on disk immediately after completing *each individual item* on the task checklist, or every 5 tool calls. Never proceed to a new task without saving progress of the previous one.
  - **The "Two-Strike" Fail-Fast Rule:** If any forensic command, query, or script fails **twice** in a row due to errors (syntax, pathing, database locks), the target agent **MUST** immediately cease active forensics, document the error in the mission card, set its status to `[partially_completed]`, and exit cleanly. Do not attempt to dynamically debug beyond two attempts.
  - **The "Record and Defer" Rule for Scope Creep:** If a target agent discovers a new, highly interesting lead, account, indicator, or artifact that is *outside* the direct scope of its current mission checklist, it **MUST NOT** pursue it immediately. Instead, the agent must document the lead in the "Discovered Leads (For Followup)" section of the mission card and continue executing its assigned checklist. This prevents budget exhaustion from chasing rabbit holes.
  - **No Relaunching Failed Missions:** If a mission is interrupted or self-terminates, it must be recorded as `[partially_completed]` with its partial audit log saved. To continue, the Case Lead MUST create a *new* mission card (e.g., `009-mission-...`) referencing the previous one, ensuring a complete forensic trail of the investigation.

## Instructions for the Delegating Agent:
### Mission Cards
Create a new markdown file for each mission in `cases/{case_name}/docs/missions/` using a sequential counter and a short semantic description. 
Name the file: `{001..999}-mission-{target_agent}-{short-task-description}.md`
(Example: `001-mission-data-analyst-deletion-timeline.md`, `002-mission-sniper-forensics-carve-zip.md`)

You **MUST** use the following exact Markdown template when creating the file:

```markdown
# Mission: [Short Title]
**Target Agent:** [Agent Name]

## Purpose
[Why are we doing this?]

## Background
[Current Case Context leading to this mission]

## Budget & Rules of Engagement
- **Orientation Budget:** [X] tool calls
- **Execution Budget:** [Y] tool calls
- **Reporting Budget:** [Z] tool calls
- **Proactive Self-Termination:** At tool call X (80% of total budget), immediately cease active forensics and use remaining calls to write out partial findings and exit cleanly.
- **Fail-Fast Condition:** [Explicit instructions on when the agent should give up, e.g., "If the file is not found in 5 searches, stop and report."]

## Task Checklist
- [ ] Task 1
- [ ] Task 2
- [ ] Update this mission card with results
- [ ] Write a chronological technical log of 100% of executed queries and commands to the `-audit.md` file (verifying that the count matches the final Budget Tally)

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
- **Findings:**
- **Confidence Rating:**
- **Budget Tally:**
- **NPS / Feedback:**

## Discovered Leads (For Followup)
*(Document any new accounts, IPs, files, or indicators found during this mission that are outside the current scope. Do NOT pursue them during this mission.)*
- **Lead 1:** [Details]
- **Lead 2:** [Details]
```

### Delegation Conversation
When tasking sub agents with a delegated task:
1. Use Explicit I/O Instructions in the task Prompt: Instead of just handing them a file path, put the exact output requirements directly into the tool invocation.
  **Example**: "Your mission is at /path/to/.../mission.md. You MUST use the patch tool to append your final report when you are done to conserve tokens. Do not just return it in the chat."
2. Reinforce the strict Tool Call Budgets & Fail-Fast: To stop them from endlessly querying, enforce "Effort-Boxing" directly in the task description using tool call limits and explicit fail-fast conditions.
3. **Validate Container Paths**: Ensure that any paths provided in the mission card match the actual mapping of the SIFT container. Specifically:
   * Use `/mnt/cases/<case_name>/<image_name>/` for the read-only mounted filesystem (e.g. `/mnt/cases/VANKO/surface_physical.E01/`).
   * Use `/scratch/` for the read-write scratch space (e.g. `/scratch/surface_physical.E01/extracted_comms/`). Do **NOT** use `/case/scratch/` inside the container as `/case` is mounted Read-Only.
   * **NEVER** write invalid hybrid paths like `/mnt/cases/<case_name>/scratch/` as they do not exist and will cause execution failures.

## Instructions for the Target Agent:
### Orientation
- Retrieve and read the mission card.
- **CRITICAL BUDGET CHECK:** If the mission card does NOT contain explicit numerical budgets for Orientation, Execution, and Reporting, you **MUST IMMEDIATELY REJECT THE MISSION**. Do not attempt to guess a budget. Update the mission card with "Mission Rejected: Missing explicit tool budgets" and return control to the Lead Agent.
- Pay special attention to the goals and the budget given to you to stay within the specified limits.
- Before executing any forensic tools, you **MUST** explicitly state the budget and fail-fast conditions you are operating under in your first response. 
- If you cannot achieve the goals within the budget, report back with a status update and records your attempts in the mission card. It is ok to not complete the entire mission, but you must report your progress, any issues encountered and a note about exhausting the budget.

### Living Mission Card & State Checkpointing
- **MANDATORY CHECKPOINTING:** To prevent token or request limit exhaustion from erasing all progress, you MUST use the `patch` tool to update your current progress back to the mission card and the `-audit.md` file on disk immediately after completing *each individual item* on the task checklist, or every 5 tool calls. Never proceed to a new task without saving progress of the previous one.
- **THE TWO-STRIKE FAIL-FAST RULE:** If any forensic command, query, or script fails **twice** in a row due to errors (syntax, pathing, database locks), you **MUST** immediately cease active forensics, document the error in the mission card, set its status to `[partially_completed]`, and exit cleanly. Do not attempt to dynamically debug beyond two attempts.
- **PROACTIVE SELF-TERMINATION:** Track your tool call count. If you reach 40 tool calls (or 80% of your total budget), immediately cease active forensic work. Use your remaining tool calls to perform a final update to the mission card on disk, set its status to `[partially_completed]`, detail what has been done and what remains, write your audit log, and exit cleanly. Do not run until a platform abort occurs as your work will be lost.

### Completing the Mission
**IMPORTANT:** When instructed to update a document, report, or mission card, you MUST use the `patch`or `write` tools to modify the file on the filesystem. Providing the updated text only in your conversational response does not fulfill the requirement and is considered a failure. **Your mission is only complete when the mission card is updated and saved.**

Complete the mission according to the instructions in the card and add a results section detailing: 
- Your approach
- Your results
- Your findings
- Your confidence rating for each finding
- NPS: A brief post mortem of the task, including any feedback or suggestions for improvement.
- Your budget tally

### Mandatory Forensic Audit Trail
To ensure transparency, reproducibility, and a clear chain of custody, you **MUST** automatically write a detailed forensic audit trail of your entire execution history to a separate file.
- **File Name Format:** Exactly the same name as the mission card you are updating, but with `-audit.md` instead of `.md` (e.g., if the card is `001-mission-data-analyst-inventory-and-triage.md`, the audit file MUST be `001-mission-data-analyst-inventory-and-triage-audit.md` in the same directory).
- **Contents Required:**
  - The exact initial prompt/mission parameters received.
  - A chronological log of every tool call executed, including the exact, complete arguments passed (with NO truncation, NO ellipses `...`, and NO placeholder summaries) and an extremely brief summary of the raw output received. (Useful, not useful, smoking gun, etc.)
  - **ALL Executed Commands (Strict Completeness):** You MUST log 100% of the shell commands, and specialized forensic tool commands executed during your mission. Do NOT summarize, group, truncate, or omit any query/command. If you ran a command that returned an error or yielded no results, you must still log it in its entirety along with its outcome. The use of ellipses `...` or placeholder text is strictly forbidden.
  - **Self-Audit Verification:** Before saving the audit file and submitting your report, cross-reference your internal monologue's tool call history against your chronological log section. Verify that:
    1. The total count of logged tool calls matches your final Budget Tally.
    2. Every single command ran is present in its raw, copy-pasteable format including the full, exact text of the command with all arguments intact.

#### Examples:

**CORRECT AUDIT LOGGING (DATABASE QUERY):**
- **Tool Call #14:** Executed SQLite query on `skype_main.db`: 
  `SELECT id, datetime(timestamp, 'unixepoch') FROM Messages WHERE body_xml LIKE '%classified%'`
  -> *Outcome: Identified 12 messages containing target keywords; logged findings to timeline.*

**CORRECT AUDIT LOGGING (SHELL COMMAND):**
- **Tool Call #20:** `shell` with `{"command": "uv run helpers/query_parquet.py --case CASEID --query \"SELECT count(*) FROM artifacts_timeline WHERE timestamp >= '2016-06-20 00:00:00+00' AND timestamp <= '2016-06-25 23:59:59+00'\""}` -> *Outcome: Counted 11,829 artifacts_timeline entries in the target date range.*

**INCORRECT AUDIT LOGGING:**
- **Tool Call #16:** `shell` with query for external drive letters in `artifacts_timeline` excluding EVTX

### Mandatory Forensic Audit Trail Template
The target agent MUST use the following structure for the `-audit.md` file:

```markdown
# Forensic Audit Trail: [Mission Name]

## 1. Initial Prompt & Parameters
[Initial instructions, targets, and budgets]

## 2. Chronological Tool Execution Log
- **Tool Call #1:** `[Tool Name]` with arguments `[Args]` -> *Outcome: [Brief summary]*
- **Tool Call #2:** ...


This ensures a complete, automatic LLM audit trail that allows human investigators to validate and reconstruct your findings exactly.

