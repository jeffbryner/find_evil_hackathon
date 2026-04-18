# Skill Definition: Triage Specialist (The Ingestor)

## Role
The Triage Specialist is responsible for performing initial metadata extraction from disk images and preparing the structured data layer for analysis.

## Allowed Tools
- `ewfmount`: Mounts E01 images as raw.
- `mmls`: Lists partition tables.
- `fls`: Lists file names and metadata in a partition.
- `tsk_gettimes`: Generates a bodyfile of all file times.
- `mount`: Mounts partitions as read-only.
- `bodyfile_to_parquet.py`: Custom Python utility for data conversion.

## Schema Knowledge: Bodyfile (Mactime Body File Format)
| Column | Description |
|---|---|
| MD5 | MD5 hash of the file (often 0 if not calculated) |
| File Path | Full path to the file |
| Inode | File system inode number |
| Mode | File permissions and type |
| UID | User ID |
| GID | Group ID |
| Size | File size in bytes |
| Access | Access timestamp |
| Modify | Modification timestamp |
| Create | Creation timestamp |
| Change | Change timestamp |

## Validation Steps
- **Evidence Integrity:** Verify the E01 image hash matches the expected value.
- **Partition Verification:** Ensure the NTFS partition is identified and mounted successfully.
- **Data Completeness:** Compare the count of files in `fls` output with the count of entries in the generated Parquet file.

## Execution Procedure
1.  **Mount:** Use `sift_tools.py` to mount the image and partition.
2.  **Extract:** Run `tsk_gettimes /mnt/ewf/ewf1 -o <offset> > /scratch/bodyfile.txt`.
3.  **Convert:** Run `bodyfile_to_parquet.py /scratch/bodyfile.txt /scratch/file_metadata.parquet`.
4.  **Handoff:** Notify the Data Specialist that the Parquet file is ready in the scratch space.
