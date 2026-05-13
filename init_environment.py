import argparse
from helpers.sift_tools import SIFTOrchestrator
import os
import sys


def main():
    parser = argparse.ArgumentParser(
        description="Initialize the environment by starting the SIFT container."
    )
    parser.add_argument(
        "--case",
        required=True,
        help="Name of the forensic case",
    )

    args = parser.parse_args()
    case_name = args.case

    orchestrator = SIFTOrchestrator(case_name=case_name)

    print("[*] Initializing SIFT Environment")
    print(f"[*] Case Root: {orchestrator.case_dir}")

    # Start container
    success = orchestrator.start_container()

    if success and orchestrator.container:
        print("[+] Environment Initialized successfully.")
        print("[+] Container ID:", str(orchestrator.container.id)[:12])
        # Create a simple file to track the container ID for future scripts
        container_id_file = os.path.join(orchestrator.scratch_dir, "container_id.txt")
        with open(container_id_file, "w") as f:
            f.write(str(orchestrator.container.id))
    else:
        print("[-] Environment initialization failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
