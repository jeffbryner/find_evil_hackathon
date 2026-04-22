# Persistence Analysis

Identify how the attacker maintains access across reboots.

## 1. Registry Artifacts (Automated)
**Artifacts**: Run Keys, Services, UserAssist, ShimCache.

The `triage_extractor.py` script automatically parses these persistence mechanisms into a unified Parquet timeline (`artifacts_timeline.parquet`).

```bash
# Manual extraction via Plaso inside the container if needed:
docker exec $(cat scratch/container_id.txt) log2timeline.py \
  --artifact_filters 'WindowsRunKeys,WindowsServices,WindowsUserAssist,WindowsAppCompatCache,WindowsEventLogSecurity,WindowsEventLogSystem' \
  --storage_file /scratch/case/evidence/artifacts.plaso \
  /mnt/cases/case/evidence
```

## 2. Manual Registry Inspection
If specific keys are needed beyond the automated triage:

```bash
# Export specific key via regfexport
docker exec $(cat scratch/container_id.txt) regfexport /mnt/cases/case/evidence/Windows/System32/config/SOFTWARE \
  -K "Microsoft\Windows\CurrentVersion\Run"
```

## 3. Scheduled Tasks
**Locations**:
- `C:\Windows\System32\Tasks` (XML files)
- `C:\Windows\Tasks` (.job files)
- Event Log: `Microsoft-Windows-TaskScheduler/Operational`

## 4. WMI Subscriptions
**Location**: `C:\Windows\System32\wbem\Repository`
**Value**: Fileless persistence. Look for `Permanent WMI subscriptions`.

## 5. Startup Folders
**Locations**:
- `C:\ProgramData\Microsoft\Windows\Start Menu\Programs\StartUp`
- `C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup`
