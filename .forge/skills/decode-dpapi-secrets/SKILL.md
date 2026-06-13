---
name: decode-dpapi-secrets
description: Decrypt Windows DPAPI (Data Protection API) secrets and browser credentials using pypykatz. Use this skill when you need to recover DPAPI master keys, decrypt Chrome/Edge Login Data databases, or extract plaintext credentials from Windows registry hives.
---

# DPAPI Decryption & Credential Recovery SOP

This skill provides a Standard Operating Procedure (SOP) for decrypting Windows DPAPI (Data Protection API) secrets, browser credentials, and registry hives using `pypykatz` within the local python/uv environment.

## Trigger
Use this skill when you identify DPAPI-protected databases (such as Google Chrome or Microsoft Edge `Login Data`), or when you need to dump SAM hashes, LSA secrets, or DPAPI master keys from an extracted Windows system.

## Core Concepts & Key Paths

To decrypt a DPAPI-protected file (such as Chrome/Edge passwords), you must reconstruct the cryptographic chain:

| Artifact | Default Windows Path | Purpose |
| --- | --- | --- |
| **Registry Hives** | `C:\Windows\System32\config\` (SAM, SYSTEM, SECURITY) | Contains user NT hashes and system LSA secrets (including DPAPI backup keys). |
| **DPAPI Master Keys** | `C:\Users\<username>\AppData\Roaming\Microsoft\Protect\<User_SID>\` | Contains the user-specific encrypted master keys. |
| **Chrome/Edge Login Data** | `C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default\Login Data` | Contains the SQLite database with DPAPI-encrypted passwords. |

---

## Execution Steps & Command Recipes

### Step 1: Extract Registry Hashes and LSA Secrets
Before decrypting master keys, you must extract the user's NT hash or the system's DPAPI backup keys. Extract the registry hives (`SYSTEM`, `SAM`, `SECURITY`) from the disk image and run:

```bash
# Dump SAM hashes (contains user NT hashes)
uv run pypykatz registry sam /path/to/extracted/SYSTEM /path/to/extracted/SAM --json /path/to/sam_output.json

# Dump LSA secrets (contains DPAPI Backup Keys)
uv run pypykatz registry lsa /path/to/extracted/SYSTEM /path/to/extracted/SECURITY --json /path/to/lsa_output.json
```

### Step 2: Decrypt the DPAPI Master Key
DPAPI-encrypted files reference a specific **Master Key GUID**. Locate the corresponding encrypted master key file in the user's `Protect` folder and decrypt it using the user's SID and their NT hash (or plaintext password):

```bash
# Decrypt the master key using the user's NT hash
uv run pypykatz dpapi masterkey /path/to/Protect/<User_SID>/<MasterKey_GUID> \
    --sid <User_SID> \
    --nthash <User_NT_Hash> \
    --outkey /path/to/decrypted_masterkey.key
```

### Step 3: Decrypt Chrome/Edge Stored Passwords
Once you have the decrypted master key, use `pypykatz` to decrypt the Chrome/Edge `Login Data` SQLite database:

```bash
# Decrypt Chrome/Edge Login Data and output to a JSON file
uv run pypykatz dpapi chrome /path/to/Login_Data \
    --masterkey /path/to/decrypted_masterkey.key \
    --json /path/to/decrypted_passwords.json
```

---

## High-Speed Querying via DuckDB

Because `pypykatz` outputs structured JSON files, you do not need a custom conversion script. DuckDB can natively query, filter, and convert standard JSON files directly.

### 1. Query Plaintext Passwords Directly
You can run SQL queries directly against the decrypted JSON file:
```sql
SELECT * FROM read_json_auto('/path/to/decrypted_passwords.json');
```

### 2. Convert Decrypted Passwords to Parquet
To save the decrypted credentials to a high-speed Parquet file for joining with other timelines:
```sql
COPY (SELECT * FROM read_json_auto('/path/to/decrypted_passwords.json')) 
TO 'cases/<case_name>/scratch/parquet/decrypted_browser_passwords.parquet' 
(FORMAT 'parquet');
```

---

## Reporting & IOC Logging

1.  **Analyze Findings:** Inspect the decrypted credentials for password reuse, unauthorized accounts, or corporate VPN passwords.
2.  **Log IOCs:** For any identified malicious accounts or credentials, you **MUST** immediately register them as Indicators of Compromise (IOCs) using `ioc_tracker.py` before completing your turn.
    ```bash
    uv run helpers/ioc_tracker.py --case <case_name> --add credential --value "<username>:<password>" --source decode-dpapi-secrets
    ```
3.  **Report:** Return a structured summary of the decrypted accounts, including URLs, usernames, plaintext passwords, and their implications for the case.
