---
name: sift-docker
description: Orchestrate forensic analysis using a SIFT workstation Docker container. Use this skill when you need to execute forensic tools (like fls, regfexport, md5sum) against mounted evidence, manage the container lifecycle, or map paths between the local host and the container environment.
---

# SIFT Docker Forensic Orchestration

This skill provides guidance and command templates for using the SIFT (SANS Investigative Forensic Toolkit) Docker container as the primary engine for artifact extraction and forensic tool execution.

## Core Concepts

- **Container ID**: Always stored in `scratch/container_id.txt`.
- **Persistent Environment**: Aim to use a single SIFT container for the entire case.
- **Evidence Mounts**: All local files are accessible in the docker image via `/cases`. Mounted filesystems live under `/mnt/cases/<case_name>/<image_name>`.
- **Local to Container Mapping**: 
    - `.` (CWD) -> `/cases` (Read-Only)
    - `./scratch` -> `/scratch` (Read-Write)

## Persistent Multi-Image Workflow

To maintain a single container with multiple mounted images:
### 1. Check environment
```bash
    .forge/skills/sift-docker/scripts/sift-check.sh
```

### 2. Start Environment
If needed (check for `scratch/container_id.txt`) initialize the shared SIFT environment:
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
docker exec $(cat scratch/container_id.txt) mount | grep /mnt/cases
```

## Common Workflows

### 1. Executing Commands
Use the container ID from the scratch file to run tools:
```bash
docker exec $(cat scratch/container_id.txt) <command>
```

### 2. Registry Analysis
Use `rip.pl` (RegRipper) against specific mounted images:
```bash
docker exec $(cat scratch/container_id.txt) rip.pl -r /mnt/cases/<case>/<evidence>/Windows/System32/config/SOFTWARE -p run
```

### 3. Memory Analysis
Volatility 3 can be run against raw memory images in `/cases/images/`:
```bash
docker exec $(cat scratch/container_id.txt) vol -q -r jsonl -f /cases/images/<imagename> windows.pslist
```

### 4. Post-Extraction Analysis
Once artifacts are extracted to Parquet format (via `triage_extractor.py`), use the `forensic-querying` skill to perform high-speed SQL analysis across the evidence.

## Troubleshooting

- **Mount Denied**: Ensure the container is started with `--privileged`.
- **Path Issues**: Always use absolute paths within `docker exec` commands or relative paths from the container's root.
- **EWF Mount Fails**: Check if another process is using the E01 or if the mount point is not empty.
- **Incorrect file types**: Be sure you aren't attempting to mount a memory image like it is a disk image. 
