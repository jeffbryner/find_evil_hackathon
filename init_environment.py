import argparse
from helpers.sift_tools import SIFTOrchestrator
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Initialize the environment by starting the SIFT container."
    )
    parser.add_argument(
        "--case-dir",
        help="Root directory for the case (defaults to current directory)",
        default=os.getcwd(),
    )

    args = parser.parse_args()
    case_dir = args.case_dir

    if not os.path.exists(case_dir):
        print(f"[-] Case directory not found: {case_dir}")
        sys.exit(1)

    orchestrator = SIFTOrchestrator()

    print("[*] Initializing SIFT Environment")
    print(f"[*] Case Root: {case_dir}")

    # Start container
    success = orchestrator.start_container(case_dir)

    if success:
        print("[+] Environment Initialized successfully.")
        print("[+] Container ID:", orchestrator.container.id[:12])
        # Create a simple file to track the container ID for future scripts
        with open("scratch/container_id.txt", "w") as f:
            f.write(orchestrator.container.id)
    else:
        print("[-] Environment initialization failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
