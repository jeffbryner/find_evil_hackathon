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
Create a new markdown file for each mission in `scratch/{case_name}/missions/` named `mission-{target_agent}-{YYYY-MM-DD-HH-MM-SS}.md`

The card MUST include the following information:
- The Target Agent
- Mission: What is the agent being asked to do
- Purpose: Why are the agent being asked to do it
- Background: Current Case Context leading to this mission
- Budget: a realistic estimate of time/turns/tokens your agent should spend on the mission (no less than 10 turns/queries)
- Task checklists: Format the mission cards with a literal markdown checklist that target agents must follow
- NPS: Net Promoter Score to measure the agent's satisfaction with the task, the overall process and note any improvements needed.


When tasking agents:
1. Use Explicit I/O Instructions in the Task Prompt: Instead of just handing them a file path, put the exact output requirements directly into the task tool invocation.
  ⁎ Example: "Your mission is at scratch/.../mission.md. You MUST use the write tool to overwrite this file with your final report when you are done. Do not just return it in the chat."
3. Strict Query Budgets: To stop them from endlessly querying, I need to enforce "Effort-Boxing" directly in the task description (e.g., "You have a budget of 5 DuckDB queries. If you don't find the artifact, fail fast, report negative findings, and stop.").

## Instructions for the Target Agent:
Retrieve and read the mission card. Pay special attention to the goals and the budget given to you to stay within the specified limits.

Complete the mission according to the instructions in the card and add a results section detailing: 
- Your approach
- Your results
- Your findings
- Your confidence rating for each finding
- NPS: A brief post mortem of the task, including any feedback or suggestions for improvement.

