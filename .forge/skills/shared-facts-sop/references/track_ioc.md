---
name: track_ioc
description: Records a new Indicator of Compromise (IOC) for a case to share with other agents.
---

# Command: Track IOC
# Description: Manages IOCs (IP, hash, domain, etc.) across the shared iocs.jsonl file for cross-agent correlation.

## Steps
1. Identify a suspicious artifact (e.g., a C2 IP address or a malicious file hash).
2. Execute `uv run helpers/ioc_tracker.py --case <case_name> --add <type> --value <value> --source <discovery_context>`.
3. Verify that the IOC is successfully recorded (output confirms the addition).

## Usage Examples
```bash
• Add or Update an IOC:
 uv run helpers/ioc_tracker.py --case my_case --add ip --value 1.2.3.4 --source "Network Log"
• List all IOCs:
 uv run helpers/ioc_tracker.py --case my_case --list
• Remove an IOC:
 uv run helpers/ioc_tracker.py --case my_case --remove --value 1.2.3.4
```

## Integration
- Recorded IOCs are automatically available via the `iocs` view in `query_parquet.py`.
- Other agents can join this view against their forensic timelines to find related activity.
