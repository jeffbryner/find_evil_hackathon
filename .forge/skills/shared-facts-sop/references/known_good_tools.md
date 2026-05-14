---
name: known_good_tools
description: Artifacts likely to be found in a forensic investigation that are known good tools, often used to perform the investigation itself and can be likely ignored as leads when searching for suspicious activities.
---
# Known Good Forensic & Admin Tools

When conducting forensic analysis, investigators often use specialized tools to acquire memory, disk images, and triage data. These tools exhibit behavior that closely mimics malware (e.g., deploying services over SMB to every host, dumping memory, opening listening ports). 

**Agents MUST explicitly filter out these known good tools from their threat hunting queries to avoid false positives.**

## F-Response (Forensic Remote Collection)
F-Response is used to remotely mount physical drives and memory from target machines to an investigator's workstation.
- **Binaries:** `subject_srv.exe`, `subject_srv.ex`, `ftusbsrvc.exe`
- **Drivers:** `Mnemosyne.sys`
- **Network Activity:** Listens on TCP port `3262`. Connects back to investigator workstations (often on ports like `5682` or `33000`).
- **Behavior:** Deploys a service named "F-Response Subject" to target hosts over SMB.
- `Mnemosyne_x64.sys`: F-Response driver usually found at `C:\Windows\System32\Mnemosyne_x64.sys`.
- `usboesrv.exe`: KernelPro USB over Ethernet (part of F-Response) usually found at `C:\Windows\System32\usboesrv.exe`.
- `f-response-lm-srv.exe`: F-Response License Manager Service `C:\Program Files\F-Response\f-response-lm-srv.exe`.
- `femc.exe`: F-Response Enterprise Management Console `C:\Program Files\F-Response\femc.exe`.

## Other Common DFIR Tools (Examples to ignore if authorized)
- **KAPE:** `kape.exe`, `tscc.exe`, `bstrings.exe`
- **Velociraptor:** `velociraptor.exe`
- **Sysinternals (often dual-use, verify intent):** `psexec.exe`, `procdump.exe`

## Common IT tools
- **Puppet:** `puppet`, `/Program Files/Puppet Labs/Puppet/puppet` Puppet from Puppet Labs is used to phone home to controllers for configuration updates.
- **McAfee:** `mcafee`, `/Program Files/McAfee` McAfee antivirus

*Note: If these tools are observed, verify with the Case Lead or user if they were part of the authorized forensic collection process for the current case.*