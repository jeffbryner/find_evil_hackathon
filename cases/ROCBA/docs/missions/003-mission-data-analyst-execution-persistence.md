# Mission: Hunt Process Execution and Persistence Mechanisms
**Target Agent:** data-analyst

## Purpose
Identify all processes executed by the attacker, commands run, and any persistence mechanisms established on the `SRL-FORGE` system.

## Background
We know that the attacker accessed Fred's system via RDP during his vacation (2020-11-10 to 2020-11-15). We need to identify exactly what commands and tools they executed (e.g., SDelete, PowerShell, command prompts, or custom malware) and whether they established any persistence to remain on the system.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no process execution or persistence artifacts are found, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Execute the `hunt-execution-sop` to find process execution history in Prefetch, AppCompatCache, and Event Logs (Event ID 4688) for the period of Fred's vacation (2020-11-10 to 2020-11-15).
- [x] Search for execution of command-line tools like `cmd.exe`, `powershell.exe`, `wscript.exe`, `cscript.exe`, `sdelete.exe`, and any other suspicious binaries.
- [x] Decode any base64-encoded or obfuscated PowerShell commands found in the execution history or event logs (none found; engine logs show automated health check/ping scripts running).
- [x] Execute the `hunt-persistence-sop` to find persistence mechanisms (Registry Run keys, Scheduled Tasks, Services).
- [x] Update `cases/ROCBA/docs/shared_facts.md` with any discovered malicious files, tools, or persistence mechanisms.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  - Conducted high-speed schema discovery and SQL queries against `artifacts_timeline` parquet files using DuckDB.
  - Queried Prefetch execution history (`windows:prefetch:execution`) during Fred's vacation window (2020-11-10 to 2020-11-15) to identify executed programs.
  - Investigated Windows Security Event Logs (`windows:evtx:record`) for process creation events (Event ID 4688) and PowerShell engine logs to reconstruct command lines.
  - Searched Registry Run keys (`windows:registry:run`) and services to uncover persistence mechanisms.
  - Analyzed authentication logs for external malicious IPs and brute-force activity.
- **Findings:**
  - **Suspicious Tool Executions:**
    - **DameWare Mini Remote Control (`MRC.EXE`):** Executed on `2020-11-10 14:00:54` and `2020-11-14 11:33:04`.
    - **Sysinternals SDelete (`SDELETE.EXE`):** Executed on `2020-11-14 11:34:00` (immediately following DameWare).
    - **PowerShell (`powershell.exe`):** Executed multiple times daily between Nov 10 and Nov 14. Event log analysis of engine startup logs revealed these were automated health check/ping scripts (`Write-Host 'Final result: 1'`).
  - **Persistence Mechanism:**
    - Identified a highly suspicious Run key created on `2020-11-10 06:12:41.621546-08:00` under `HKEY_CURRENT_USER\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`:
      `C18E42C7363A0E298C5594A2ABE53A0760B71220._service_run: "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" --type=service /prefetch:8`. This masquerades as Microsoft Edge but uses a SHA-1 hash name and suspicious arguments to run on startup.
  - **External Brute-Force Activity:**
    - Discovered a massive NTLM brute-force attack originating from external IP `85.14.242.76` starting on `2020-11-13 15:12:38` and continuing through `2020-11-14 06:15:09`, targeting 30+ different usernames. No successful logons (Event ID 4624) from this IP were recorded.
- **Confidence Rating:** 5/5
- **Budget Tally:**
  - **Orientation Budget:** 5 / 5 tool calls
  - **Execution Budget:** 20 / 20 tool calls
  - **Reporting Budget:** 4 / 5 tool calls
- **NPS / Feedback:** 10/10 - The DuckDB/Parquet timeline pipeline is extremely powerful and allowed us to quickly pivot from process execution to registry persistence and brute-force IP discovery!
