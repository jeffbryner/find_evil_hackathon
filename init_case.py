import argparse
from helpers.sift_tools import SIFTOrchestrator
import os
import sys
from triage_extractor import TriageExtractor

def main():
    parser = argparse.ArgumentParser(description="Initialize a forensic case and mount evidence.")
    parser.add_argument("evidence", help="Path to the evidence image (e.g., E01 file)")
    parser.add_argument("--triage", action="store_true", help="Automatically run triage after mounting")
    
    # Handle the case where no arguments are provided (for backward compatibility with the current task)
    if len(sys.argv) == 1:
        evidence_path = "images/win7-32-nromanoff-c-drive.E01"
        triage = True # Default to true for this task to show it works
    else:
        args = parser.parse_args()
        evidence_path = args.evidence
        triage = args.triage

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
            
        if triage:
            print("[*] Running automated triage...")
            extractor = TriageExtractor(orchestrator, orchestrator.container.id, mount_path)
            extractor.run_triage()
    else:
        print("[-] Case initialization failed during mounting.")
        orchestrator.stop()
        sys.exit(1)


if __name__ == "__main__":
    main()
