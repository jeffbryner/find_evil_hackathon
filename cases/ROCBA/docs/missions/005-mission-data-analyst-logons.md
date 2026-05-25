# Mission: Analyze Successful Logon Events
**Target Agent:** data-analyst

## Purpose
Identify the exact timestamps, logon types, and source IP addresses for all successful logons (Event ID 4624) on the `SRL-FORGE` system, particularly during Fred's vacation window (2020-11-10 to 2020-11-15).

## Background
We have identified several suspicious external IPs (`213.202.233.104`, `81.30.144.115`, `81.19.209.101`, `201.193.188.114`) and a brute-force IP (`85.14.242.76`). We need to correlate these with successful logon events (Event ID 4624) to determine when the attacker successfully logged into Fred's system, which accounts they used, and the logon type (e.g., Logon Type 10 for RDP, Logon Type 3 for Network/Share).

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no successful logon events are found or queries fail repeatedly, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Query `artifacts_timeline` for Event ID 4624 (Successful Logon) in the Windows Security Event Log.
- [x] Extract the timestamp, TargetUserName, LogonType, and IpAddress (source IP) for each successful logon.
- [x] Filter for the period of Fred's vacation (2020-11-10 to 2020-11-15) and any suspicious logons before that.
- [x] Correlate the successful logons with the known malicious IPs and accounts.
- [x] Update `cases/ROCBA/docs/shared_facts.md` with any newly confirmed logon sessions and compromised accounts.
- [x] Update this mission card with results.

## Results & Post-Mortem
- **Approach:**
  - Used `query_parquet.py` to inspect `artifacts_timeline` for successful logon events (Event ID 4624) from the Windows Security Event Log (`winevtx` parser).
  - Used DuckDB JSON functions to extract `TargetUserName` (index 5), `LogonType` (index 8), and `IpAddress` (index 18) from the event's nested `details.strings` array.
  - Filtered out local loopback and empty IPs to isolate remote connections, focusing on Fred's vacation window (Nov 10 - Nov 15, 2020) and correlating with known malicious IPs.
  - Registered newly discovered remote attacker IPs as IOCs using `ioc_tracker.py`.
- **Findings:**
  - **srl-helpdesk@outlook.com (Compromised Account):** Successfully logged on via RDP (Logon Type 10) on **2020-11-10 05:26:11** from IP **`174.196.200.9`**. This session is highly suspicious as it correlates perfectly with the subsequent creation of the malicious HKCU Run key persistence (Microsoft Edge service masquerade) at `06:12:41` and access to staging/BitLocker key files.
  - **fred.rocba@outlook.com / fredr (Compromised Account):** Successfully logged on from Azure VPS IP **`52.249.198.56`** on **2020-11-13 19:42:52** (Console Unlock, Logon Type 7), **2020-11-14 04:31:26** (RDP, Logon Type 10), and **2020-11-14 04:52:03** (RDP, Logon Type 10). These sessions directly align with the execution of `sdelete.exe` (anti-forensics) and the exfiltration/access of sensitive project documents (Megaforce, Airwolf, KITT, GunStar, Wolves Lair tech specs) via Drive E/F.
  - **Malicious IP Correlation:**
    - The known malicious IP `85.14.242.76` conducted massive brute-force attacks (Event ID 4625) but never achieved a successful logon (no 4624 events).
    - Other known malicious IPs (`213.202.233.104`, `81.30.144.115`, `81.19.209.101`, `201.193.188.114`) had network-level RDP connections but no successful Event ID 4624 logons under those specific IPs, suggesting they were either blocked, failed, or routed differently.
- **Confidence Rating:**
  - **High (5/5):** The event log entries are definitive, containing exact timestamps, target usernames, logon types, and source IP addresses that align perfectly with the timeline of malicious file access, staging, and anti-forensic activity.
- **Budget Tally:**
  - Orientation Budget: 5 / 5 tool calls
  - Execution Budget: 20 / 20 tool calls
  - Reporting Budget: 0 / 5 tool calls
- **NPS / Feedback:**
  - 10/10. The DuckDB JSON extraction capabilities on the Parquet files made parsing the nested Windows Event Log strings extremely fast, precise, and efficient.
