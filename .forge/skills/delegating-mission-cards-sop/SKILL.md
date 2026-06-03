---
name: delegating-mission-cards-sop
description: Standard operating procedure delegating missions to subagents. Always use this skill when delegating tasks or receiving tasks.
---
# Mission Cards

## Overview
To standardize the way tasks are delegated and executed across multiple agents, follow this standard operating procedure to coordinate tasks through mission cards.

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
  - Execution budgets should be between 10-50 tool calls depending on the complexity of the task. 
  - Orientation and reporting budgets should be between 5-15 tool calls.

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
- **Fail-Fast Condition:** [Explicit instructions on when the agent should give up, e.g., "If the file is not found in 5 searches, stop and report."]

## Task Checklist
- [ ] Task 1
- [ ] Task 2
- [ ] Update this mission card with results

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
- **Findings:**
- **Confidence Rating:**
- **Budget Tally:**
- **NPS / Feedback:**
```

### Delegation Conversation
When tasking sub agents with a delegated task:
1. Use Explicit I/O Instructions in the task Prompt: Instead of just handing them a file path, put the exact output requirements directly into the tool invocation.
  **Example**: "Your mission is at /path/to/.../mission.md. You MUST use the patch tool to append your final report when you are done to conserve tokens. Do not just return it in the chat."
2. Reinforce the strict Tool Call Budgets & Fail-Fast: To stop them from endlessly querying, enforce "Effort-Boxing" directly in the task description using tool call limits and explicit fail-fast conditions.

## Instructions for the Target Agent:
### Orientation
- Retrieve and read the mission card.
- **CRITICAL BUDGET CHECK:** If the mission card does NOT contain explicit numerical budgets for Orientation, Execution, and Reporting, you **MUST IMMEDIATELY REJECT THE MISSION**. Do not attempt to guess a budget. Update the mission card with "Mission Rejected: Missing explicit tool budgets" and return control to the Lead Agent.
- Pay special attention to the goals and the budget given to you to stay within the specified limits.
- Before executing any forensic tools, you **MUST** explicitly state the budget and fail-fast conditions you are operating under in your first response. 
- If you cannot achieve the goals within the budget, report back with a status update and records your attempts in the mission card. It is ok to not complete the entire mission, but you must report your progress, any issues encountered and a note about exhausting the budget.

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
  - A chronological log of every tool call executed, including the exact arguments passed and an extremely brief summary of the raw output received. (Useful, not useful, smoking gun, etc.)
  - **ALL Executed Queries & Commands (Strict Completeness):** You MUST log 100% of the raw SQL queries, shell commands, and specialized forensic tool commands executed during your mission. Do NOT summarize, group, truncate, or omit any query/command. If you ran a query that returned an error or yielded no results, you must still log it in its entirety along with its outcome.
  - **Self-Audit Verification:** Before saving the audit file and submitting your report, cross-reference your internal monologue's tool call history against your chronological log and SQL section. Verify that:
    1. The total count of logged tool calls matches your final Budget Tally.
    2. Every single command or SELECT statement you ran is present in the SQL section in its raw, copy-pasteable format.

### Mandatory Forensic Audit Trail Template
The target agent MUST use the following structure for the `-audit.md` file:

```markdown
# Forensic Audit Trail: [Mission Name]

## 1. Initial Prompt & Parameters
[Initial instructions, targets, and budgets]

## 2. Chronological Tool Execution Log
- **Tool Call #1:** `[Tool Name]` with arguments `[Args]` -> *Outcome: [Brief summary]*
- **Tool Call #2:** ...

## 3. All Executed SQL Queries & Shell Commands (In Full)
Every single command or SQL statement run MUST be documented below in its raw form:

### Query/Command 1: [Short description of intent]
\```sql
[Full SQL Statement or Shell Command]
\```
*Result: [E.g., Returned 15 rows / Error: column not found / No results]*

### Query/Command 2: ...
```

This ensures a complete, automatic LLM audit trail that allows human investigators to validate and reconstruct your findings exactly.

