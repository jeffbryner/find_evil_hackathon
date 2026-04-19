# Persistence Analysis

Identify how the attacker maintains access across reboots.

## 1. Registry Run Keys
**Locations**:
- `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run`
- `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`

```bash
# Check Software Hive
docker exec $(cat scratch/container_id.txt) regfexport /mnt/windows/Windows/System32/config/SOFTWARE \
  -K "Microsoft\Windows\CurrentVersion\Run"
```

## 2. Windows Services
**Location**: `SYSTEM` hive -> `CurrentControlSet\Services`
**Value**: Look for unsigned drivers or services with suspicious image paths (e.g., `%TEMP%`).

```bash
# Export services for analysis
docker exec $(cat scratch/container_id.txt) regfexport /mnt/windows/Windows/System32/config/SYSTEM \
  -K "ControlSet001\Services"
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
