# System Usage & Exfiltration

Track data volumes, browser activity, and deleted files.

## 1. SRUM (System Resource Usage Monitor)
**Location**: `C:\Windows\System32\sru\SRUDB.dat`
**Value**: Records per-application network bytes sent/received and CPU usage. Confirms data exfiltration volumes.

## 2. Browser Artifacts
**Locations**:
- Chrome/Edge: `AppData\Local\Google\Chrome\User Data\Default\History`
- Firefox: `AppData\Roaming\Mozilla\Firefox\Profiles\<ID>\places.sqlite`


## 3. Recycle Bin
**Location**: `C:\$Recycle.Bin\<SID>`
**Value**: $I files contain metadata (original path, deletion time). $R files contain content.

TODO: Reference for how to run utilities in the SIFT container
