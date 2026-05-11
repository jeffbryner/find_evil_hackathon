# Purpose
The goal is to conduct forensic analysis using AI as efficiently as possible to uncover what happened in a case as quickly as possible.


# Architecture

**Core Technologies:** SIFT (Docker/amd64), DuckDB (Native arm64), AI Agent (forge) (Orchestration), Parquet files for speed/size efficiency, csv or json where needed.

**Approach**: We will be using a "Hybrid Funnel" approach: forensic tool use or heavy-lifting artifact extraction occurs in an emulated SIFT environment, while high-speed reasoning and timeline analysis occur locally using 'agent-friendly' analysis tools like DuckDB and Parquet.

# Guidelines

## Core Technical Standards
- Use `uv` for any python work to ensure the global python environment is unaffected
- To ensure forensic integrity do not modify any evidence images (disk, memory, etc)

## AI Agent Operating Requirements
- **Agents must operate as a team:** There are Standard Operating Procedures (SOPs) formatted as skills that define procedures for task delegation, information sharing and case reporting. These must be followed at all times.

    Key Team Skills:
    - shared-facts-sop
    - delegating-mission-cards-sop
    
