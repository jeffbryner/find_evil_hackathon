# Execution Evidence

Determine what programs were executed on the system.

## 1. Prefetch (.pf)
**Location**: `C:\Windows\Prefetch`
**Value**: Confirms execution, last 8 run times, and file/DLL dependencies.


## 2. Shimcache (AppCompatCache)
**Location**: `SYSTEM` hive -> `CurrentControlSet\Control\Session Manager\AppCompatCache`
**Value**: Presence confirms a file *existed* on disk. Win7: chronological by execution. Win8+: unordered.


## 3. Amcache
**Location**: `C:\Windows\appcompat\Programs\Amcache.hve`
**Value**: SHA1 hash of binaries + first execution time. Great for VirusTotal pivots.


## 4. UserAssist
**Location**: `NTUSER.DAT` -> `Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist`
**Value**: GUI execution history (programs launched via Start Menu/Explorer).


## 5. BAM / DAM
**Location**: `SYSTEM` hive -> `CurrentControlSet\Services\bam\State\UserSettings\<SID>`
**Value**: Last execution time for programs per user.


TODO: References for how to run utilities in the SIFT container