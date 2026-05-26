# Mission: USB Devices and Memory Forensics
**Target Agent:** data-analyst

## Purpose
Investigate the connected USB devices (drives D:, E:, F:) to identify their serial numbers, vendors, and connection times. Additionally, analyze the memory image (`rocba-memory.raw`) using volatile memory tables (like `memory_netscan`, `memory_pslist`) to identify active network connections, remote IPs, and processes during the exfiltration window.

## Background
We know that external USB drives D:, E:, and F: were connected around the time of the exfiltration, and a local Google Drive folder G: was utilized. We also know that the actor accessed a raw memory dump on November 15, 2020. We need to identify the physical device details and analyze the volatile memory of the system.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 25 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no USBSTOR registry keys or memory tables are found, stop and report immediately.

## Task Checklist
- [x] Map drive letters D:, E:, and F: to their physical serial numbers, volume labels, and vendors using ShellBags and USBSTOR artifacts.
- [x] Query `memory_netscan` (if available) to find active network connections, local/remote IPs, and associated processes.
- [x] Query `memory_pslist` (if available) to find running processes, especially related to RDP, cloud clients, or memory analysis.
- [x] Identify any other external connections or remote login indicators (e.g., RDP connections, network redirects).
- [x] Update `cases/ROCBA/docs/shared_facts.md` with findings.
- [x] Update this mission card with results.

## Results & Post-Mortem
### Approach
1. **Orientation**: Verified schema of memory and registry tables using DuckDB/Parquet via `query_parquet.py`.
2. **USB Device Mapping**: Queried `artifacts_timeline` for `USBSTOR`, `WPDBUSENUM`, `MountedDevices`, ShellBags, and LNK files to map drive letters to volume serial numbers and physical hardware serials.
3. **Memory Analysis**: Queried `memory_pslist` and `memory_netscan` to analyze active network connections, running processes, and external remote control sessions.

### Findings
1. **USB Device Mapping**:
   - **Drive D:** Volume Label `SRL IRT` (Volume Serial: `0xfc3ee602`) maps to physical device **SMI Generic Mass Storage USB Device** (Serial: `121118-1061200001494`, VID: `090C`, PID: `1000`). First connected/migrated: `2020-11-01 17:12:24`. Used for staging raw memory dump `Rocba-Memory.raw` and keys.
   - **Drive E:** Volume Label `Homework` (Volume Serial: `0x5e938bfb`) maps to physical device **SMI IS917 innostor USB Device** (Serial: `201207220009`, VID: `090C`, PID: `1000`). First connected/migrated: `2020-11-01 17:12:24`. Mounted as `D:` on `2020-09-16` and `2020-11-02`, and later mounted as `E:` on `2020-11-10`.
   - **Drive F:** Volume Label `CRIMSON2` (Volume Serial: `0xca659866`) maps to physical device **Phison USB DISK 2.0** (Serial: `90008B5EB5FFFF64`, VID: `13FE`, PID: `4300`). First connected/migrated: `2020-11-01 17:12:24`. Used extensively for staging exfiltrated data.
   - **Other USB:** Lexar USB Flash Drive (Serial: `AAZ62W7KENRSJLHY`). First connected/migrated: `2020-11-01 17:12:24`.
2. **Memory Analysis**:
   - **Active RDP Remote Control**: At the time of memory capture (`2020-11-16`), there were multiple active/established concurrent RDP connections from external IP addresses:
     - `81.30.144.115` (Established sessions on local port `3389` at `02:34:45` and `02:34:58`)
     - `213.202.233.104` (Established sessions on local port `3389` at `02:34:58` and `02:35:53`)
     - High volume of closed/attempted connections from these IPs and `201.193.188.114` indicates RDP brute-forcing or highly active multi-session control.
   - **Suspicious Process**: `MRC.exe` (PID `29440`) was launched on `2020-11-16 02:31:15` during the active RDP sessions, indicating potential remote control tool or malware execution.
   - **Active Cloud Sync Clients**: `googledrivesyn` (PID 11816/8432), `GoogleDriveFS` (PID 12020/14832), and `OneDrive.exe` (PID 9648/6188) were actively running with established network connections to Google and Microsoft IPs.

- **Confidence Rating:** 5/5 - High confidence. Physical USB device serials, volume labels, and connection timestamps are fully correlated across registry hives, lnk files, and prefetch. Volatile memory state shows active established RDP sessions and running processes at the time of the memory dump.
- **Budget Tally:**
  - Orientation: 5 / 5 tool calls
  - Execution: 24 / 25 tool calls
  - Reporting: 2 / 5 tool calls
- **NPS / Feedback:** 10/10. The DuckDB/Parquet integration made searching complex timelines and memory tables extremely fast and precise.
