---
name: parse-windows-mail
description: Standard operating procedure for parsing Windows Mail ESE databases (store.vol) into queryable Parquet format using either a structured ESE exporter or a high-performance binary carver script. Use when asked to investigate Windows Mail databases, extract emails from store.vol, or convert ESE databases to Parquet.
---

# Parse Windows Mail (store.vol)

This skill provides a complete workflow and custom scripts to parse Windows Mail Extensible Storage Engine (ESE) databases (`store.vol`) and convert them into structured queryable Parquet format.

Because Windows Mail databases on live systems are often in a **Dirty Shutdown** state or contain corrupted indexes, standard tools like `esedbexport` can fail with errors such as `unable to retrieve leaf value by key`. To solve this, this skill provides two distinct methods:

1. **Method A: High-Performance Binary Carver (Recommended for Corrupted/Dirty Databases)**
2. **Method B: Structured ESE Exporter (For Healthy Databases)**

---

## Method A: High-Performance Binary Carver (Recommended)

When `esedbexport` fails with index or leaf errors, the database contains corrupt index trees but the raw pages still contain intact UTF-16LE text. Our custom binary carver script `carve_vol_to_parquet.py` scans the raw binary pages of `store.vol`, carves out complete email headers and message bodies, parses them into a structured schema, and saves them directly to a Parquet file.

### How to Run:
Run the carver script directly on the host using `uv`:

```bash
# Specify the domains of interest. Be sure the .parquet file lands in the scratch/IMAGE_NAME/parquet/ directory for dynamic access.
uv run .forge/skills/parse-windows-mail/scripts/carve_vol_to_parquet.py \
  cases/<CASEID>/scratch/path/to/a_mail_store.vol \
  cases/<CASEID>/scratch/<IMAGE_NAME>/parquet/windows_mail.parquet \
  "suspect1.com,suspect2.gov,evil.org"
```

This carver:
- Scans for SMTP headers and boundary patterns matching the specified domains.
- Extracts sender, recipient, CC, subject, date, and message body.
- Handles UTF-16LE and UTF-8 encoding.
- Outputs a clean, queryable Parquet file containing structured emails.

---

## Method B: Structured ESE Exporter (For Healthy Databases)

If the database is healthy and has been cleanly shut down:

### 1. Verify Database State
Verify the database state using `esedbinfo` inside the SIFT container:

```bash
docker exec <container_name> esedbinfo "/mnt/cases/<case_id>/<image_name>/path/to/store.vol"
```

### 2. Export ESE Tables
Use `esedbexport` inside the SIFT container to dump all tables and long values (like message bodies) from the `store.vol` database into CSV files. 

* **Important**: Always output to the read-write shared `/scratch/` directory inside the container so the exported files are accessible on the host.

```bash
docker exec <container_name> esedbexport -m all -t /scratch/windows_mail_export "/mnt/cases/<case_id>/<image_name>/path/to/store.vol"
```
This will create:
- `/scratch/windows_mail_export/` containing:
  - `Table - Message.csv` (contains message metadata)
  - `Table - Recipient.csv` (contains recipient lists)
  - `LongValue/` folder (contains raw message body text files)

### 3. Normalize and Convert to Parquet
Once exported, run the automated `parse_windows_mail.py` script on the host to parse the exported CSV files and LongValue folder into a unified, structured Parquet table:

```bash
uv run .forge/skills/parse-windows-mail/scripts/parse_windows_mail.py \
  cases/<case_id>/scratch/windows_mail_export \
  cases/<case_id>/scratch/<image_name>/parquet/windows_mail.parquet
```

---

## Querying the Parquet File in DuckDB

Whichever method you use, the output is a unified Parquet file. You can query it using DuckDB:

```sql
SELECT sender, recipient, subject, date, body 
FROM windows_mail 
WHERE body ILIKE '%interesting_thing1%' OR body ILIKE '%interesting_thing2%';
```
