---
name: triage_image
description: Extracts a filesystem timeline (bodyfile) and converts it to Parquet for local analysis.
---

# Command: Triage Disk Image
# Description: Extracts a filesystem timeline (bodyfile) and converts it to Parquet for local analysis.

## Prerequisites
- Case must be initialized (SIFT container running).

## Steps
1. Use `docker exec` to run `tsk_gettimes` on the raw evidence image inside the running SIFT container:
   ```bash
   # Replace <case_name> and <evidence_name> with actual names
   docker exec $(cat scratch/container_id.txt) bash -c 'tsk_gettimes /mnt/ewf/<case_name>/<evidence_name>/ewf1 > /scratch/<case_name>/<evidence_name>/bodyfile.txt'
   ```
2. Convert the generated bodyfile to a Parquet file for high-speed local analysis:
   ```bash
   ./helpers/convert_bodyfile.sh scratch/<case_name>/<evidence_name>/bodyfile.txt scratch/<case_name>/<evidence_name>/file_metadata.parquet
   ```
3. Verify `scratch/<case_name>/<evidence_name>/file_metadata.parquet` exists.

## Notes
- `/mnt/ewf/<case_name>/<evidence_name>/ewf1` is the path for the raw disk device exposed by `ewfmount` in the SIFT container.
- The `scratch/` directory is shared between the host and the container.
