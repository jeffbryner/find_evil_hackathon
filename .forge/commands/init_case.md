---
name: init_case
description: Starts the SIFT container and mounts the evidence image.
---

# Command: Initialize Forensic Case
# Description: Starts the SIFT container and mounts the evidence image.

## Steps
1. Execute `./helpers/init_case.sh`.
2. Verify that `scratch/container_id.txt` exists and contains a valid Docker container ID.
3. Confirm that the evidence is mounted at `/mnt/windows` inside the container.

## Usage Example
```bash
./helpers/init_case.sh
```
