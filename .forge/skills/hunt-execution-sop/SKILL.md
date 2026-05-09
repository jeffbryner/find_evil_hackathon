---
name: hunt-execution-sop
description: This skill provides a Standard Operating Procedure (SOP) for the `data-analyst` agent to hunt for process execution history using DuckDB and Parquet.
---
# Hunt Execution SOP

This skill provides a Standard Operating Procedure (SOP) for the `data-analyst` agent to hunt for process execution history using DuckDB and Parquet.

## Trigger
Use this skill when the Case Lead delegates a task to "Execute the hunt-execution-sop skill" targeting a specific binary, host, or time window.

## Execution Steps

1.  **Query Prefetch Execution:**
    Execute the following SQL to find execution evidence in Prefetch (which proves a binary actually ran):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:prefetch:execution' 
      AND (LOWER(message) ILIKE '%<TARGET_BINARY>%' OR timestamp BETWEEN '<START_TIME>' AND '<END_TIME>')
    ORDER BY timestamp DESC;
    ```

2.  **Query AppCompatCache (Shimcache):**
    Execute the following SQL to find evidence of binaries being present on the system (even if deleted or not recently executed):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:registry:appcompatcache' 
      AND LOWER(message) ILIKE '%<TARGET_BINARY>%'
    ORDER BY timestamp DESC;
    ```

3.  **Query Process Creation Events (4688):**
    Execute the following SQL to find command-line arguments associated with the execution (if logging was enabled):
    ```sql
    SELECT timestamp, imagename, message 
    FROM artifacts_timeline 
    WHERE data_type = 'windows:evtx:record' AND message ILIKE '%4688%' 
      AND LOWER(message) ILIKE '%<TARGET_BINARY>%'
    ORDER BY timestamp DESC;
    ```

4.  **Analyze Findings:**
    Determine the first and last time the target binary was executed. Identify the path it was executed from and any command-line arguments used.

5.  **Report to Case Lead:**
    Return a structured timeline of the binary's execution, including the source artifact (Prefetch, AppCompatCache, EVTX) and the execution context.
