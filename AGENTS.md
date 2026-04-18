# Purpose
This repository aims to develop an AI assisted forensic capability consisting of local `forge` agents armed with tools that allow them to use utilities housed in the SIFT forensic workstation that SANS produces. 

The SIFT workstation is a reproducable, known quantity for an army of forensic tools and saves us from having to custom install every tool locally. However it is not tuned or oriented for use by AI. 

# Architecture

**Core Technologies:** SIFT (Docker/amd64), DuckDB (Native arm64), AI Agent (forge) (Orchestration), Parquet files for speed/size efficiency, csv or json where needed.

**Approach**: We will be using a "Hybrid Funnel" approach: forensic tool use or heavy-lifting artifact extraction occurs in an emulated SIFT environment, while high-speed reasoning and timeline analysis occur locally using 'agent-friendly' analysis tools like DuckDB and Parquet.

# Development Guidelines

## Core Standards
- Use Python as the preferred development language
- Use `forgecode.dev` aka forge as the agent harness
- Use `uv` for any python work to ensure the global python environment is unaffected
- To ensure forensic integrity do not modify any evidence images (disk, memory, etc)

## AI Agent Requirements

The agent harness we will use for runtime is https://forgecode.dev.
We will create local `.forge` agents, skills, etc for use with the forge harness. 
References: 
- https://forgecode.dev/docs/commands/
- https://forgecode.dev/docs/creating-agents/
- https://forgecode.dev/docs/custom-rules-guide/
- https://forgecode.dev/docs/skills/

The runtime agents we are building for will not be focused on coding, but rather focused on forensic investigation, artifact gathering, analysis, validation and conclusions.

## AI Agent tooling
- Prefer local skills and commands over custom tooling/programs/mcp servers
- When necessary develop custom tooling in python, using command line approaches rather than MCP
- Build for analysis performed by AI using tooling complimentary to AI environments (limited context, reducing tokens, eliminating halucinations, etc)