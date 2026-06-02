# Email Forensic Hunting Recipes

This reference documents common SQL hunting recipes for analyzing parsed email databases (Parquet format) using DuckDB.

## Ingesting and Previewing Emails

To load the parsed email Parquet database and view the schema:

```sql
-- Preview schema and first 5 emails
SELECT * FROM read_parquet('emails.parquet') LIMIT 5;

-- Get total count of emails by source (allocated vs. recovered)
SELECT source, count(*) as count 
FROM read_parquet('emails.parquet') 
GROUP BY source;
```

---

## 1. Hunting for Exfiltration & Cloud Staging

To identify emails discussing cloud storage services (like Google Drive, Dropbox, OneDrive, iCloud) or containing cloud URLs:

```sql
SELECT delivery_time, sender_name, subject, body 
FROM read_parquet('emails.parquet') 
WHERE lower(subject) LIKE '%drive%' 
   OR lower(body) LIKE '%drive%'
   OR lower(body) LIKE '%dropbox%'
   OR lower(body) LIKE '%file%'
   OR body LIKE '%http%://%drive.google.com%'
ORDER BY delivery_time;
```

---

## 2. Hunting for Anti-Forensics & USB Staging

To identify discussions about external storage devices, physical delivery, or anti-forensics tools (like Eraser, CCleaner):

```sql
SELECT delivery_time, sender_name, subject, body 
FROM read_parquet('emails.parquet') 
WHERE lower(subject) LIKE '%usb%' 
   OR lower(body) LIKE '%usb%'
   OR lower(subject) LIKE '%storage%'
   OR lower(body) LIKE '%storage%'
   OR lower(body) LIKE '%device%'
   OR lower(body) LIKE '%eraser%'
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
  FROM read_parquet('emails.parquet')
)
SELECT 
  f.write_time,
  f.file_path,
  e.email_time,
  e.sender_name,
  e.subject
FROM read_parquet('fs_timeline.parquet') f
JOIN parsed_emails e 
  ON abs(epoch(f.write_time) - epoch(e.email_time)) <= 600 -- within 10 minutes
ORDER BY f.write_time;
```
