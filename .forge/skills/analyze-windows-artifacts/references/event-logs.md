# Event Log Analysis

Reconstruct a timeline of system and user events.

## 1. Parsing with EvtxECmd
**Location**: `C:\Windows\System32\winevt\Logs`

```bash
# Parse all logs in the container
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/EvtxeCmd/EvtxECmd.dll \
  -d /mnt/windows/Windows/System32/winevt/Logs \
  --csv /evidence/scratch/ \
  --maps /opt/zimmermantools/EvtxeCmd/Maps/
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
