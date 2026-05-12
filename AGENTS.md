# Purpose
The goal is to conduct forensic analysis using AI as efficiently as possible to uncover what happened in a case as quickly as possible.

# Architecture
**Core Technologies:** SIFT (Docker/amd64), DuckDB (Native arm64), AI Agent (forge) (Orchestration), Parquet files for speed/size efficiency, csv or jsonl where needed.

**Approach**: We will be using a "Hybrid Funnel" approach: forensic tool use or heavy-lifting artifact extraction occurs in an emulated SIFT environment, while high-speed reasoning and timeline analysis occur locally using 'agent-friendly' analysis tools like DuckDB and Parquet.

# Guidelines

## Core Technical Standards
- Use `uv` for any python work to ensure the global python environment is unaffected: ```uv run <script.py>``` not ```python3 script.py```
- To ensure forensic integrity do not modify any evidence images (disk, memory, etc)
- **IMPORTANT:** When updating files ALWAYS prefer the `patch` tool over the `write` tool. Using `patch` significantly reduces context token bloat by only sending the diffs.**

## AI Agent Operating Requirements
- **Agents must operate as a team:** There are Standard Operating Procedures (SOPs) formatted as skills that define procedures for task delegation, information sharing and case reporting. These must be followed at all times.

    Key Team Skills:
    - shared-facts-sop
    - delegating-mission-cards-sop

## Budget Tracking
Agent operating parameters will include budgets identified in the mission cards. If you receive a mission, your job as an agent is to maintain a "Budget Counter" in your internal monologue (thought block).

For every task with a tool call budget, you **MUST** track your current count at the start of every turn. Count every tool invocation, including  read, shell, and skill. If you reach the limit or trigger a fail-fast condition, you must stop immediately and report, even if you believe you are close to a solution. Report budget exhaustion if it occurs.
