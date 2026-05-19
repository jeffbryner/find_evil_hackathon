---
name: extract-triage-artifacts
description: Extract forensic artifacts from disk images using the Dissect framework (target-query, target-reg). Use this skill when you need to quickly retrieve system info, registry keys, browser history, or other OS artifacts and optionally convert them to Parquet format for SQL analysis.
---

# Extract Triage Artifacts

The Dissect framework provides a set of utilities (`target-*`) to quickly retrieve and analyze artifacts from forensic disk images (not for memory images).

## Core Utilities

### 1. target-info
Get general information about an image (hostname, OS version, IPs, timezone).
```shell
uv run target-info -q <forensic_disk_image_filename>
```

### 2. target-query
Query specific operating system artifacts using plugins.
```shell
uv run target-query <forensic_disk_image_filename> -f <plugin> -qs
```
- `-q`: Quiet extraneous stdout.
- `-s`: Force string/ascii only output.
- For a full list of available plugins, see [plugins.md](references/plugins.md).

### 3. target-reg
Query registry hives or keys directly.
```shell
uv run target-reg <forensic_disk_image_filename> -k "HKEY_LOCAL_MACHINE\\Software\\..." -d 2 -q
```
- `-k`: Registry key name (escape backslashes).
- `-d`: Depth level of traversal.

## Exporting to Parquet

To enable high-speed SQL analysis via DuckDB, use the `rdump_to_parquet.py` helper.

### Usage
```shell
uv run target-query <path/to/drive_image> -f <target.module> | uv run helpers/rdump_to_parquet.py <output.parquet>
```

### Example: Browser History
```shell
uv run target-query cases/<CASEID>/images/<DRIVE_IMAGE> -f browser.history | uv run helpers/rdump_to_parquet.py cases/<CASEID>/scratch/DRIVE_IMAGE/parquet/browser_history.parquet
```

## Filtering and Formatting with rdump
Use `rdump` to process, filter, and format results.
- **Select fields**: `uv run target-query host.img -f users | uv run rdump -F name,home`
- **JSONL output**: `uv run target-query host.img -f users | uv run rdump -J`
- **Filter records**: `uv run target-query host.img -f users | uv run rdump -s "r.domain is not None"`
