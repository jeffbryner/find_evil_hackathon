# Hunt Exfiltration SOP

This skill provides a Standard Operating Procedure (SOP) for the `data-analyst` agent to hunt for data staging and exfiltration indicators using DuckDB and Parquet.

## Trigger
Use this skill when the Case Lead delegates a task to "Execute the hunt-exfiltration-sop skill" on a specific host or across the environment.

## Execution Steps

1.  **Query Archive File Creation (Staging):**
    Execute the following SQL to find newly created archive files (ZIP, RAR, 7Z, CAB, TAR) in suspicious or temporary directories:
    ```sql
    SELECT timestamp, imagename, message, details->>'Size' as file_size 
    FROM fs_timeline 
    WHERE (LOWER(message) LIKE '%.zip' OR LOWER(message) LIKE '%.rar' OR LOWER(message) LIKE '%.7z' OR LOWER(message) LIKE '%.cab')
      AND (LOWER(message) LIKE '%/temp/%' OR LOWER(message) LIKE '%/public/%' OR LOWER(message) LIKE '%/programdata/%' OR LOWER(message) LIKE '%/logs/%')
    ORDER BY timestamp DESC LIMIT 50;
    ```

2.  **Query Archiving Tool Execution:**
    Execute the following SQL to find execution of common archiving tools:
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:prefetch:execution' 
      AND (LOWER(message) LIKE '%makecab.exe%' OR LOWER(message) LIKE '%7z.exe%' OR LOWER(message) LIKE '%rar.exe%' OR LOWER(message) LIKE '%zip.exe%')
    ORDER BY timestamp DESC LIMIT 50;
    ```

3.  **Query SRUM Network Usage:**
    Execute the following SQL to find applications sending large amounts of data over the network (SRUM):
    ```sql
    SELECT timestamp, imagename, message, details->>'bytes_sent' as bytes_sent
    FROM artifacts_timeline 
    WHERE data_type LIKE '%srum%' AND CAST(details->>'bytes_sent' AS BIGINT) > 10000000
    ORDER BY CAST(details->>'bytes_sent' AS BIGINT) DESC LIMIT 50;
    ```

4.  **Analyze Findings:**
    Correlate the timestamps of archive creation with large outbound network connections or the execution of tunneling tools (e.g., PowerShell reverse port-forwards).

5.  **Report to Case Lead:**
    Return a structured summary of potential staging directories, created archives (including size and path), and any correlated network exfiltration events.
