# AI Forensics

## What
This repository is a structured way to perform forensics using a discrete set of tooling: 

### SIFT
The SIFT workstation from SANS is a battle-tested collection of tried and true forensic utilities. We use it as a docker container to: 

- Run multiple containers in parallel
- Make choices about using tool versions in the container, or locally
- Allow AI an easy CLI interface into the vast set of tools

### Forgecode
Forgecode (or forge) is an AI harness written in rust that allows

- Easy agent creation (a simple .md file)
- Agents to be pointed at any provider/model (a lead investigator using a powerful thinking model, a worker using an efficient flash model)
- Agents to operate as a team
- Agents to operate at scale, instantiating many at a time

### Dissect/Triage-query
The dissect set of utilities https://docs.dissect.tools/en/latest/index.html are a python-based forensics suite that reads any file as a source of forensic data and allows consistent parsing of artifacts. Rather than an individual tool per file type, it offers AI a consistent way to retrieve and parse artifacts adhoc. 

### DuckDB
AI is notoriously bad at navigating large context like we experience in forensics, but notoriously good at data science especially with SQL. 

We purposefully build a pipeline for artifacts to go from raw form to .parquet files with a structured schema, presented as a query utility for AI. This allows extremely rapid and repeatable discovery, analysis by AI in an environment it knows well. DuckDB is local only, no servers needed and is capable of dynamically stitching together .parquet (and other) files which gives us an adhoc environment we can add data as needed.

## Getting started. 

- Install uv for the python environment
- Install the libraries (uv pip install -r requirements.txt)
- `source .venv/bin/activate` to activate the python environment
- Install forge, login with your AI provider and choose your models.
- Create a directory to hold your case images: `mkdir -p ./cases/<CASE_ID>/images`
- Copy in your disk/memory images (by convention `<hostname-disc|memory>.<filetype>` ) 
    - Where filetype is .E01 for expert witness files, .img for memory images. 
    - Files without the word `memory` in the name will be considered disk images and mounted. 
    - Files with the word `memory` in the name will be processed as memory images. 
- Initialize the case `uv run init_case.py --case <CASE_ID> ./cases/<CASE_ID>/images/*
- Initialize processing the case files: 
    - Process all images: `uv run triage_extractor.py --case <CASE_ID> --all`
    - Process selected images (or new images as they arrive): `uv run triage_extractor.py --case <CASE_ID> --evidence ./cases/<CASE_ID>/images/*memory*`

This will kick off a series of artifact gathering for: 
- file system timelines (mactime)
- log2timeline/plaso extraction of key targets: 
    - WindowsRunKeys,
    - WindowsServices,
    - WindowsUserAssist,
    - WindowsAppCompatCache,
    - WindowsEventLogSecurity,
    - WindowsEventLogSystem,
    - WindowsXMLEventLogSecurity,
    - WindowsXMLEventLogSystem,
    - WindowsPrefetchFiles
- volatility
    - pslist
    - netstat
    - timeliner
- MFT records

All of these will be converted to .parquet files with a common schema. Your investigation canvas is now ready for AI. 

## Engage AI

```shell 
forge
```

Will start a forge session. Choose the `forensic-investigator` agent `/agent-forensic-investigator` and begin your investigation. 

