---
name: carve-file-sop
description: This skill provides a Standard Operating Procedure (SOP) for the `sniper-forensics` agent to recover deleted files or extract specific files from a disk image using Sleuthkit (`fls` and `icat`) within the SIFT Docker container.
---

# Carve File SOP

This skill provides a Standard Operating Procedure (SOP) for the `sniper-forensics` agent to recover deleted files or extract specific files from a disk image using Sleuthkit (`fls` and `icat`) within the SIFT Docker container.

## Trigger
Use this skill when the Case Lead delegates a task to "Execute the carve-file-sop skill" to recover a specific file from a disk image.

## Execution Steps

1.  **Locate the Inode (fls):**
    First, use `fls` to search the directory structure of the disk image to find the inode number of the target file.
    ```bash
    docker exec $(cat scratch/container_id.txt) fls -r /mnt/cases/<CASE_NAME>/<IMAGE_NAME> | grep -i "<TARGET_FILE_NAME>"
    ```
    *Note: The output will look like `r/r * 12345-128-4: TargetFile.txt`. The number `12345-128-4` is the inode.*

2.  **Extract the File (icat):**
    Once you have the inode, use `icat` to extract the file content and save it to the `scratch/` directory.
    ```bash
    docker exec $(cat scratch/container_id.txt) icat /mnt/cases/<CASE_NAME>/<IMAGE_NAME> <INODE_NUMBER> > scratch/<CASE_NAME>/<OUTPUT_FILE_NAME>
    ```

3.  **Verify Extraction:**
    Check the size and type of the extracted file to ensure the carving was successful.
    ```bash
    ls -lh scratch/<CASE_NAME>/<OUTPUT_FILE_NAME>
    file scratch/<CASE_NAME>/<OUTPUT_FILE_NAME>
    ```
    *(Optional) If the file is an archive (e.g., ZIP), you can list its contents using `unzip -l` or `7z l` to verify integrity.*

4.  **Report to Case Lead:**
    Return a structured summary including the exact commands used, the inode found, the extraction status, and the location of the carved file in the `scratch/` directory.
