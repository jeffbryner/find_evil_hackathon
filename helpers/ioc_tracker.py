#!/usr/bin/env uv run python
import argparse
import json
import os
import fcntl
from datetime import datetime, timezone
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Track Indicators of Compromise (IOCs) in a JSONL file."
    )
    parser.add_argument(
        "--case", required=True, help="Name of the case (folder in scratch/)"
    )

    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--add",
        help="Type of IOC to add (e.g., ip, domain, hash, filename)",
    )
    action_group.add_argument(
        "--remove",
        action="store_true",
        help="Remove an IOC (requires --value)",
    )
    action_group.add_argument(
        "--list",
        action="store_true",
        help="List all IOCs",
    )

    parser.add_argument("--value", help="The actual value of the IOC")
    parser.add_argument(
        "--source",
        help="The source or context of where the IOC was found",
    )

    args = parser.parse_args()

    case_path = os.path.join("cases", f"{args.case}/scratch")

    if not os.path.exists(case_path):
        os.makedirs(case_path, exist_ok=True)

    iocs_file = os.path.join(case_path, "iocs.jsonl")

    # Handle List
    if args.list:
        if not os.path.exists(iocs_file):
            print(f"[*] No IOCs found for case: {args.case}")
            return

        print(f"[*] IOCs for case: {args.case}")
        print("-" * 60)
        try:
            with open(iocs_file, "r") as f:
                fcntl.flock(f, fcntl.LOCK_SH)
                for line in f:
                    if line.strip():
                        ioc = json.loads(line)
                        print(
                            f"Type: {ioc.get('type'):<10} Value: {ioc.get('value'):<20} Source: {ioc.get('source')}"
                        )
        except Exception as e:
            print(f"[-] Error reading {iocs_file}: {e}")
        return

    # For Add and Remove, we need --value
    if not args.value:
        print("[-] Error: --value is required for --add or --remove")
        sys.exit(1)

    # Handle Add
    if args.add:
        if not args.source:
            print("[-] Error: --source is required when adding an IOC")
            sys.exit(1)

        ioc_data = {
            "type": args.add,
            "value": args.value,
            "source": args.source,
            "timestamp": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        # Read existing to check for duplicates/updates
        iocs = []
        updated = False
        if os.path.exists(iocs_file):
            try:
                with open(iocs_file, "r+") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    lines = f.readlines()
                    for line in lines:
                        if line.strip():
                            ioc = json.loads(line)
                            if ioc.get("value") == args.value:
                                iocs.append(ioc_data)
                                updated = True
                            else:
                                iocs.append(ioc)

                    if not updated:
                        iocs.append(ioc_data)

                    f.seek(0)
                    f.truncate()
                    for ioc in iocs:
                        f.write(json.dumps(ioc) + "\n")
            except Exception as e:
                print(f"[-] Error updating {iocs_file}: {e}")
                sys.exit(1)
        else:
            try:
                with open(iocs_file, "w") as f:
                    fcntl.flock(f, fcntl.LOCK_EX)
                    f.write(json.dumps(ioc_data) + "\n")
            except Exception as e:
                print(f"[-] Error creating {iocs_file}: {e}")
                sys.exit(1)

        action_str = "Updated" if updated else "Added"
        print(f"[+] {action_str} {args.add} IOC: {args.value} to {iocs_file}")

    # Handle Remove
    elif args.remove:
        if not os.path.exists(iocs_file):
            print(f"[-] Error: {iocs_file} does not exist.")
            sys.exit(1)

        removed = False
        iocs = []
        try:
            with open(iocs_file, "r+") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                lines = f.readlines()
                for line in lines:
                    if line.strip():
                        ioc = json.loads(line)
                        if ioc.get("value") == args.value:
                            removed = True
                            continue
                        iocs.append(ioc)

                if removed:
                    f.seek(0)
                    f.truncate()
                    for ioc in iocs:
                        f.write(json.dumps(ioc) + "\n")
                    print(f"[+] Removed IOC: {args.value} from {iocs_file}")
                else:
                    print(f"[-] IOC not found: {args.value}")
        except Exception as e:
            print(f"[-] Error removing from {iocs_file}: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
