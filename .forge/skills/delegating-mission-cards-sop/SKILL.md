---
name: delegating-mission-cards-sop
description: Standard operating procedure delegating missions to subagents. Always use this skill when delegating tasks or receiving tasks.
---
# Mission Cards

## Overview
To standardize the way tasks are delegated and executed across multiple agents, follow this standard operating procedure to coordinate tasks through mission cards.

## When to use
All agents MUST use this skill to properly delegate and execute tasks while setting appropriate context and returning meaningful results.
- When delegating a task
- When starting a task
- When completing a task

## Rules
  - Never remove mission cards, they are a record of all delegated tasks.
  - Never remove sections, append new content instead.
  - Keep entries concise and agent/parsing friendly (markdown todo lists for example)

## Instructions for the Delegating Agent:
Create a new markdown file for each mission in `scratch/{case_name}/missions/` using a sequential counter and a short semantic description. 
Name the file: `{001..999}-mission-{target_agent}-{short-task-description}.md`
(Example: `001-mission-data-analyst-deletion-timeline.md`, `002-mission-sniper-forensics-carve-zip.md`)

The card MUST include the following information:
- The Target Agent
- Mission: What is the agent being asked to do
- Purpose: Why are the agent being asked to do it
- Background: Current Case Context leading to this mission
- Budget: A strict limit on the number of **tool calls** (e.g., "Maximum 30 tool calls"). Do not use time or abstract query limits. 
- Fail-Fast Condition: Explicit instructions on when the agent should give up (e.g., "If your first 5 working searches yield no results, stop and report negative findings. Do not guess table names or follow fruitless paths.").
- Task checklists: Format the mission cards with a literal markdown checklist that target agents must follow
- NPS: Net Promoter Score to measure the agent's satisfaction with the task, the overall process and note any improvements needed.


When tasking agents:
1. Use Explicit I/O Instructions in the Task Prompt: Instead of just handing them a file path, put the exact output requirements directly into the task tool invocation.
  ⁎ Example: "Your mission is at scratch/.../mission.md. You MUST use the patch tool to append your final report when you are done to conserve tokens. Do not just return it in the chat."
2. Phase Separation (Micro-Missions): Do not combine heavy schema orientation with deep-dive data extraction. If orientation is needed, make it a separate prerequisite mission card.
3. Strict Tool Call Budgets & Fail-Fast: To stop them from endlessly querying, enforce "Effort-Boxing" directly in the task description using tool call limits and explicit fail-fast conditions.

## Instructions for the Target Agent:
Retrieve and read the mission card. Pay special attention to the goals and the budget given to you to stay within the specified limits. If you cannot achieve the goals within the budget, report back with a status update and records your attempts in the mission card. It is ok to not complete the entire mission, but you must report your progress and any issues encountered.

**IMPORTANT: When updating the mission card or shared facts, ALWAYS prefer the `patch` tool over the `write` tool. Using `patch` significantly reduces context token bloat by only sending the diffs.**

Complete the mission according to the instructions in the card and add a results section detailing: 
- Your approach
- Your results
- Your findings
- Your confidence rating for each finding
- NPS: A brief post mortem of the task, including any feedback or suggestions for improvement.

