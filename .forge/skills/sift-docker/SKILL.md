---
name: sift-docker
description: Orchestrate forensic analysis using a SIFT workstation Docker container. Use this skill when you need to execute forensic tools (like fls, regfexport, md5sum) against mounted evidence, manage the container lifecycle, or map paths between the local host and the container environment.
---

# SIFT Docker Forensic Orchestration

This skill provides guidance and command templates for using the SIFT (SANS Investigative Forensic Toolkit) Docker container as the primary engine for artifact extraction and forensic tool execution.

## Core Concepts

- **Container ID**: Always stored locally in `cases/<CASE_NAME>/scratch/container_id.txt`.
- **Persistent Environment**: Aim to use a single SIFT container for the entire case.
- **Evidence Mounts**: All local files are accessible in the docker image via `/cases`. Mounted filesystems live under `/mnt/cases/<case_name>/<image_name>`.
- **Local to Container Mapping**: 

| Context | Base Path | Purpose |
| :--- | :--- | :--- |
| **Local Host** | `cases/<case_name>/images/` | Source E01/Memory images |
| **SIFT Container (Filesystem)** | `/mnt/cases/<case_name>/<image>/` | Direct file access (ls, cp, exiftool) |
| **SIFT Container (Raw/EWF)** | `/mnt/ewf/<case_name>/<image>/ewf1` | Sleuthkit tools (fls, icat, mmls) |
| **Scratch (Shared)**| `/scratch/` | Bidirectional data exchange |
| **Project Root** | `/case/` | Read-only access to case docs/logs |

- **Common Tool Locations**:
    - **Sleuthkit**: `/usr/bin/` (`fls`, `icat`, `mmls`)
    - **Registry**: `/usr/bin/regfexport`, `/usr/local/bin/rip.pl`
    - **Memory**: `/usr/local/bin/vol` (Volatility 3)

- **Mapping Details**:
    - `./cases/<case_name>/` (Case current working directory) -> `/case` (Read-Only in the container, write in the local host)
    - `./cases/<case_name>/scratch` (Case scratch directory) -> `/scratch` (Read-Write in both environments)
    - `./cases/<case_name>/images` (Case images directory) -> `/case/images` (Read-Only in the container, write in the local host)

## ⚡ Efficiency & Budgeting
To stay within tool call budgets and minimize token waste:
- **Batch Commands**: ALWAYS batch related commands into a single `docker exec` call using `bash -c` or HEREDOC. 
- **Targeted Discovery**: Avoid verbose noise like `ls -R` or recursive `fls` if a path is known. Use `find`, `stat`, or targeted `ls` instead.
- **Internal Piping**: Run filters like `grep` inside the container (`bash -c "cmd | grep"`) to avoid sending massive raw output to the host/AI context.
- **Orientation First**: Use 1-2 calls to verify mount points and file existence before launching heavy extraction tools.


## Persistent Multi-Image Workflow

To maintain a single container with multiple mounted images:
### 1. Check environment
```bash
    .forge/skills/sift-docker/scripts/sift-check.sh
```

### 2. Start Environment
If needed (check for `cases/<CASE_NAME>/scratch/container_id.txt`) initialize the shared SIFT environment:
```bash
uv python init_environment.py
```

### 3. Initialize Case & Mount Evidence
Associate images with a case and mount them automatically:
```bash
uv python init_case.py --case <case_name> <images...>
```

### 4. Verify All Mounts
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) mount | grep /mnt/cases
```

## Common Workflows

### 1. Executing Commands
Use the container ID from the scratch file to run tools:
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) <command>
```
Remember that the command is executed in the context of the container. The output of the command would be processed locally (piping to grep for example.) See `references.md` for examples of running multiple commands in a single execution using methods like HEREDOC.

### Registry Analysis
See the `analyze-windows-artifacts` skill for specific commands, but as an example:
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) regfexport -r -i /mnt/cases/<case_name>/<image_name>/Windows/System32/config/SYSTEM -o /scratch/system_hives/
```

### 3. Memory Analysis
Volatility 3 can be run against raw memory images in `/case/images/`:
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) vol -q -r jsonl -f /case/images/<imagename> windows.pslist
```

### 4. Post-Extraction Analysis
Once artifacts are extracted to Parquet format (via `triage_extractor.py`), use the `forensic-querying` skill to perform high-speed SQL analysis across the evidence. 
Do not rely on grep or manual analysis for large datasets. Use the data-analyst agent to query Parquet files with DuckDB for efficient analysis.

## Troubleshooting

- **Path Issues**: Always use absolute paths within `docker exec` commands or relative paths from the container's root.
- **EWF Mount Fails**: Check if another process is using the E01 or if the mount point is not empty.
- **Incorrect file types**: Be sure you aren't attempting to mount a memory image like it is a disk image. 

<resource>/Users/jeffbryner/development/find_evil_hackathon/.forge/skills/sift-docker/references/commands.md</resource>
<resource>/Users/jeffbryner/development/find_evil_hackathon/.forge/skills/sift-docker/scripts/sift-check.sh</resource>
