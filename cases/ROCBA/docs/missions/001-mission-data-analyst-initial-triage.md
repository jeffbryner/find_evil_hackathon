# Mission: Initial Triage and Data Inventory
**Target Agent:** data-analyst

## Purpose
Inventory the extracted forensic artifacts for the ROCBA case, identify the available tables/schemas, and perform initial triage of user activity (such as browser history and user accounts) to locate initial leads.

## Background
Fred Rocba, a new SRL hire, accepted his job on 2020-10-24 and worked from home on an SRL-provided Surface system. On 2020-11-13, his home was burglarized, and his SRL system was targeted. We need to find what he had access to, what was stolen, and how/when/where it was transferred.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 25 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If `query_parquet.py` fails to find any schema or tables, or if no tables exist, stop and report immediately.

## Task Checklist
- [x] Query the available tables and schema in the ROCBA case using `query_parquet.py` with `--schema`
- [x] Identify user accounts present on the system (check if there is a `users` table or query `artifacts_timeline` / `fs_timeline`)
- [x] Analyze browser history in `browser_history.parquet` to see what Fred was working on, searching for, or downloading
- [x] Identify any key projects or directories Fred was accessing (e.g., in `fs_timeline` or `browser_history`)
- [x] Update `cases/ROCBA/docs/shared_facts.md` with findings (using the `shared-facts-sop` guidelines)
- [x] Update this mission card with results

## Results & Post-Mortem
- **Approach:** 
  1. Ran schema query to find tables (`memory_pslist`, `memory_netscan`, `memory_timeliner`, `artifacts_timeline`, `fs_timeline`, `browser_history`).
  2. Queried SAM registry parser in `artifacts_timeline` to identify local user accounts and login times.
  3. Performed targeted queries on `browser_history` and `fs_timeline` focusing on the burglary date (2020-11-13) and surrounding days (2020-11-14 to 2020-11-16).
  4. Identified files/projects accessed, external USB drives, and secure deletion tool usage.
- **Findings:**
  - **User Accounts:** Identified local users `fredr` (Fred Rocba, last login: 2020-11-14 04:51:58-08:00) and setup user `srl-h` (last login: 2020-11-10 05:26:09-08:00).
  - **Data Exfiltration:** Starting on 2020-11-13 at 19:45:54 (hours after the reported burglary), Fred (or an actor using his account) performed massive file copy operations to external USB drives (E:, F:, D:) and Google Drive (G:).
  - **Confidential Projects Targeted:** Exfiltrated projects include Project KITT, Megaforce, New Alloy Research, Vibranium/Vibrainium, Adamantium, StarFury, TIVO, Airwolf, Gunstar, Blue Thunder, and a complete export of SRL emails (`SRL-EMAIL-EXPORT.pst`).
  - **Anti-Forensics:** Downloaded Sysinternals `SDelete` at 05:38:02 on 2020-11-14 and executed it 7 times between 05:42:30 and 05:47:10 to securely erase files and destroy evidence.
  - **Post-Incident Activity:** On 2020-11-15 at 18:32:19, the user opened `D:/ROCBA-SYSTEM/Rocba-Memory.raw`, indicating possession/analysis of a raw memory image of the system.
- **Confidence Rating:** 5/5 (High confidence. The timeline from the browser history and filesystem is extremely detailed and corroborated by prefetch and registry artifacts).
- **Budget Tally:**
  - Orientation Budget: 5 / 5 tool calls
  - Execution Budget: 18 / 25 tool calls
  - Reporting Budget: 2 / 5 tool calls
- **NPS / Feedback:** 10/10. The `query_parquet.py` script and DuckDB backend are incredibly fast and made timeline analysis of 2,600+ browser entries and 1.8M+ file events seamless.
