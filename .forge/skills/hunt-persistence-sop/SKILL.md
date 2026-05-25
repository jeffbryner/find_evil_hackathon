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
    ORDER BY timestamp DESC;
    ```

2.  **Query Scheduled Tasks:**
    Execute the following SQL to find scheduled task creation events (Event ID 4698):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND message ILIKE '%4698%'
    ORDER BY timestamp DESC;
    ```

3.  **Query Service Creation:**
    Execute the following SQL to find new service installations (Event ID 7045 or 4697):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND (message ILIKE '%7045%' OR message ILIKE '%4697%')
    ORDER BY timestamp DESC;
    ```

4.  **Analyze Findings & Log IOCs:**
    Review the output for suspicious binaries (e.g., executing out of `C:\Windows\Temp`, `C:\Users\Public`, or randomly named executables).
    
    **CRITICAL:** For any identified suspicious IP, domain, file path, registry key, or hash, you **MUST** immediately register it as an Indicator of Compromise (IOC) using `ioc_tracker.py` before completing your turn. This ensures parallel sub-agents can automatically correlate and join your findings.
    
    *Example:*
    ```bash
    uv run helpers/ioc_tracker.py --case <case_name> --add registry_key --value "HKCU\Software\Microsoft\Windows\CurrentVersion\Run\msedge_service" --source hunt-persistence-sop
    ```

5.  **Report to Case Lead:**
    Return a structured JSON or Markdown summary of the suspicious persistence mechanisms found, including timestamps, hostnames (`imagename`), the exact payloads, and a list of logged IOCs.
