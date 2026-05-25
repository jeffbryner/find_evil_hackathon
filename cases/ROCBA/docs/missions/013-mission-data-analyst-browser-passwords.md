# Mission: Retrieve and Analyze Browser Passwords
**Target Agent:** data-analyst

## Purpose
Retrieve and analyze any stored browser passwords or credential database files (such as Chrome's "Login Data" or other browser credential databases) to see if they contain credentials for compromised accounts or other systems.

## Background
The attacker compromised multiple accounts, including `srl-helpdesk@outlook.com` and `fred.rocba@outlook.com`. We need to determine if any credentials for these or other accounts were stored in the browser databases on Fred's workstation and if we can extract or recover them.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 15 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no Chrome or Edge login credential files or tables are found, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Query the filesystem timeline or parquet tables for the presence of browser credential files (e.g., `Login Data` for Chrome or Edge).
- [x] Check if there are any extracted or decoded credentials, or if we can run queries on any decrypted/extracted credential tables.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  - Analyzed the schema of ROCBA parquet tables and queried `fs_timeline` for Chrome or Edge `Login Data` files. Identified multiple Chrome/Edge database files across multiple profiles.
  - Used Dissect's `browser.passwords` plugin against the `rocba-cdrive.e01` disk image to recover browser credentials.
  - Dissect failed to decrypt DPAPI-protected Chrome/Edge credentials due to lack of master key decryption.
  - Successfully recovered completely plaintext Firefox credentials from `logins.json` and `logins-backup.json`.
  - Queried LSA Secrets using Dissect's `lsa.secrets` plugin, recovering VPN/RAS dial parameters which contained Stark Research Labs Active Directory domain credentials.
- **Findings:**
  - Decrypted Firefox stored passwords:
    - `fred.rocba@outlook.com` -> `C0bracommand` (at `https://login.live.com`)
    - `redguard.cobra@gmail.com` -> `C0bracommand` (at `https://accounts.google.com`)
    - `fred.rocba@gmail.com` -> `C0bracommand` / `c0bracommand` (at `https://accounts.google.com`, `https://www.amazon.com`, `https://www.netflix.com`)
    - `3392233317` -> `C0bracommand` (at `https://www.facebook.com`)
  - Decrypted LSA VPN secrets:
    - `SHIELDBASE\frocba` -> `Big-Purple-Truck` (Stark Research Labs Active Directory/Office365 domain credentials)
- **Confidence Rating:** 5/5 (High confidence, verified by exact decryption signatures and matches).
- **Budget Tally:**
  - Orientation Budget: 5/5
  - Execution Budget: 15/15
  - Reporting Budget: 1/5
- **NPS / Feedback:** 10/10. The combination of high-speed timeline querying with targeted Dissect plugin extraction is extremely powerful.
