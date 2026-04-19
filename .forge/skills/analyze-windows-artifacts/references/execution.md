# Execution Evidence

Determine what programs were executed on the system.

## 1. Prefetch (.pf)
**Location**: `C:\Windows\Prefetch`
**Value**: Confirms execution, last 8 run times, and file/DLL dependencies.

```bash
# Parse all Prefetch files in the container
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/PECmd.dll \
  -d /mnt/windows/Windows/Prefetch \
  --csv /evidence/scratch/ \
  --csvf prefetch_parsed.csv
```

## 2. Shimcache (AppCompatCache)
**Location**: `SYSTEM` hive -> `CurrentControlSet\Control\Session Manager\AppCompatCache`
**Value**: Presence confirms a file *existed* on disk. Win7: chronological by execution. Win8+: unordered.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/AppCompatCacheParser.dll \
  -f /mnt/windows/Windows/System32/config/SYSTEM \
  --csv /evidence/scratch/ \
  --csvf shimcache.csv
```

## 3. Amcache
**Location**: `C:\Windows\appcompat\Programs\Amcache.hve`
**Value**: SHA1 hash of binaries + first execution time. Great for VirusTotal pivots.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/AmcacheParser.dll \
  -f /mnt/windows/Windows/appcompat/Programs/Amcache.hve \
  --csv /evidence/scratch/ \
  --csvf amcache.csv
```

## 4. UserAssist
**Location**: `NTUSER.DAT` -> `Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`
**Value**: GUI execution history (programs launched via Start Menu/Explorer).

```bash
# Use RECmd batch for automated extraction
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/RECmd/RECmd.dll \
  -f /mnt/windows/Users/<USERNAME>/NTUSER.DAT \
  --bn /opt/zimmermantools/RECmd/BatchExamples/Kroll_Batch.reb \
  --csv /evidence/scratch/ \
  --csvf userassist.csv
```

## 5. BAM / DAM
**Location**: `SYSTEM` hive -> `CurrentControlSet\Services\bam\State\UserSettings\<SID>`
**Value**: Last execution time for programs per user.
