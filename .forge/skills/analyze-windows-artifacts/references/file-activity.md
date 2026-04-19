# File & Folder Activity

Track file system changes and user browsing history.

## 1. MFT ($MFT)
**Location**: `C:\$MFT`
**Value**: The master index of the NTFS file system.

```bash
# Parse MFT for timeline analysis
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/MFTECmd.dll \
  -f /mnt/windows/\$MFT \
  --csv /evidence/scratch/ \
  --csvf mft_parsed.csv
```

## 2. $UsnJrnl (Change Journal)
**Location**: `$UsnJrnl:$J` (extracted from inode 11)
**Value**: Records file creations, deletions, and renames. Survives file deletion.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/MFTECmd.dll \
  -f /mnt/windows/\$J \
  --csv /evidence/scratch/ \
  --csvf usnjrnl_parsed.csv
```

## 3. Shellbags
**Locations**: `NTUSER.DAT` and `UsrClass.dat`
**Value**: Records folder browsing history (local, network, removable media). Persists even after the folder is gone.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/SBECmd.dll \
  -d /mnt/windows/Users/<USERNAME>/ \
  --csv /evidence/scratch/
```

## 4. LNK Files (.lnk)
**Location**: `C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Recent`
**Value**: Reveals target file paths, MAC times, and volume serial numbers.

```bash
docker exec $(cat scratch/container_id.txt) dotnet /opt/zimmermantools/LECmd.dll \
  -d /mnt/windows/Users/<USER>/AppData/Roaming/Microsoft/Windows/Recent \
  --csv /evidence/scratch/
```

## 5. Jump Lists
**Location**: `C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations`
**Value**: Shows pinned and frequent files per application.
