---
name: parse-email-databases
description: Extract, parse, and analyze local email databases (OST, PST, MSG, EML, MBOX) from forensic images, search for exfiltration indicators, and correlate communications with filesystem timelines.
---

# Parse Email Databases

This skill provides standard operating procedures and automated scripts to parse local email databases (like Outlook OST/PST files) extracted from Windows, Linux, or Mac evidence images.

## Core Workflow

### 1. Verify and Analyze the Database Integrity
Before exporting, verify the database content type and check for encryption or corruption using `pffinfo` inside the SIFT container:

```bash
docker exec <container_name> pffinfo "/mnt/cases/<case_id>/<image_name>/path/to/database.ost"
```

### 2. Extract Database Contents
Use `pffexport` to extract all allocated, orphan, and recovered items from the database. It is recommended to output the results to a directory in `/scratch/`:

```bash
docker exec <container_name> pffexport -m all -t /scratch/ost_export "/mnt/cases/<case_id>/<image_name>/path/to/database.ost"
```
This will create:
- `/scratch/<image_name>/ost_export.export` (Allocated items)
- `/scratch/<image_name>/ost_export.recovered` (Orphan and recovered items)

### 3. Normalize and Parse Extracted Messages
Run the automated `parse_emails.py` script to parse the extracted directories into structured JSON, Parquet, and Markdown formats.

It is important to include the <image_name> in the output paths so parquet files are organized by image and can be easily queried in the DuckDB pipeline later.

```bash
uv run .forge/skills/parse-email-databases/scripts/parse_emails.py \
  -e cases/<case_id>/scratch/<image_name>/ost_export.export \
  -r cases/<case_id>/scratch/<image_name>/ost_export.recovered \
  -j cases/<case_id>/scratch/<image_name>/emails.json \
  -p cases/<case_id>/scratch/<image_name>/parquet/emails.parquet \
  -m cases/<case_id>/scratch/<image_name>/email_report.md
```

### 4. Perform SQL Hunting
Once the email database is converted to Parquet format, you can use the DuckDB pipeline to run advanced hunting queries.
See [email-hunting-recipes.md](references/email-hunting-recipes.md) for pre-built SQL hunting recipes, including:
- Cloud staging and exfiltration URL hunts.
- USB and physical media delivery hunts.
- Temporal joins correlating emails with filesystem timeline activity.
