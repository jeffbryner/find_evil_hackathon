---
name: extract-triage-artifacts
description: Extract forensic artifacts from disk images using the Dissect framework (target-query, target-reg). Use this skill when you need to quickly retrieve basic system information, registry keys, browser history, browser passwords, or other targeted OS artifacts and optionally convert them to Parquet format for SQL analysis.
---

# Extract Triage Artifacts

The Dissect framework provides a set of utilities (`target-*`) to quickly retrieve and analyze artifacts from forensic disk images (not for memory images).

## Core Utilities

### 1. target-info
Get general information about an image (hostname, OS version, IPs, timezone).
```shell
uv run target-info -q cases/<CASEID>/images/<DRIVE_IMAGE_FILENAME>
```
Sample output:
```<Target cases/<CASEID>/images/<DRIVE_IMAGE_FILENAME>>

Disks
- <Disk type='ewf' size=1234567890>

Volumes
- <Volume name='Basic data partition' size=377486848 fs='ntfs'>
- <Volume name='EFI system partition' size=209714688 fs='fat'>
- <Volume name='Microsoft reserved partition' size=134217216 fs=None>
- <Volume name='Basic data partition' size=118212263424 fs='ntfs'>
- <Volume name='part_1bb1100000' size=471858688 fs='ntfs'>
- <Volume name='Basic data partition' size=5662309888 fs='ntfs'>

Mounts
- <Mount fs='ntfs' path='sysvol'>
- <Mount fs='fat' path='efi'>
- <Mount fs='ntfs' path='c:'>
- <Mount fs='ntfs' path='/$fs$/fs0'>
- <Mount fs='ntfs' path='/$fs$/fs1'>
- <Mount fs='ntfs' path='/$fs$/fs2'>

Hostname       : ANAME
Domain         : None
Ips            : 192.168.0.103, 192.168.0.141
Os family      : windows
Os version     : Windows 10 Pro (NT 10.0) 10586.420
Architecture   : amd64-win64
Language       : en_US
Timezone       : America/New_York
Install date   : 2016-03-15T11:04:06.000000+00:00
Last activity  : 2016-11-04T14:45:48.456490+00:00
```

### 2. target-query
Query specific operating system artifacts using plugins.
```shell
uv run target-query <forensic_disk_image_filename> -f <plugin> -qs
```
- `-q`: Quiet extraneous stdout.
- `-s`: Force string/ascii only output.
- For a full list of available plugins, see [plugins.md](references/plugins.md).

**Agent Best Practice:** Always pipe `target-query` outputs to `rdump -J` (for JSONL) or use the `-s` (string-only) flag. Dumping raw record streams directly to the terminal outputs binary control characters, which can pollute your context window and degrade reasoning performance.

### 3. target-reg
Query registry hives or keys directly.
```shell
uv run target-reg cases/<CASEID>/images/<DRIVE_IMAGE_FILENAME> -k "HKEY_LOCAL_MACHINE\\Software\\" -d 1 -q
```
- `-k`: Registry key name (escape backslashes).
- `-d`: Depth level of traversal.

## 4. Filtering and Formatting with rdump
Use `rdump` to process, filter, and format results.
- **Select fields**: `uv run target-query host.img -f users | uv run rdump -F name,home`
- **JSONL output**: `uv run target-query host.img -f users | uv run rdump -J`
- **Filter records**: `uv run target-query host.img -f users | uv run rdump -s "r.domain is not None"`

## Exporting to Parquet

To save data for high-speed SQL analysis via DuckDB, use the `rdump_to_parquet.py` helper.

### Usage
```shell
uv run target-query <path/to/drive_image> -f <target.module> | uv run helpers/rdump_to_parquet.py <output.parquet>
```

### Example: Browser History
```shell
uv run target-query cases/<CASEID>/images/<DRIVE_IMAGE_FILENAME> -f browser.history | uv run helpers/rdump_to_parquet.py cases/<CASEID>/scratch/<DRIVE_IMAGE_FILENAME>/parquet/browser_history.parquet
```
Note that by convention we store Parquet files in a `parquet/` subdirectory under the image's scratch directory.

### End-to-End Pipeline Quick-Reference
Use this table to map common forensic objectives to Dissect target-query modules, their corresponding Parquet outputs, and the standard SQL queries to analyze them:

| Forensic Objective | Dissect Plugin | Target Parquet File | Recommended Query |
| --- | --- | --- | --- |
| **Browser History** | `browser.history` | `browser_history.parquet` | `SELECT url, title, visit_count FROM browser_history ORDER BY visit_count DESC;` |
| **User Accounts** | `users` | `users.parquet` | `SELECT name, sid, home, shell FROM users;` |
| **Installed Apps** | `apps` | `installed_apps.parquet` | `SELECT name, version, install_date FROM installed_apps;` |
| **LSA Secrets** | `lsa.secrets` | `lsa_secrets.parquet` | `SELECT name, secret_type, value FROM lsa_secrets;` |
| **Browser Logins** | `browser.passwords` | `browser_passwords.parquet` | `SELECT url, username, password FROM browser_passwords;` |
| **Run Keys** | `registry.run` | `run_keys.parquet` | `SELECT key_path, name, value FROM run_keys;` |


## Document new data
If you create new parquet data files, be sure to update the shared facts case documentation data inventory with the new file paths and descriptions. This ensures that all team members have access to the latest extracted artifacts for analysis.



