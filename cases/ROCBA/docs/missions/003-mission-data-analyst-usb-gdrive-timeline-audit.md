# Forensic Audit Trail: Deep-Dive USB and Google Drive Timeline

## 1. Initial Prompt & Parameters
- **Target Agent:** data-analyst
- **Initial Instructions:** Deep-dive the USB drives and Google Drive File Stream configurations and timelines in the ROCBA case.
  1. Identify all USB drives connected, their vendor, product, hardware serial numbers, volume labels, and drive letters.
  2. Determine the exact connection/disconnection timeline for USB drive CRIMSON2 (F:) on Nov 13, 2020.
  3. Identify Google Drive File Stream (G:) volume serial number, volume label, installation/configuration time, and active periods.
  4. Search for associated Google accounts, email addresses, or configurations.
  5. Correlate all these activities with the RDP session timelines.
- **Budgets:**
  - Orientation Budget: 5 tool calls
  - Execution Budget: 15 tool calls
  - Reporting Budget: 5 tool calls
  - Proactive Self-Termination: At tool call 20, cease active forensics and write out findings.

## 2. Chronological Tool Execution Log
- **Tool Call #1:** `read` on `/Users/jeffbryner/development/find_evil_hackathon/cases/ROCBA/docs/missions/003-mission-data-analyst-usb-gdrive-timeline.md` -> *Outcome: Read the mission card parameters and rules.*
- **Tool Call #2:** `skill` on `hunt-usb-activity-sop` -> *Outcome: Loaded the USB exfiltration hunting standard operating procedure.*
- **Tool Call #3:** `read` on `/Users/jeffbryner/development/find_evil_hackathon/.forge/skills/hunt-usb-activity-sop/references/sql-recipes.md` -> *Outcome: Read SQL query recipes for USBSTOR, MountedDevices, and LNK/shell item correlation.*
- **Tool Call #4:** `skill` on `shared-facts-sop` -> *Outcome: Loaded standard operating procedure for updating the shared facts file.*
- **Tool Call #5:** `skill` on `delegating-mission-cards-sop` -> *Outcome: Loaded standard operating procedure for updating mission cards and audit logs.*
- **Tool Call #6:** `read` on `/Users/jeffbryner/development/find_evil_hackathon/cases/ROCBA/docs/shared_facts.md` -> *Outcome: Ingested current case knowledge base and staging folder details.*
- **Tool Call #7:** `shell` with command `uv run helpers/query_parquet.py --help` -> *Outcome: Checked the parameters and help output of the query utility.*
- **Tool Call #8:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --schema` -> *Outcome: Inspected the schema of available Parquet tables (`artifacts_timeline`, `fs_timeline`, `browser_history`, `memory_*`).*
- **Tool Call #9:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT DISTINCT data_type FROM artifacts_timeline WHERE message ILIKE '%USBSTOR%' OR details ILIKE '%USBSTOR%'"` -> *Outcome: Identified relevant USBSTOR data types in `artifacts_timeline` (including `windows:registry:usbstor:instance` and `setupapi:log:line`).*
- **Tool Call #10:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE data_type = 'windows:registry:usbstor:instance' LIMIT 10"` -> *Outcome: Extracted USBSTOR instances containing vendor names, product IDs, and hardware serial numbers (e.g. `AAZ62W7KENRSJLHY` for Lexar, `201207220009` for Innostor).*
- **Tool Call #11:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE message ILIKE '%MountedDevices%' LIMIT 100"` -> *Outcome: Retrieved the `MountedDevices` registry key modification timestamp and drive mappings (\DosDevices\C: through H:).*
- **Tool Call #12:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE message ILIKE '%DosDevices%' OR details ILIKE '%DosDevices%'"` -> *Outcome: Discovered `googledrivefs3229` System EVTX logs recording the mount, link creation, and link deletion times of the virtual `G:` drive (Google Drive File Stream).*
- **Tool Call #13:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE data_type ILIKE 'windows:shell_item%' AND (message ILIKE '%G:\%' OR message ILIKE '%F:\%' OR message ILIKE '%E:\%' OR message ILIKE '%D:\%' OR message ILIKE '%H:\%') LIMIT 100"` -> *Outcome: Analyzed shell items pointing to files and directories on non-system drives.*
- **Tool Call #14:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE data_type ILIKE 'windows:shell_item%' AND (message ILIKE '%F:\%' OR details ILIKE '%F:\%') LIMIT 50"` -> *Outcome: Verified file access paths on the exfiltration staging drive `F:\`.*
- **Tool Call #15:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE message ILIKE '%.lnk%' AND (message ILIKE '%F:\%' OR details ILIKE '%F:\%') LIMIT 5"` -> *Outcome: Identified shell items and LNK references pointing to exfiltrated files on the `F:\` drive.*
- **Tool Call #16:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT DISTINCT data_type FROM artifacts_timeline WHERE data_type ILIKE '%lnk%'"` -> *Outcome: Confirmed that `windows:lnk:link` is the correct data type for parsed LNK files.*
- **Tool Call #17:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message, details FROM artifacts_timeline WHERE data_type = 'windows:lnk:link' AND (message ILIKE '%F:\%' OR details ILIKE '%F:\%' OR message ILIKE '%G:\%' OR details ILIKE '%G:\%') LIMIT 10"` -> *Outcome: Extracted volume serial numbers, volume labels, and drive types from LNK metadata for both `F:` (CRIMSON2, serial `0xCA659866`) and `G:` (Google Drive File Stream, serial `0x19831116`).*
- **Tool Call #18:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT DISTINCT details::JSON->>'volume_label' as volume_label, details::JSON->>'drive_serial_number' as serial, details::JSON->>'drive_type' as drive_type FROM artifacts_timeline WHERE data_type = 'windows:lnk:link'"` -> *Outcome: Extracted all unique connected volume labels and volume serial numbers from LNK artifacts.*
- **Tool Call #19:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT DISTINCT details::JSON->>'volume_label' as volume_label, details::JSON->>'drive_serial_number' as serial, details::JSON->>'drive_type' as drive_type, regexp_extract(message, 'Local path: ([A-Z]:)', 1) as drive_letter FROM artifacts_timeline WHERE data_type = 'windows:lnk:link'"` -> *Outcome: Successfully mapped volume labels, serial numbers, and drive types to their assigned drive letters (C:, D:, E:, F:, G:).*
- **Tool Call #20:** `shell` with command `uv run helpers/query_parquet.py --case ROCBA --query "SELECT timestamp, message FROM artifacts_timeline WHERE message ILIKE '%AAZ62W7KENRSJLHY%' OR message ILIKE '%201207220009%' OR message ILIKE '%90008B5EA6FFFF27%' OR message ILIKE '%90008B5EB5FFFF64%' OR message ILIKE '%040419-37110%' OR message ILIKE '%102016-51572%' OR message ILIKE '%121118-1061200001494%' LIMIT 100"` -> *Outcome: Located registry setup, migration, and PnP references mapping hardware serial numbers to system device nodes.*

## 3. Self-Audit Verification
- The total count of logged active forensic tool calls is exactly 20.
- All executed SQL queries are recorded in their entirety.
- The final reporting file writes and patches are excluded from the budget tally as per the Recursive Audit Exclusion Rule.
