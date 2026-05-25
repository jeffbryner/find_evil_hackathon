# Dissect Plugins

A full list of available plugin modules for `target-query`. You can also list these dynamically using `uv run target-query -l`.

## Browser
- `browser.history`: History for chromium, edge, iexplore, firefox, brave, chrome, safari.
- `browser.cookies`: Cookies for chromium, edge, firefox, brave, chrome.
- `browser.downloads`: Downloads for chromium, edge, iexplore, firefox, brave, chrome.
- `browser.extensions`: Extensions for chromium, edge, firefox, brave, chrome.
- `browser.passwords`: Passwords recovered from browser storage.

## Windows Specific
- `amcache.applications`: InventoryApplication records from Amcache hive.
- `bam`: Parse bam and dam registry keys (Evidence of execution).
- `evtx`: Return entries from Windows Event log files (*.evtx).
- `lnk`: Parse all .lnk files in /ProgramData, /Users, and /Windows.
- `prefetch`: Return the content of all prefetch files.
- `runkeys`: Iterate various run key locations.
- `shimcache`: Return the shimcache.
- `userassist`: Return the UserAssist information for each user.
- `usb`: Information about historically attached USB storage devices.
- `services`: Information about all installed Windows services.
- `tasks`: All scheduled tasks on a Windows system.
- `lsa.secrets`: Yield decrypted LSA secrets from a Windows target. (output: records)
- `sam`: Dump SAM entries (output: records)
- `dpapi.keyprovider.credhist.keys`: Yield Windows CREDHIST SHA1 hashes. (output: lines)
- `dpapi.keyprovider.defaultpassword.lsa.keys`: Yield Windows LSA DefaultPassword strings. (output: lines)
- `dpapi.keyprovider.defaultpassword.winlogon.keys`: Yield Windows Winlogon DefaultPassword strings. (output: lines)
- `dpapi.keyprovider.keychain.keys`: Yield keychain passphrases. (output: lines)
- `dpapi.keyprovider.keys`: Return keys for: dpapi.keyprovider.empty, dpapi.keyprovider.keychain, dpapi.keyprovider.credhist, dpapi.keyprovider.defaultpassword.lsa, dpapi.keyprovider.defaultpassword.winlogon (output: lines)


## Linux/Unix Specific
- `bashhistory`: Return shell history for all UNIX users.
- `cronjobs`: Yield cronjobs and their configured environment variables.
- `journal`: Return the contents of Systemd Journal log files.
- `processes`: Return the processes available in /proc.
- `services`: Information about all installed systemd and init.d services.

## Application Specific
- `msoffice.startup`: Startup items found in Microsoft Office startup folders.
- `anydesk.logs`: Parse AnyDesk trace files.
- `teamviewer.logs`: Yield TeamViewer client logs.
- `powershell_history`: Return PowerShell command history for all users.

## Filesystem
- `mft.records`: Return the MFT records of all NTFS filesystems.
- `usnjrnl`: Return the UsnJrnl entries of all NTFS filesystems.
- `walkfs`: Walk a target's filesystem and return all filesystem entries.
- `yara`: Scan files inside the target with YARA rules.

---
*Note: This is a curated list. Use `uv run target-query -l` for the exhaustive list.*
