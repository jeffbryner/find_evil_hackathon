---
name: analyze-windows-artifacts
description: Investigate Windows-specific forensic artifacts including persistence, execution history, file activity, and memory. Use this skill when analyzing a Windows evidence image or memory dump to answer questions like "What was executed?", "How did they stay?", and "What files were accessed?".
---

# Windows Forensic Analysis Guide

This skill provides a domain-oriented approach to Windows forensics, leveraging the SIFT workstation's tools. It is organized by investigative goals rather than individual tools.

## Investigative Goals

### 1. Evidence of Execution
To determine what programs were run, when, and how many times.
- **Artifacts**: Prefetch, Shimcache, Amcache, BAM/DAM, UserAssist.
- **Guide**: [Execution Evidence](references/execution.md)

### 2. Persistence Mechanisms
To find how an attacker maintains access across reboots.
- **Artifacts**: Run Keys, Services, Scheduled Tasks, WMI Subscriptions.
- **Guide**: [Persistence Analysis](references/persistence.md)

### 3. File & Folder Activity
To track file creations, deletions, and folder browsing history.
- **Artifacts**: $MFT, $UsnJrnl, Shellbags, LNK Files, Jump Lists.
- **Guide**: [File & Folder Activity](references/file-activity.md)

### 4. User & System Events
To reconstruct a timeline of logons, process starts, and system changes.
- **Artifacts**: Security, System, and Application Event Logs.
- **Guide**: [Event Log Analysis](references/event-logs.md)

### 5. Memory Forensics
To find injected code, hidden processes, and active network connections.
- **Artifacts**: RAM Image (Volatility 3).
- **Guide**: [Memory Analysis](references/memory.md)

### 6. System Usage & Exfiltration
To track data volumes, browser history, and deleted files.
- **Artifacts**: SRUM, Browser History, Recycle Bin.
- **Guide**: [System Usage](references/system-usage.md)

## General SIFT Workflow

1. **Mount Evidence**: Use `sift-docker` skill to ensure `/mnt/windows` is ready.
2. **Triage/Extract**: Use Sleuthkit (`fls`, `icat`) to pull hives and artifact files to `scratch/`.
3. **Parse**: Use EZ Tools (via `dotnet /opt/zimmermantools/...`) to convert artifacts to CSV.
4. **Analyze**: Use DuckDB (via `query_parquet.py`) or Timeline Explorer to find anomalies.
