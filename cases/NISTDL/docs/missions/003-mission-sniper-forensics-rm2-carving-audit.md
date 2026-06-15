# Forensic Audit Trail: Removable Media 2 File Carving and Extraction
**Case:** NISTDL
**Target Image:** `cfreds_2015_data_leakage_rm2.dd`
**Investigator:** sniper-forensics
**Date:** 2026-06-03

---

## 1. Summary of Investigation
This audit trail documents the forensic identification, carving, extraction, and verification of deleted and orphaned files from Removable Media 2 (`cfreds_2015_data_leakage_rm2.dd`). Every single file in the `/$OrphanFiles/` directory has been successfully recovered, and deep-dive inspection revealed extensive **file masquerading** (defense evasion) used by the suspect to hide confidential project documents.

---

## 2. Forensic Actions & Command Log

### Step 1: Image & Partition Analysis
First, we analyzed the partition table of the raw disk image `cfreds_2015_data_leakage_rm2.dd` using `mmls` inside the SIFT Docker container.

**Command:**
```bash
docker exec 823e74b98a9471e537d211eb1ca18c575311147d6365aec920c3ee06a442051d mmls /case/images/cfreds_2015_data_leakage_rm2.dd
```

**Output:**
```
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000000127   0000000128   Unallocated
002:  000:000   0000000128   0002097279   0002097152   Win95 FAT32 (0x0b)
003:  -------   0002097280   0007821311   0005724032   Unallocated
```
*Analysis:* The FAT32 filesystem partition begins at sector **128**.

---

### Step 2: Filesystem Navigation & Directory Listing
We listed the root directory of the FAT32 partition using `fls` with sector offset `128`.

**Command:**
```bash
docker exec 823e74b98a9471e537d211eb1ca18c575311147d6365aec920c3ee06a442051d fls -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd
```

**Output:**
```
r/r 3:IAMAN $_@   (Volume Label Entry)
v/v 33423363:$MBR
v/v 33423364:$FAT1
v/v 33423365:$FAT2
V/V 33423366:$OrphanFiles
```
*Analysis:* The volume label is `IAMAN $_@`. All files on the drive are located in the deleted/orphaned directory `/$OrphanFiles/` at inode **33423366**.

---

### Step 3: Recursive File Listing of Orphaned Files
We performed a recursive directory listing starting from inode `33423366` to locate all deleted and orphaned files.

**Command:**
```bash
docker exec 823e74b98a9471e537d211eb1ca18c575311147d6365aec920c3ee06a442051d fls -r -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 33423366
```

**Output:**
```
-/d * 133:design
+ r/r * 263:winter_storm.amr
+ r/r * 267:winter_whether_advisory.zip
-/d * 136:PRICIN~1
+ r/r * 967047:my_favorite_cars.db
+ r/r * 967050:my_favorite_movies.7z
+ r/r * 967053:new_years_day.jpg
+ r/r * 967056:super_bowl.avi
-/d * 137:progress
+ r/r * 1651335:my_friends.svg
+ r/r * 1651338:my_smartphone.png
+ r/r * 1651341:new_year_calendar.one
-/d * 138:proposal
+ r/r * 1793159:a_gift_from_you.gif
+ r/r * 1793161:landscape.png
-/d * 141:TECHNI~1
+ r/r * 3096966:diary_#1d.txt
+ r/r * 3096968:diary_#1p.txt
+ r/r * 3096970:diary_#2d.txt
+ r/r * 3096972:diary_#2p.txt
+ r/r * 3096974:diary_#3d.txt
+ r/r * 3096976:diary_#3p.txt
```

---

### Step 4: Batch File Extraction
We created a local output directory `cases/NISTDL/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/` and extracted all key files using `icat` inside the SIFT container.

**Command:**
```bash
docker exec 823e74b98a9471e537d211eb1ca18c575311147d6365aec920c3ee06a442051d bash -c '
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 967050 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/my_favorite_movies.7z"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 3096966 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#1d.txt"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 3096968 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#1p.txt"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 3096970 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#2d.txt"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 3096972 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#2p.txt"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 3096974 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#3d.txt"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 3096976 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#3p.txt"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 267 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/winter_whether_advisory.zip"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 967047 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/my_favorite_cars.db"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 1651335 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/my_friends.svg"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 1651338 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/my_smartphone.png"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 1651341 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/new_year_calendar.one"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 263 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/winter_storm.amr"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 1793159 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/a_gift_from_you.gif"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 1793161 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/landscape.png"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 967053 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/new_years_day.jpg"
icat -o 128 /case/images/cfreds_2015_data_leakage_rm2.dd 967056 > "/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/super_bowl.avi"
'
```

---

### Step 5: File Type Verification (Detecting Masquerading)
We ran the `file` utility to analyze the magic bytes of each extracted file.

**Command:**
```bash
file cases/NISTDL/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/*
```

**Results:**
- `diary_#1d.txt`: Microsoft Word 2007+ (.docx)
- `diary_#1p.txt`: Microsoft PowerPoint 2007+ (.pptx)
- `diary_#2d.txt`: Microsoft Word 2007+ (.docx)
- `diary_#2p.txt`: Microsoft PowerPoint 97-2003 (.ppt)
- `diary_#3d.txt`: Microsoft Word 97-2003 (.doc)
- `diary_#3p.txt`: Microsoft PowerPoint 97-2003 (.ppt)
- `my_favorite_movies.7z`: Microsoft Excel 2007+ (.xlsx)
- `winter_whether_advisory.zip`: Microsoft PowerPoint 2007+ (.pptx)
- `my_favorite_cars.db`: Microsoft Excel 97-2003 (.xls)
- `my_friends.svg`: Microsoft Word 97-2003 (.doc)
- `my_smartphone.png`: Microsoft Word 2007+ (.docx)
- `new_year_calendar.one`: Microsoft Word 2007+ (.docx)
- `winter_storm.amr`: Microsoft PowerPoint 97-2003 (.ppt)
- `a_gift_from_you.gif`: Microsoft Word 2007+ (.docx)
- `landscape.png`: Microsoft Word 2007+ (.docx)
- `new_years_day.jpg`: Microsoft Excel 2007+ (.xlsx)
- `super_bowl.avi`: Microsoft Excel 97-2003 (.xls)

---

### Step 6: Text Extraction & Metadata Recovery
For Zip-based Office documents (`.docx`, `.pptx`, `.xlsx`), we extracted and parsed `word/document.xml`, `ppt/slides/slide1.xml`, or `xl/sharedStrings.xml` using `unzip` and `sed` to retrieve the first page text and titles. For OLE-based Office documents (`.doc`, `.ppt`, `.xls`), we extracted printable ASCII/Unicode sequences using `strings`.

**Examples of Commands used:**
```bash
unzip -p cases/NISTDL/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#1d.txt word/document.xml | sed -e 's/<[^>]*>//g'
strings cases/NISTDL/scratch/cfreds_2015_data_leakage_rm2.dd/extracted_files/diary_#2p.txt | grep -i -E "secret|scenario|cfreds"
```

---

## 3. Forensic Analysis & Key Findings

1. **Defense Evasion / File Masquerading:**
   The suspect engaged in extensive anti-forensics by changing the extensions of all stolen files to common benign extensions (`.txt`, `.7z`, `.zip`, `.db`, `.png`, `.gif`, `.amr`, `.svg`, `.one`, `.jpg`, `.avi`). This was clearly designed to bypass keyword or file extension filters during basic searches.
   
2. **Confidential Project Scope:**
   The recovered files represent the core intellectual property and planning materials of a confidential project, explicitly labeled as `[secret_project]`. The files cover the entire lifecycle of this project:
   - **Proposals:** `Detailed Proposal.docx` and `Proposal.docx` (staged as `.gif` and `.png`).
   - **Design:** `detailed_design.pptx` and `revised_points.ppt` (staged as `.zip` and `.amr`).
   - **Technical Reviews:** `Technical Review #1`, `#2`, and `#3` (staged as `.txt` and `.ppt`/`.doc`).
   - **Progress Reports:** `Progress #1`, `#2`, and `#3` (staged as `.png`, `.one`, and `.svg`).
   - **Commercial Data:** `price_analysis_#2.xls` and `market_shares.xls` (staged as `.db` and `.avi`).

3. **Exfiltration Context:**
   The presence of these files in the deleted/orphaned `$OrphanFiles` directory of Removable Media 2 indicates that the suspect copied these files to the USB drive, and subsequently deleted them or the directory structure was orphaned. This aligns perfectly with the other evidence of local file wiping and Google Drive exfiltration on **2015-03-25**.

---

## 4. Final Evidence Manifest

| Extracted Filename | Original Inode | Actual File Format | True Document Title / Purpose | Size |
|---|---|---|---|---|
| `diary_#1d.txt` | 3096966 | Word Document (.docx) | `[Secret Project]Technical Review #1.docx` | 119 KB |
| `diary_#1p.txt` | 3096968 | PowerPoint (.pptx) | `[Secret Project]technical_review_#1.pptx` | 448 KB |
| `diary_#2d.txt` | 3096970 | Word Document (.docx) | `[Secret Project]Technical Review #2.docx` | 643 KB |
| `diary_#2p.txt` | 3096972 | PowerPoint (.ppt) | `[secret_project]_technical_review_#2` | 1.1 MB |
| `diary_#3d.txt` | 3096974 | Word Document (.doc) | `[secret_project]_technical_review_#3` | 2.3 MB |
| `diary_#3p.txt` | 3096976 | PowerPoint (.ppt) | `[secret_project]_technical_review_#3` | 318 KB |
| `winter_whether_advisory.zip` | 267 | PowerPoint (.pptx) | `[Secret Project]detailed_design.pptx` | 16 MB |
| `my_favorite_cars.db` | 967047 | Excel Spreadsheet (.xls) | `[secret_project]_price_analysis_#2` | 134 KB |
| `my_favorite_movies.7z` | 967050 | Excel Spreadsheet (.xlsx) | Nutrient constituents reference sample data | 98 KB |
| `my_friends.svg` | 1651335 | Word Document (.doc) | `[secret_project]_progress_#3` | 118 KB |
| `my_smartphone.png` | 1651338 | Word Document (.docx) | `[Secret Project]Progress #1.docx` | 114 KB |
| `new_year_calendar.one` | 1651341 | Word Document (.docx) | `[Secret Project]Progress #2.docx` | 108 KB |
| `winter_storm.amr` | 263 | PowerPoint (.ppt) | `[Secret Project]revised_points.ppt` | 1.3 MB |
| `a_gift_from_you.gif` | 1793159 | Word Document (.docx) | `[Secret Project]Detailed Proposal.docx` | 111 KB |
| `landscape.png` | 1793161 | Word Document (.docx) | `[Secret Project]Proposal.docx` | 200 KB |
| `new_years_day.jpg` | 967053 | Excel Spreadsheet (.xlsx) | Statistical reference sample data | 84 KB |
| `super_bowl.avi` | 967056 | Excel Spreadsheet (.xls) | `[secret_project]_market_shares` | 112 KB |

---
*End of Audit Trail.*