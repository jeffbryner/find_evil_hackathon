---
name: shared-facts-sop
description: Standard operating procedure for maintaining and utilizing the centralized case knowledge base to prevent duplicate work and share context across agents.
---
# Shared Facts

## Overview
Reduce the risk of context loss, remove the cold start cost for subagents and ensure key facts are tracked as multiple agents work simultaneously.  

## When to use
All agents MUST use this skill to centralize case knowleged and shared memory as the understanding of the case develops. 
- When starting a task
- When completing a task

## Instructions for the Agent:
1. Locate or Create: Upon starting your task, look for scratch/{case_name}/shared_facts.md. If it does not exist, create it with the following standardized headers:
      * # Data Inventory
      * # Compromised Accounts
      * # Known Malicious IPs & Domains
      * # Suspicious Files & Staging Directories
      * # Decoded Payloads & Scripts
      * # Confirmed Exfiltrated/Accessed Data
      * # Known Forensic Artifacts (IGNORE)
2. Ingest Context: Before running any forensic tools or SQL queries, read shared_facts.md. Use the IPs, file paths, and accounts listed there to filter your initial searches and avoid re-analyzing known artifacts. Also, review the `known_good_tools.md` reference to ensure you do not flag legitimate investigator tools (like F-Response) as malicious.
3. Execute Task: Perform your assigned forensic analysis or SQL queries.
4. Update the Shared Brain: When your analysis yields new hard facts (e.g., a newly discovered staging folder, a decoded base64 string, a new lateral movement IP), you MUST append this data under the appropriate header in shared_facts.md using the `patch` tool. ALWAYS prefer `patch` over `write` for existing files to conserve context tokens.
5. Share IOCs in a queryable format using the track_ioc reference.
5. Return Summary: Finally, return your conversational summary to the Case Lead.

## Rules
  - Never overwrite existing facts; only append.
  - Keep entries concise and agent/parsing friendly (e.g., - TIMESTAMP:2018-09-06 12:00:00+00:00 IP: 108.79.235.64 DESCRIPTION: Associated with evil.exe. )
  - Add new sections if existing sections do not cover your findings

