---
name: parse-itunes-backup
description: Standard operating procedure for parsing iTunes MobileSync backups (iOS 4 to iOS 10+), extracting basic metadata, decrypting/unpacking backup files using pyiosbackup/iOSbackup in SIFT, and analyzing standard iOS system and application databases (SMS, Call History, WhatsApp, Skype, Apple Notes, Safari, etc.). Use when asked to investigate iTunes backups, extract mobile device data, or decrypt/unpack iOS backup folders.
---

# Parse iTunes Backup

This skill provides a comprehensive workflow to locate, identify, decrypt, unpack, and analyze iTunes MobileSync backups of iOS devices (iPhones, iPads, iPods) from a workstation forensic image.

---

## 1. Locate the Backup on the Workstation

iTunes backups are typically stored in the following default paths on a Windows workstation:
- **Windows Vista/7/8/10/11**: `\Users\<Username>\AppData\Roaming\Apple Computer\MobileSync\Backup\<UDID>\`
- **Windows XP**: `\Documents and Settings\<Username>\Application Data\Apple Computer\MobileSync\Backup\<UDID>\`
- **Microsoft Store iTunes**: `\Users\<Username>\AppData\Local\Packages\AppleInc.iTunes_...\LocalState\Partition\MobileSync\Backup\<UDID>\`

---

## 2. Identify the Backup Format & Version

Check the files in the `<UDID>` backup folder to determine the backup version and format:
- **iOS 4 to iOS 9 (Pre-iOS 10)**: Uses a binary manifest file named `Manifest.mbdb` along with metadata plists: `Manifest.plist`, `Info.plist`, `Status.plist`. Backup files are hashed (SHA-1 of Domain + Path) and stored in the root of the backup folder without extensions.
- **iOS 10+**: Uses a SQLite database named `Manifest.db` instead of `Manifest.mbdb`. Backup files are hashed and stored in subfolders named after the first two characters of the SHA-1 hash (e.g., `0a/0a12345...`).

---

## 3. Extract Basic Device Metadata (Host Side)

Run a python script on the host to parse the `Info.plist` and `Status.plist` files to retrieve device name, serial number, phone number, IMEI, ICCID, product version (iOS version), and last backup timestamp:

```python
import plistlib

with open("path/to/Info.plist", "rb") as f:
    plist = plistlib.load(f)
    print(f"Device Name: {plist.get('Device Name')}")
    print(f"iOS Version: {plist.get('Product Version')}")
    print(f"Serial Number: {plist.get('Serial Number')}")
    print(f"IMEI: {plist.get('IMEI')}")
    print(f"ICCID: {plist.get('ICCID')}")
    print(f"Last Backup Date: {plist.get('Last Backup Date')}")
```

---

## 4. Unpack/Decrypt the Backup (SIFT Container)

Use the specialized `pyiosbackup` utility inside the SIFT container to decrypt and unpack the hashed files into a standard directory layout.

### A. Check Backup Statistics
Verify the backup encryption status, file counts, and installed applications list:
```bash
docker exec <container_id> /opt/ufade/bin/pyiosbackup stats "/mnt/cases/<CASEID>/<IMAGE_NAME>/path/to/Backup/<UDID>/"
```

### B. Unpack the Backup (Unencrypted)
If the backup is not encrypted, unpack all files into a human-readable filesystem layout:
```bash
docker exec <container_id> /opt/ufade/bin/pyiosbackup unback --target /scratch/<IMAGE_NAME>/extracted_comms/unpacked_backup/ "/mnt/cases/<CASEID>/<IMAGE_NAME>/path/to/Backup/<UDID>/" ""
```

### C. Unpack the Backup (Encrypted)
If the backup is encrypted, provide the decryption password as the last argument:
```bash
docker exec <container_id> /opt/ufade/bin/pyiosbackup unback --target /scratch/<IMAGE_NAME>/extracted_comms/unpacked_backup/ "/mnt/cases/<CASEID>/<IMAGE_NAME>/path/to/Backup/<UDID>/" "decryption_password"
```

---

## 5. Analyze Extracted iOS Artifacts

Once unpacked, the files will be structured under their iOS Domain folders (e.g., `HomeDomain`, `WirelessDomain`, `AppDomain-<BundleID>`).

### A. Core iOS System Databases
For a complete listing of key databases, paths, and tables, see the [iOS Backup Artifacts Reference](references/ios_backup_artifacts.md).

### B. Handling iOS Cocoa Timestamps
Many iOS SQLite databases store timestamps in Cocoa/Mac Absolute Time (seconds since January 1, 2001, 00:00:00 UTC). To convert these to UTC in SQL queries:
- **SQL (SQLite)**: `datetime(ZDATE + 978307200, 'unixepoch')`
- **Python**:
  ```python
  import datetime
  cocoa_time = 478714696.76589
  dt = datetime.datetime(2001, 1, 1) + datetime.timedelta(seconds=cocoa_time)
  print(dt.isoformat()) # Outputs: 2016-03-03T16:18:16.765890
  ```

### C. Parsing Binary Plists (.plist / composition)
Many configuration files and application states (such as Twitter/Tweetie drafts) are stored as Binary Plists (`bplist`). Use python's `plistlib` on the host to load and parse them:
```python
import plistlib

with open("path/to/composition.2", "rb") as f:
    plist = plistlib.load(f)
    # Access keys inside the plist
    print(plist)
```
