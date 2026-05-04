# Hunt Lateral Movement SOP

This skill provides a Standard Operating Procedure (SOP) for the `data-analyst` agent to hunt for lateral movement indicators using DuckDB and Parquet.

## Trigger
Use this skill when the Case Lead delegates a task to "Execute the hunt-lateral-movement-sop skill" on a specific host or across the environment.

## Execution Steps

1.  **Query Network Logons (RDP/SMB):**
    Execute the following SQL to find successful remote logons (Logon Type 3 for SMB/Network, Logon Type 10 for RDP - Event ID 4624):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND message LIKE '%4624%' AND (message LIKE '%Logon Type: 3%' OR message LIKE '%Logon Type: 10%')
    ORDER BY timestamp DESC LIMIT 50;
    ```

2.  **Query WMI Execution:**
    Execute the following SQL to find `wmic.exe` execution across the environment:
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:prefetch:execution' AND LOWER(message) LIKE '%wmic.exe%'
    ORDER BY timestamp DESC LIMIT 50;
    ```

3.  **Query Remote Service Creation:**
    Attackers often use tools like PsExec which create remote services. Query for Event ID 7045 (Service Control Manager):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND message LIKE '%7045%' AND LOWER(message) LIKE '%psexec%'
    ORDER BY timestamp DESC LIMIT 50;
    ```

4.  **Analyze Findings:**
    Correlate the source IPs from the 4624 events with the destination hosts where WMI or PsExec was executed. Identify the compromised accounts being used.

5.  **Report to Case Lead:**
    Return a structured summary of the lateral movement paths (Source Host -> Destination Host -> Account -> Tool used).
