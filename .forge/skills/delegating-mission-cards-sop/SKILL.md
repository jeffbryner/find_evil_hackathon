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

## Instructions for the Delegating Agent:
### Mission Cards
Create a new markdown file for each mission in `scratch/{case_name}/missions/` using a sequential counter and a short semantic description. 
Name the file: `{001..999}-mission-{target_agent}-{short-task-description}.md`
(Example: `001-mission-data-analyst-deletion-timeline.md`, `002-mission-sniper-forensics-carve-zip.md`)

The card **MUST** include the following information:
- The Target Agent
- Mission: What is the agent being asked to do
- Purpose: Why are the agent being asked to do it
- Background: Current Case Context leading to this mission
- Budget: A strict limit on the number of **tool calls** allotted for the task (Do not use time or abstract query limits). 
  - Mission cards **MUST** define an 'Orientation Budget' (e.g., 3 calls to find and verify the image) **AND** an 'Execution Budget' (e.g., 10 calls to extract data). 
  - If orientation fails, the mission is aborted before execution begins.
  - No less than 3 calls should be allocated for orientation and no less than 10 calls for execution.
- Fail-Fast Condition: Explicit instructions on when the agent should give up (e.g., "If your first 5 working searches yield no results, stop and report negative findings. Do not guess table names or follow fruitless paths.").
- Task checklists: Format the mission cards with a literal markdown checklist that target agents must follow
- NPS: Net Promoter Score to measure the agent's satisfaction with the task, the overall process and note any improvements needed.

### Delegation Conversation
When tasking sub agents with a delegated task:
1. Use Explicit I/O Instructions in the Task Prompt: Instead of just handing them a file path, put the exact output requirements directly into the tool invocation.
  ⁎ Example: "Your mission is at scratch/.../mission.md. You MUST use the patch tool to append your final report when you are done to conserve tokens. Do not just return it in the chat."
2. Phase Separation (Micro-Missions): Do not combine heavy schema orientation with deep-dive data extraction. If orientation is needed, make it a separate prerequisite mission card.
3. Strict Tool Call Budgets & Fail-Fast: To stop them from endlessly querying, enforce "Effort-Boxing" directly in the task description using tool call limits and explicit fail-fast conditions.

## Instructions for the Target Agent:
### Orientation
- Retrieve and read the mission card.
- Pay special attention to the goals and the budget given to you to stay within the specified limits.
- Before executing any forensic tools, you **MUST** explicitly state the budget and fail-fast conditions you are operating under in your first response. 
- If you cannot achieve the goals within the budget, report back with a status update and records your attempts in the mission card. It is ok to not complete the entire mission, but you must report your progress, any issues encountered and a note about exhausting the budget.

### Completing the Mission
**IMPORTANT:** When instructed to update a document, report, or mission card, you MUST use the `patch`or `write` tools to modify the file on the filesystem. Providing the updated text only in your conversational response does not fulfill the requirement and is considered a failure. Your mission is only complete when the mission card is updated and saved.

Complete the mission according to the instructions in the card and add a results section detailing: 
- Your approach
- Your results
- Your findings
- Your confidence rating for each finding
- NPS: A brief post mortem of the task, including any feedback or suggestions for improvement.
- Your budget tally

