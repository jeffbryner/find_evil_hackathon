# Purpose
The goal is to conduct forensic analysis using AI as efficiently as possible to uncover what happened in a case as quickly as possible.

This repository provides an AI assisted forensic capability consisting of local `forge` agents armed with tools that allow them to use utilities housed in the SIFT forensic workstation that SANS produces. 

The SIFT workstation is a reproducable, known quantity for an army of forensic tools and saves us from having to custom install every tool locally. However it is not tuned or oriented for use by AI. 


# Architecture

**Core Technologies:** SIFT (Docker/amd64), DuckDB (Native arm64), AI Agent (forge) (Orchestration), Parquet files for speed/size efficiency, csv or json where needed.

**Approach**: We will be using a "Hybrid Funnel" approach: forensic tool use or heavy-lifting artifact extraction occurs in an emulated SIFT environment, while high-speed reasoning and timeline analysis occur locally using 'agent-friendly' analysis tools like DuckDB and Parquet.

# Guidelines

## Core Technical Standards
- Use Python as the preferred development language
- Use `forgecode.dev` aka forge as the agent harness
- Use `uv` for any python work to ensure the global python environment is unaffected
- To ensure forensic integrity do not modify any evidence images (disk, memory, etc)

## AI Agent Operating Requirements
- **Agents must operate as a team:** There are Standard Operating Procedures (SOPs) formatted as skills that define procedures for task delegation, information sharing and case reporting. These must be followed at all times.

    Key Skills:
    - shared-facts-sop
    - delegating-mission-cards-sop
    
- **Mandate Parallel Delegation:** If you are the lead investigator, whenever you discover a specific artifact requiring deep-dive extraction (e.g., a suspicious PID in memory, a deleted file MFT record, or a carved registry key), you MUST immediately use the `task` tool to launch a sub-agent to investigate it. Do not stop your high-level timeline analysis to perform deep-dive extractions sequentially.
- **Forbid Inline Scripting for Output Parsing:** NEVER use inline Python (`python3 -c "..."`) and Regex to scrape or parse truncated terminal output. If a query returns long strings (like Base64 PowerShell commands or JSON blobs) that get truncated, you MUST use structured output formats (like JSONL) or DuckDB's native export functions to save the full results to a file in the `scratch/` directory for analysis.
- **Maximize Native SQL:** Leverage DuckDB's native string manipulation, regex extraction (`regexp_extract`), and decoding functions (`from_base64`) directly within your SQL queries to process data efficiently, rather than pulling raw data into Python for processing.
