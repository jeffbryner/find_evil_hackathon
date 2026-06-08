---
name: carve-file-sop
description: This skill provides a Standard Operating Procedure (SOP) for the `sniper-forensics` agent to recover deleted files or extract specific files from a disk image using Sleuthkit (`fls` and `icat`) within the SIFT Docker container.
---

# Carve File SOP

This skill provides a Standard Operating Procedure (SOP) for the `sniper-forensics` agent to recover deleted files or extract specific files from a disk image using Sleuthkit (`fls` and `icat`) within the SIFT Docker container.

## Trigger
Use this skill when the Case Lead delegates a task to "Execute the carve-file-sop skill" to recover a specific file from a disk image.

## Execution Steps

1.  **Locate the Inode **

    **Option: via parquet search:**
    Use `uv run helpers/query-parquet.py` to search the parquet file for the target file name and retrieve its inode number.
    ```bash
    uv run helpers/query-parquet.py --case <CASE_NAME> --query "SELECT details->>'Meta' as inode,* FROM fs_timeline WHERE file_name_lower ILIKE '%<TARGET_FILE_NAME>%'"
    ```
    **Option: via fls:**
    Use `fls` to search the directory structure of the disk image to find the inode number of the target file.
    ```bash
    docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) fls -r /mnt/cases/<CASE_NAME>/<IMAGE_NAME> | grep -i "<TARGET_FILE_NAME>"
    ```
    *Note: The output will look like `r/r * 12345-128-4: TargetFile.txt`. The number `12345-128-4` is the inode.*

2.  **Extract the File (icat):**
    Once you have the inode, use `icat` to extract the file content and save it to the `scratch/` directory.
    ```bash
    docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) icat /mnt/cases/<CASE_NAME>/<IMAGE_NAME> <INODE_NUMBER> > scratch/<CASE_NAME>/<OUTPUT_FILE_NAME>
    ```

3.  **Verify Extraction:**
    Check the size and type of the extracted file to ensure the carving was successful.
    ```bash
    ls -lh scratch/<CASE_NAME>/<OUTPUT_FILE_NAME>
    file scratch/<CASE_NAME>/<OUTPUT_FILE_NAME>
    ```
    *(Optional) If the file is an archive (e.g., ZIP), you can list its contents using `unzip -l` or `7z l` to verify integrity.*

## Advanced Recovery Techniques (Lessons Learned)

When standard file name searches fail or secure wipe tools (like SDelete) are executed, use these advanced techniques:

1.  **Search by File Size:**
    If the target file has been renamed (e.g., moved to the Recycle Bin as `$R...`), query the filesystem timeline or MFT records for the exact byte size of the target file rather than its name.
    
2.  **Audit Cloud Sync Cache Databases:**
    If the file was staged in a cloud-sync directory (e.g., Google Drive File Stream, OneDrive), inspect local sync client databases (e.g., SQLite metadata databases) to map the target file to its local cache file ID (`stable_id`). This reveals the cache file name and original size even if the file is deleted.

3.  **Check for Attacker Operational Errors:**
    Attackers often execute secure deletion tools (like SDelete) but subsequently perform standard deletions on other copies or files (e.g., deleting the original local file after wiping the cloud cache). Always audit the `$Recycle.Bin` directory and active/deleted MFT records for the target size, as these files may remain completely intact and allocated.

4.  **Verify Magic Bytes & Integrity:**
    Ensure the carved file starts with the correct magic bytes (e.g., `!BDN` or `21 42 44 4E` in hex for Microsoft Outlook PST files) before attempting parsing.

4.  **Report to Case Lead:**
    Return a structured summary including the exact commands used, the inode found, the extraction status, and the location of the carved file in the `scratch/` directory.
