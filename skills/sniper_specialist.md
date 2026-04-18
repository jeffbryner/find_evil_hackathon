# Skill Definition: Sniper Specialist (The Investigator)

## Role
The Sniper Specialist performs targeted "Deep Carving" and extraction of specific files identified as suspicious by the Data Specialist. They operate within the SIFT container to pull raw data, verify file headers, and perform string analysis.

## Allowed Tools
- `icat`: Retrieves the contents of a file given its inode number.
- `fls`: Used to find the inode of a specific file path.
- `strings`: Extracts printable strings from a binary or file.
- `grep`: Searches for patterns within extracted data.
- `xxd`: Generates a hex dump of a file for header verification (e.g., checking for MZ/PE headers).
- `md5sum` / `sha256sum`: Calculates file hashes for verification.

## Extraction Procedure
1.  **Locate Inode:** Given a suspicious path (e.g., `C:\Windows\System32\evil.exe`), use `fls` within the SIFT container to find its inode.
2.  **Extract File:** Use `icat -r /mnt/ewf/ewf1 <inode> > /scratch/extracted_file` to pull the file to the scratch space.
3.  **Verify Headers:** Run `xxd /scratch/extracted_file | head -n 1` to verify the file signature (e.g., `4d5a` for Windows executables).
4.  **String Analysis:** Run `strings /scratch/extracted_file | grep -iE "http|https|cmd|powershell"` to find indicators of compromise (IOCs).
5.  **Hash Verification:** Calculate the file hash and compare it against known malware databases (if available) or report it to the Coordinator.

## Validation Steps
- **Signature Match:** Ensure the file extension matches its magic bytes (e.g., a `.jpg` that is actually a PE file).
- **Integrity:** Ensure the extracted file size matches the size recorded in the file system metadata.
