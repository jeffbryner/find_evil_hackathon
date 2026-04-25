#!/usr/bin/env uv run python
import argparse
import json
import os
import fcntl
from datetime import datetime
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Track Indicators of Compromise (IOCs) in an append-only JSONL file."
    )
    parser.add_argument(
        "--case", required=True, help="Name of the case (folder in scratch/)"
    )
    parser.add_argument(
        "--add",
        required=True,
        help="Type of IOC to add (e.g., ip, domain, hash, filename)",
    )
    parser.add_argument("--value", required=True, help="The actual value of the IOC")
    parser.add_argument(
        "--source",
        required=True,
        help="The source or context of where the IOC was found",
    )

    args = parser.parse_args()

    case_path = os.path.join("scratch", args.case)
    if not os.path.exists(case_path):
        # We don't create the case directory here, it should be created by init_case
        # But we'll allow it just in case if scratch/ exists
        if not os.path.exists("scratch"):
            print("[-] Error: 'scratch/' directory does not exist.")
            sys.exit(1)
        os.makedirs(case_path, exist_ok=True)

    iocs_file = os.path.join(case_path, "iocs.jsonl")

    ioc_data = {
        "type": args.add,
        "value": args.value,
        "source": args.source,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }

    # Append safely using fcntl for process-safe concurrent writes
    try:
        with open(iocs_file, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(json.dumps(ioc_data) + "\n")
            # fcntl.flock(f, fcntl.LOCK_UN) is automatically called when file is closed
    except Exception as e:
        print(f"[-] Error writing to {iocs_file}: {e}")
        sys.exit(1)

    print(f"[+] Added {args.add} IOC: {args.value} to {iocs_file}")


if __name__ == "__main__":
    main()
