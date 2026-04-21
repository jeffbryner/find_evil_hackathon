# Event Log Analysis

Reconstruct a timeline of system and user events.

## 1. Parsing with Plaso (Automated)
**Location**: `C:\Windows\System32\winevt\Logs`

The `triage_extractor.py` script automatically parses `Security.evtx` and `System.evtx` into a unified Parquet timeline.

```bash
# Manual extraction via Plaso inside the container if needed:
docker exec $(cat scratch/container_id.txt) log2timeline.py \
  --parsers winevtx \
  --storage_file /scratch/case/evidence/event_logs.plaso \
  /mnt/cases/case/evidence/Windows/System32/winevt/Logs/
```

## 2. Critical Event IDs

### Authentication (Security.evtx)
- **4624**: Successful Logon (LogonType 10 = RDP, 3 = Network).
- **4625**: Failed Logon.
- **4648**: Logon using explicit credentials (runas).
- **4672**: Special privileges assigned (Admin logon).

### Execution & Persistence (Security.evtx)
- **4688**: Process Creation (requires Audit Process Creation policy).
- **4698**: Scheduled Task Created.

### PowerShell (Microsoft-Windows-PowerShell/Operational.evtx)
- **4104**: Script Block Logging (Contains the **full script content**).

### Services (System.evtx)
- **7045**: New Service Installed.

### RDP (TerminalServices-RemoteConnectionManager/Operational.evtx)
- **1149**: RDP Authentication Success (Contains source IP).

## 3. Analysis Strategy
- **Pivot on Time**: Filter logs around the time of a suspicious file creation.
- **Pivot on Account**: Look for all logons from a specific user.
- **Pivot on IP**: Look for all connections from a suspicious source IP.
