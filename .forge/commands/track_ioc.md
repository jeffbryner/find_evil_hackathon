---
name: track_ioc
description: Records a new Indicator of Compromise (IOC) for a case to share with other agents.
---

# Command: Track IOC
# Description: Appends a new IOC (IP, hash, domain, etc.) to the case's shared iocs.jsonl file for cross-agent correlation.

## Steps
1. Identify a suspicious artifact (e.g., a C2 IP address or a malicious file hash).
2. Execute `uv run helpers/ioc_tracker.py --case <case_name> --add <type> --value <value> --source <discovery_context>`.
3. Verify that the IOC is successfully recorded (output confirms the addition).

## Usage Example
```bash
uv run helpers/ioc_tracker.py --case SRL --add ip --value 199.73.28.114 --source "memory_netscan discovery"
```

## Integration
- Recorded IOCs are automatically available via the `iocs` view in `query_parquet.py`.
- Other agents can join this view against their forensic timelines to find related activity.
