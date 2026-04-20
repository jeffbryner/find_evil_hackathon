---
name: init_case
description: Starts the SIFT container and mounts one or more evidence images for a specific case.
---

# Command: Initialize Forensic Case
# Description: Starts the SIFT container (if not running) and mounts evidence images for a named case.

## Steps
1. Execute `./helpers/init_case.sh --case <case_name> <evidence_file_1> [<evidence_file_2> ...]`.
2. Verify that `scratch/container_id.txt` exists and contains a valid Docker container ID.
3. Confirm that evidence is mounted at `/mnt/cases/<case_name>/<evidence_basename>` inside the container.

## Usage Example
```bash
./helpers/init_case.sh --case Aegis images/win7-c-drive.E01
```
