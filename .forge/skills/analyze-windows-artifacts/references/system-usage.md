# System Usage & Exfiltration

Track data volumes, browser activity, and deleted files.

## 1. SRUM (System Resource Usage Monitor)
**Location**: `C:\Windows\System32\sru\SRUDB.dat`
**Value**: Records per-application network bytes sent/received and CPU usage. Confirms data exfiltration volumes.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/SrumECmd.dll \
  -f /mnt/windows/Windows/System32/sru/SRUDB.dat \
  --csv /evidence/scratch/
```

## 2. Browser Artifacts
**Locations**:
- Chrome/Edge: `AppData\Local\Google\Chrome\User Data\Default\History`
- Firefox: `AppData\Roaming\Mozilla\Firefox\Profiles\<ID>\places.sqlite`

```bash
# Parse SQLite databases
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/SQLECmd/SQLECmd.dll \
  -d /mnt/windows/Users/<USER>/AppData/Local/Google/Chrome/User Data/Default/ \
  --csv /evidence/scratch/
```

## 3. Recycle Bin
**Location**: `C:\$Recycle.Bin\<SID>`
**Value**: $I files contain metadata (original path, deletion time). $R files contain content.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/RBCmd.dll \
  -d /mnt/windows/\$Recycle.Bin \
  --csv /evidence/scratch/
```
