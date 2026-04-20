---
name: sift-docker
description: Orchestrate forensic analysis using a SIFT workstation Docker container. Use this skill when you need to execute forensic tools (like fls, regfexport, md5sum) against mounted evidence, manage the container lifecycle, or map paths between the local host and the container environment.
---

# SIFT Docker Forensic Orchestration

This skill provides guidance and command templates for using the SIFT (SANS Investigative Forensic Toolkit) Docker container as the primary engine for artifact extraction and forensic tool execution.

## Core Concepts

- **Container ID**: Always stored in `scratch/container_id.txt`.
- **Persistent Environment**: Aim to use a single SIFT container for the entire case.
- **Evidence Mounts**: All evidence images should be accessible via `/evidence`. Mounted filesystems live under `/mnt/windows/<image_name>`.
- **Local to Container Mapping**: 
    - `./images` -> `/evidence` (Read-Only)
    - `./scratch` -> `/scratch` (Read-Write)

## Persistent Multi-Image Workflow

To maintain a single container with multiple mounted images:

### 1. Start/Attach to Container
Check if a container is already running. If not, start one mounting the entire `images` directory:
```bash
docker run -d --name sift-case --privileged -v $(pwd)/images:/evidence -v $(pwd)/scratch:/scratch sift-volatility:latest tail -f /dev/null
docker ps -q -f name=sift-case > scratch/container_id.txt
```

### 2. Mount New Evidence Image
For each E01 image in the case:
```bash
# Define variables
IMAGE="win7-32-nromanoff-c-drive.E01"
CASE_NAME="nromanoff"

# Create mount points
docker exec $(cat scratch/container_id.txt) mkdir -p /mnt/ewf/$CASE_NAME /mnt/windows/$CASE_NAME

# Mount E01
docker exec $(cat scratch/container_id.txt) ewfmount /evidence/$IMAGE /mnt/ewf/$CASE_NAME

# Find and mount NTFS partition (example using offset 0)
docker exec $(cat scratch/container_id.txt) mount -t ntfs -o ro,loop,offset=0 /mnt/ewf/$CASE_NAME/ewf1 /mnt/windows/$CASE_NAME
```

### 3. Verify All Mounts
```bash
docker exec $(cat scratch/container_id.txt) mount | grep /mnt/windows
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
docker exec $(cat scratch/container_id.txt) rip.pl -r /mnt/windows/nromanoff/Windows/System32/config/SOFTWARE -p run
```

### 3. Memory Analysis
Volatility 3 can be run against raw memory images in `/evidence`:
```bash
docker exec $(cat scratch/container_id.txt) vol -f /evidence/win7-32-nromanoff-memory-raw.001 windows.pslist
```

## Troubleshooting

- **Mount Denied**: Ensure the container is started with `--privileged`.
- **Path Issues**: Always use absolute paths within `docker exec` commands or relative paths from the container's root.
- **EWF Mount Fails**: Check if another process is using the E01 or if the mount point is not empty.
