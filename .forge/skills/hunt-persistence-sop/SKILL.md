---
name: hunt-persistence-sop
description: This skill provides a Standard Operating Procedure (SOP) for the `data-analyst` agent to hunt for common persistence mechanisms using DuckDB and Parquet.
---
# Hunt Persistence SOP

This skill provides a Standard Operating Procedure (SOP) for the `data-analyst` agent to hunt for common persistence mechanisms using DuckDB and Parquet.

## Trigger
Use this skill when the Case Lead delegates a task to "Execute the hunt-persistence-sop skill" on a specific host or across the environment.

## Execution Steps

1.  **Query Registry Run Keys:**
    Execute the following SQL to find all startup registry keys:
    ```sql
    SELECT timestamp, imagename, message, details->>'key_path' as registry_key
    FROM artifacts_timeline
    WHERE parser = 'winreg/run'
    ORDER BY timestamp DESC LIMIT 50;
    ```

2.  **Query Scheduled Tasks:**
    Execute the following SQL to find scheduled task creation events (Event ID 4698):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND message LIKE '%4698%'
    ORDER BY timestamp DESC LIMIT 50;
    ```

3.  **Query Service Creation:**
    Execute the following SQL to find new service installations (Event ID 7045 or 4697):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND (message LIKE '%7045%' OR message LIKE '%4697%')
    ORDER BY timestamp DESC LIMIT 50;
    ```

4.  **Analyze Findings:**
    Review the output for suspicious binaries (e.g., executing out of `C:\Windows\Temp`, `C:\Users\Public`, or randomly named executables).

5.  **Report to Case Lead:**
    Return a structured JSON or Markdown summary of the suspicious persistence mechanisms found, including timestamps, hostnames (`imagename`), and the exact payloads.
