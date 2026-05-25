---
name: hunt-usb-activity-sop
description: Standard Operating Procedure for investigating USB device connections, mapping drive letters to hardware serial numbers, and establishing exfiltration timelines using DuckDB/Parquet. Use this skill when asked to identify external media, find USB serial numbers, or determine when a USB device was connected/disconnected.
---

# Hunt USB Activity SOP

This skill provides a structured workflow for identifying USB devices and their activity windows by correlating multiple forensic artifacts.

## Workflow

### 1. Identify Drive Letter & Initial Indicators
Search for LNK files or jump lists that point to non-system drive letters (e.g., D:, E:, F:, G:). These often indicate the drive letter assigned to an external, virtual, or redirected device.

- **Artifacts**: `fs_timeline.parquet`, `artifacts_timeline.parquet` (windows:lnk, windows:jump_list)
- **Key Indicators**: File names like `Homework (E).lnk` or paths starting with `E:\`.

### 2. Differentiate Drive Types (Physical vs. Redirected vs. Cloud)
Before hunting for physical hardware insertion registry keys (like `USBSTOR`), determine if the drive letter represents a physical USB, an RDP-redirected drive, or a cloud drive mount.

- **Physical USB Drive**:
  - **Drive Type**: `2` (`DRIVE_REMOVABLE`)
  - **Indicators**: Unique hardware serial number in ShellBags/registry, entries in `USBSTOR`.
- **RDP-Redirected Client Drive (TSClient)**:
  - **Drive Type**: `4` (`DRIVE_REMOTE` / network redirect)
  - **Indicators**: Paths starting with `\\tsclient\<drive_letter>`, drive serial number is `0x00000000`, volume label is empty.
- **Cloud/Virtual Drive (e.g., Google Drive)**:
  - **Drive Type**: `3` (`DRIVE_FIXED`)
  - **Indicators**: Specific volume label (e.g., `Google Drive File Stream`) and unique volume serial numbers (e.g., `0x19831116`).

### 3. Map Drive Letter to Serial Number (ShellBags)
Use Windows ShellBags to find the unique hardware identifier, network path, or virtual volume details associated with the drive letter.

- **Artifacts**: `artifacts_timeline.parquet` (windows:shell_items)
- **Method**: Search for shell items matching the drive letter (e.g., `[My Computer]\E:\`). The `details` field often contains the hardware serial number, UNC connection path, or vendor name.

### 4. Identify Vendor & Product Details
Search for the serial number across all artifacts to find registry keys or event logs that provide more context.

- **Artifacts**: `artifacts_timeline.parquet`
- **Key Locations**: 
    - `USBSTOR` registry keys
    - `Windows Portable Devices`
    - `MountedDevices`
- **Goal**: Confirm the manufacturer (e.g., Lexar, SanDisk, Innostor) and product ID.

### 5. Establish Connection/Disconnection Timeline
Determine the "window of presence" for the device.

- **Connection Time**: Look for the earliest timestamp of the drive letter access in ShellBags or the creation of LNK files pointing to that drive.
- **Disconnection Time**: Look for the deletion of LNK files, "Device Removed" events in EVTX (if available), or the last modified time of the drive's root ShellBag.

## SQL Recipes
See [references/sql-recipes.md](references/sql-recipes.md) for specific DuckDB queries to execute this workflow.
