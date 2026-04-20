from helpers.sift_tools import SIFTOrchestrator
import os
import sys


def main():
    evidence_path = "images/win7-32-nromanoff-c-drive.E01"
    if not os.path.exists(evidence_path):
        print(f"[-] Evidence file not found: {evidence_path}")
        sys.exit(1)

    orchestrator = SIFTOrchestrator()

    print("[*] Initializing Case: Aegis-SIFT POC")
    print(f"[*] Image: {evidence_path}")

    # Start container
    file_name = orchestrator.start_container(evidence_path)

    # Mount evidence
    mount_path = orchestrator.mount_evidence(file_name)

    if mount_path:
        print("[+] Case Initialized successfully.")
        print("[+] Container ID:", orchestrator.container.id[:12])
        print(f"[+] Evidence mounted at {mount_path} within the container.")
        # Create a simple file to track the container ID for future scripts
        with open("scratch/container_id.txt", "w") as f:
            f.write(orchestrator.container.id)
    else:
        print("[-] Case initialization failed during mounting.")
        orchestrator.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
