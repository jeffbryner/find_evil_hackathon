---
name: sift-docker
description: Orchestrate forensic analysis using a SIFT workstation Docker container. Use this skill when you need to execute forensic tools (like fls, icat, psteal_to_parquet.py) against mounted evidence, manage the container lifecycle, or map paths between the local host and the container environment.
---

# SIFT Docker Forensic Orchestration

This skill provides guidance and command templates for using the SIFT (SANS Investigative Forensic Toolkit) Docker container as the primary engine for artifact extraction and forensic tool execution.

## Core Concepts

- **Container ID**: Always stored locally in `cases/<CASE_NAME>/scratch/container_id.txt`. The Container name will match the case name for easy reference.
- **Persistent Environment**: Use a single SIFT container for the entire case.
- **Evidence Mounts**: All local files are accessible in the docker image via `/case` (which is Read-Only). Mounted filesystems live under `/mnt/cases/<case_name>/<image_name>/` (where `<image_name>` matches the filename of the evidence image, e.g. `surface_physical.E01`). Scratch space is shared at `/scratch/` (which is Read-Write).
- **Local to Container Mapping**: 

| Context | Base Path | Purpose |
| :--- | :--- | :--- |
| **Local Host** | `cases/<case_name>/images/` | Source Disk/Memory images |
| **SIFT Container (Filesystem)** | `/mnt/cases/<case_name>/<image_name>/` | Direct file access to the mounted partition (e.g. `/mnt/cases/VANKO/surface_physical.E01/`) |
| **SIFT Container (Raw/EWF)** | `/mnt/ewf/<case_name>/<image_name>/ewf1` | Sleuthkit raw tools (fls, icat, mmls) |
| **Scratch (Shared)**| `/scratch/` | **Read-Write** bidirectional data exchange and tool output staging |
| **Project Root** | `/case/` | **Read-Only** access to case docs/logs |

- **Common Tool Locations**:
    - **Sleuthkit**: `/usr/bin/` (`fls`, `icat`, `mmls`)
    - **Registry**: `/opt/ai-tools/bin/target-reg`, 
    - **Memory**: `/opt/ai-tools/bin/vol` (Volatility 3)

- **Local Mapping Details**:
    - `./cases/<case_name>/` (Case current working directory) -> `/case` (**Read-Only** in the container, write in the local host)
    - `./cases/<case_name>/scratch` (Case scratch directory) -> `/scratch` (**Read-Write** in both environments)
    - `./cases/<case_name>/images` (Case images directory) -> `/case/images` (**Read-Only** in the container, write in the local host)

### 🚨 CRITICAL PATH MAPPING CAUTION (DO NOT MIX THESE UP!)
Forensic investigators and subagents often confuse container paths, leading to execution failures. Ensure you strictly distinguish between these two environments inside the SIFT container:
1. **The Mounted Evidence Filesystem**: `/mnt/cases/<case_name>/<image_name>/`
   * *Example*: `/mnt/cases/NISTDL/surface_physical.E01/`
   * *Purpose*: This is the read-only, mounted filesystem of the target machine itself. You can navigate it directly using standard tools (e.g. `ls`, `cp`, `cat`) without Sleuthkit.
   * *Common Mistake*: Do **NOT** append `/scratch` to this path (e.g., `/mnt/cases/NISTDL/scratch/...` is **INVALID** and does not exist).
2. **The Host Scratch Directory**: `/scratch/`
   * *Example*: `/scratch/surface_physical.E01/parquet/`
   * *Purpose*: This is the **Read-Write** shared space between your local machine and the SIFT container. Staged outputs, extracted databases, and parsed logs **MUST** be written here so they persist on the host. Do **NOT** use `/case/scratch/` inside the container because `/case` is mounted Read-Only, and writes to `/case/scratch/` will fail.

## ⚡ Efficiency & Budgeting
To stay within tool call budgets and minimize token waste:
- **Batch Commands**: ALWAYS batch related commands into a single `docker exec` call using `bash -c` or HEREDOC. 
- **Targeted Discovery**: Avoid verbose noise like `ls -R` or recursive `fls` if a path is known. Use `find`, `stat`, or targeted `ls` instead.
- **Internal Piping**: Run filters like `grep` inside the container (`bash -c "cmd | grep"`) to avoid sending massive raw output to the host/AI context.
- **Orientation First**: Use 1-2 calls to verify mount points and file existence before launching heavy extraction tools. Know that the container is persistent and stateful across turns, so you can build on previous discoveries without re-querying. The disk images will remain mounted so you can access files directly without having to search via fls every time..


## Persistent Multi-Image Workflow

To maintain a single container with multiple mounted images:
### 1. Check environment for SIFT container named after our case:
```bash
    docker ps 
```

### 2. Start Environment
If needed (check for `cases/<CASE_NAME>/scratch/container_id.txt`) initialize the shared SIFT environment:
```bash
uv run start_case_container.py --case <case_name>
```

### 3. Initialize Case & Mount Evidence
Associate images with a case and mount them automatically:
```bash
uv run init_case.py --case <case_name> <images...>
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
You can also use the name of the container (which will be the case name) if you prefer:
```bash
docker exec <container_name> <command>
```

Remember that the command is executed in the context of the container. The output of the command would be processed locally (piping to grep for example.) See `references.md` for examples of running multiple commands in a single execution using methods like HEREDOC.

