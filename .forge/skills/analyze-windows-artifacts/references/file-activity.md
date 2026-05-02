# File & Folder Activity

Track file system changes and user browsing history.

## 1. MFT ($MFT)
**Location**: `C:\$MFT`
**Value**: The master index of the NTFS file system.


## 2. $UsnJrnl (Change Journal)
**Location**: `$UsnJrnl:$J` (extracted from inode 11)
**Value**: Records file creations, deletions, and renames. Survives file deletion.


## 3. Shellbags
**Locations**: `NTUSER.DAT` and `UsrClass.dat`
**Value**: Records folder browsing history (local, network, removable media). Persists even after the folder is gone.


## 4. LNK Files (.lnk)
**Location**: `C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Recent`
**Value**: Reveals target file paths, MAC times, and volume serial numbers.


## 5. Jump Lists
**Location**: `C:\Users\<USER>\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations`
**Value**: Shows pinned and frequent files per application.


TODO: References for how to run utilities in the SIFT container