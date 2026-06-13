# Email Forensic Hunting Recipes

This reference documents common SQL hunting recipes for analyzing parsed email databases (Parquet format) using DuckDB.

## Ingesting and Previewing Emails

Using the `query_parquet.py` helper tool: 

```sql
-- Preview schema and first 5 emails
SELECT * FROM emails LIMIT 5;

-- Get total count of emails by source (allocated vs. recovered)
SELECT source, count(*) as count 
FROM emails 
GROUP BY source;
```

---

## 1. Hunting for Exfiltration & Cloud Staging

To identify emails discussing cloud storage services (like Google Drive, Dropbox, OneDrive, iCloud) or containing cloud URLs:

```sql
SELECT delivery_time, sender_name, subject, body 
FROM emails 
WHERE subject ILIKE '%drive%' 
   OR body ILIKE '%drive%'
   OR body ILIKE '%dropbox%'
   OR body ILIKE '%file%'
   OR body ILIKE '%http%://%drive.google.com%'
ORDER BY delivery_time;
```

---

## 2. Hunting for Anti-Forensics & USB Staging

To identify discussions about external storage devices, physical delivery, or anti-forensics tools (like Eraser, CCleaner):

```sql
SELECT delivery_time, sender_name, subject, body 
FROM emails
WHERE subject ILIKE '%usb%' 
   OR body ILIKE '%usb%'
   OR subject ILIKE '%storage%'
   OR body ILIKE '%storage%'
   OR body ILIKE '%device%'
   OR body ILIKE '%eraser%'
ORDER BY delivery_time;
```

---

## 3. Correlation with Filesystem Timelines

To correlate email delivery times with filesystem activity (e.g., finding files accessed or created within 10 minutes of an email exchange):

```sql
-- Join emails with filesystem timeline (assuming standard datetime formats)
-- Adjust strptime format if needed based on the email delivery_time string
WITH parsed_emails AS (
  SELECT 
    strptime(substring(delivery_time, 1, 20), '%b %d, %Y %H:%M:%S') AS email_time,
    sender_name,
    subject
  FROM emails
)
SELECT 
  f.timestamp,
  f.file_name_lower,
  e.email_time,
  e.sender_name,
  e.subject
FROM fs_timeline as f
JOIN parsed_emails e 
  ON abs(epoch(f.timestamp) - epoch(e.email_time)) <= 600 -- within 10 minutes
ORDER BY f.timestamp ;
```
