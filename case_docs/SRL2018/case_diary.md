> **🚨 CURRENT INVESTIGATIVE STATE:** Pausing investigation after identifying major data exfiltration staging directories, archiving tools, and target files. Awaiting further direction from the user.

# Case Diary: SRL2018

## 1. Executive Summary
The environment has been compromised through a coordinated attack involving lateral movement, privilege escalation, and persistent access. The attacker utilized PsExec-style service creation and encoded PowerShell payloads. The attacker aggressively targeted sensitive data, staging files in anomalous directories (e.g., `C:\Windows\Logs\WindowsServerBackup\`, `/ProgramData/staging/mcollective_agents/`) and using archiving tools (`makecab.exe`, `7za.exe`, `rar.exe`) for exfiltration. Significant data targeted includes an "M&A Targets.zip" archive and a full Active Directory credential dump (NTDS.dit). Compromised accounts include `spsql`, `rsydow-a`, `cbarton-a`, and `tdungan`. 
*(Note: Initial findings regarding `Mnemosyne.sys` and `subject_srv.exe` have been identified as legitimate forensic activity originating from the response server `base-hunt` and are excluded from malicious indicators.)*

## 2. Timeline of Events
- **2018-07-17:** Staging of `mcollective-shell-agent-0.0.2.zip` and `mcollective-puppet-agent-1.13.0.zip` in `/ProgramData/staging/mcollective_agents/` on `base-file`.
- **2018-08-28 01:09:03:** PsExec-style lateral movement to `base-rd-01` (Service `24f8f7e` executing `3795920.exe` via `spsql`).
- **2018-08-30 16:42:44:** PsExec-style lateral movement to `base-rd-01` (Service `fb9f33e` executing `35da1b7.exe` via `spsql`).
- **2018-08-31 00:09:13:** PsExec-style lateral movement to `base-rd-02` (Service `df0398a` executing `5b1b72b.exe`).
- **2018-08-31 00:09:43:** Service `8556ce1` created on `base-rd-02` executing a large encoded PowerShell command.
- **2018-09-05 12:16:** Credential dumping on `base-dc`, creating copies of `ntds.dit`, `SYSTEM`, and `SECURITY` registry hives in `/temp/Active Directory/` and `/temp/registry/`.
- **2018-09-06 to 2018-09-07:** 
  - Multiple executions of encoded PowerShell on `base-file`.
  - Execution of `makecab.exe` across `base-dc`, `base-rd-01`, and `base-rd-02`.
  - Lateral movement activities involving accounts `cbarton-a` and `rsydow-a`.
  - Attacker tools (`7za.exe`, `rar.exe`, `procdump.exe`, `get_ma.bat`) staged in `C:\Users\rsydow-a\Documents\20180905\` on `base-file`.
  - Creation of `66.cab`, `67.cab`, `68.cab`, `69.cab` in `C:\Windows\Temp\perfmon\` on `base-file`.
- **2018-09-07 16:36:18:** Creation of `M&A Targets.zip` in `C:\Windows\Logs\WindowsServerBackup\7.15\` on `base-file` (subsequently deleted).

## 3. Findings & Analysis
- **Persistence Mechanisms:**
  - Encoded PowerShell Services: Used for persistent execution of malicious scripts (e.g., service `8556ce1` on `base-rd-02`).
- **Lateral Movement:**
  - Widespread use of the `ADMIN$` share to execute randomly named binaries (`5b1b72b.exe`, `35da1b7.exe`, `3795920.exe`).
  - Abuse of compromised accounts (`spsql`, `rsydow-a`, `cbarton-a`, `tdungan`).
- **Data Staging & Exfiltration:**
  - **Credential Theft:** The attacker successfully dumped Active Directory credentials (NTDS.dit) from `base-dc`.
  - **Targeted Data:** A highly suspicious archive named `M&A Targets.zip` was created on `base-file`, indicating targeted theft of Mergers & Acquisitions data.
  - **Staging Directories:** The attacker used multiple hidden or deceptive directories for staging data:
    - `C:\Windows\Logs\WindowsServerBackup\` (and subdirectories like `7.15`) on `base-file`.
    - `C:\Windows\Temp\perfmon\` on `base-file`.
    - `/ProgramData/staging/mcollective_agents/` on `base-rd-02` and `base-file`.
  - **Archiving Tools:** Extensive use of `makecab.exe`, `7za.exe`, and `rar.exe` to compress data prior to exfiltration.
- **Legitimate Forensic Activity (False Positives):**
  - `Mnemosyne.sys` and `subject_srv.exe` (F-Response) were used by the incident response team from `base-hunt` to gather memory images and are not part of the compromise.

## 4. MITRE ATT&CK Mapping
- **Initial Access:** Valid Accounts (T1078)
- **Execution:** Command and Scripting Interpreter (T1059) - PowerShell, Service Execution (T1569.002)
- **Persistence:** Create or Modify System Process: Windows Service (T1543.003)
- **Privilege Escalation:** Valid Accounts (T1078)
- **Defense Evasion:** Deobfuscate/Decode Files or Information (T1140), Indicator Removal on Host (T1070)
- **Credential Access:** OS Credential Dumping: NTDS (T1003.003)
- **Lateral Movement:** Remote Services: SMB/Windows Admin Shares (T1021.002)
- **Collection:** Archive Collected Data (T1560), Data from Local System (T1005)

## 5. Recommendations
1.  **Containment:** Isolate `base-dc`, `base-file`, `base-rd-01`, and `base-rd-02` from the network immediately.
2.  **Eradication:** 
    - Delete the staging directories (`/ProgramData/staging/`, `C:\Windows\Logs\WindowsServerBackup\`, `C:\Windows\Temp\perfmon\`).
    - Terminate any running instances of the randomly named executables (`5b1b72b.exe`, etc.).
    - Remove malicious services executing encoded PowerShell (e.g., `8556ce1`).
3.  **Credential Reset:** Force a global password reset, prioritizing the compromised accounts (`spsql`, `rsydow-a`, `cbarton-a`, `tdungan`), as the NTDS.dit file was compromised.
4.  **Further Investigation:** 
    - Decode the PowerShell payloads to understand their exact function.
    - Recover the deleted `M&A Targets.zip` to determine exactly what data was stolen.

## 6. Evidence Information
- **Disk Images:** `base-dc-cdrive.E01`, `base-file-cdrive.E01`, `base-rd-01-cdrive.E01`, `base-rd-02-cdrive.E01`
- **Memory Images:** 16 memory images across various hosts.
- Findings were extracted using timeline analysis (`artifacts_timeline`, `fs_timeline`) via DuckDB and Parquet queries.