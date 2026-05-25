# Mission: USB Exfiltration Verification
**Target Agent:** data-analyst

## Purpose
Determine if any files were exfiltrated to a USB drive (including drive F:) during the compromise window of November 13-14, 2020, or if exfiltration was restricted to online resources like Google Drive.

## Background
The user is asking for clarification on whether files were exfiltrated to the USB drive, or only to online resources like Google Drive. We need to analyze the USB connection logs and filesystem timelines specifically for November 13-14, 2020, to see if any USB drive (like drive F: or drive E:) was connected and if files were copied to it.

## Budget & Rules of Engagement
- **Orientation Budget:** 5 tool calls
- **Execution Budget:** 20 tool calls
- **Reporting Budget:** 5 tool calls
- **Fail-Fast Condition:** If no USB connection or USB file activity is found on November 13-14, 2020, stop and report.

## Task Checklist
- [x] Read the `shared-facts-sop` and `delegating-mission-cards-sop` before acting.
- [x] Determine if any USB storage devices (such as drive F: or drive E:) were connected to the system during the incident window (November 13-14, 2020).
- [x] Query the `fs_timeline` and `artifacts_timeline` for any file access or creation events on drive E: or drive F: during November 13-14, 2020.
- [x] Verify if the files on drive F: (e.g., `Wolves_Lair_Tech_Specs.pptx`, `Quantum Particles Affected by Other Dimensions.pdf`, `The Future of KITT.pptx`) were accessed from an external USB drive connected during the incident or if they represent another path.
- [x] Update `cases/ROCBA/docs/shared_facts.md` with any clarifications or new findings. (Verified: shared facts already accurately reflect RDP drive redirection for F:).
- [x] Update this mission card with results.

## Results & Post-Mortem
*(To be filled out by the Target Agent)*
- **Approach:** Queried DuckDB tables (`artifacts_timeline` and `fs_timeline`) using the `query_parquet.py` helper to hunt for USB device connection events (registry paths, setup logs), specific drive letters (`E:`, `F:`), and events around the RDP session window on November 13-14, 2020.
- **Findings:**
  1. **USB Storage Device Connection Status**: No local USB storage devices (such as drive `E:` or drive `F:`) were physically connected to the server `SRL-FORGE` during the compromise window of November 13-14, 2020. Queries of USB-related registry keys and event logs yielded zero connection events.
  2. **Mapping of Drive F: during the RDP Session**: At **November 14, 2020, 06:01:34 UTC** (which is **November 13, 2020, 22:01:34 PST**), drive `F:` was mapped as an **RDP-redirected network drive** (`\\tsclient\F`) from the attacker's local client machine. LNK files (`SRL-EMAIL-EXPORT.lnk` and `Exported-PST.lnk`) created/modified at this timestamp resolve to the remote path `\\tsclient\F\SRL-EMAIL-EXPORT.pst` with Drive Type `4` (`DRIVE_REMOTE`), a drive serial number of `0x00000000`, and an empty volume label.
  3. **Exfiltration Vector Verification**: The exfiltration of sensitive data was strictly restricted to online resources and RDP-redirected drives. The attacker staged the file `SRL-EMAIL-EXPORT.pst` inside the local Google Drive File Stream directory on drive `G:` (`G:\My Drive\STARK-RESEARCH-LABS FOLDER\Exported-PST\SRL-EMAIL-EXPORT.pst`, Drive Type `3` - `DRIVE_FIXED`, Serial: `0x19831116`, Volume Label: `Google Drive File Stream`), and then accessed/exfiltrated it directly to their local client machine via the RDP-redirected drive `F:` (`\\tsclient\F\SRL-EMAIL-EXPORT.pst`).
- **Confidence Rating:** 5/5 (High confidence; corroborated directly by shell items, LNK files, and drive type indicators).
- **Budget Tally:** 12 tool calls.
- **NPS / Feedback:** 10/10 - Excellent parquet/timeline datasets and very clear redirection indicators!
