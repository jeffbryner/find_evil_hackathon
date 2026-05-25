# Mission: DPAPI Decryption and SAM/Chrome Credential Recovery
**Target Agent:** sniper-forensics

## Purpose
Attempt to decrypt DPAPI-protected files (such as Google Chrome/Microsoft Edge Login Data) and extract additional user credentials for Fred Rocba or other accounts from SAM/LSA registry hives using the new `decode-dpapi-secrets` skill and `pypykatz`.

## Background
We recently established that Fred Rocba used the password `C0bracommand` across several accounts. However, we have not yet decrypted the Chrome/Edge browser passwords because they are DPAPI-protected. By using `pypykatz` and the new DPAPI decryption SOP, we want to see if we can recover any other credentials or secrets from Fred's Chrome/Edge logins, SAM, or other likely areas.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 25 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If the registry hives (SAM, SYSTEM, SECURITY) or Chrome/Edge `Login Data` databases cannot be found or are unreadable, stop and report immediately.

## Task Checklist
- [ ] Read the `shared-facts-sop`, `delegating-mission-cards-sop`, and the new `decode-dpapi-secrets` skill.
- [ ] Extract or locate the Windows registry hives (SAM, SYSTEM, SECURITY) and DPAPI master keys for Fred's profile.
- [ ] Dump the SAM registry hive using `pypykatz` to verify user hashes.
- [ ] Locate the Chrome/Edge `Login Data` database and any master keys in Fred's profile.
- [ ] Use `pypykatz` to decrypt the DPAPI master keys using Fred's NT hash or SID, and then decrypt the Chrome/Edge passwords database.
- [ ] Save the decrypted passwords as a JSON file, and query/analyze them using DuckDB.
- [ ] Update this mission card with results, including an updated "Results & Post-Mortem" section.

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:**
- **Findings:**
- **Confidence Rating:**
- **Budget Tally:**
- **NPS / Feedback:**
