import argparse
from helpers.sift_tools import SIFTOrchestrator, get_docker_socket
import os
import sys
import docker
from triage_extractor import TriageExtractor


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a forensic case and mount evidence images.",
        usage="uv run init_case.py --case SRL2018  images/*",
    )
    parser.add_argument("--case", required=True, help="Name of the forensic case")
    parser.add_argument(
        "evidence", nargs="+", help="Path(s) to the evidence images (e.g., E01 files)"
    )
    args = parser.parse_args()
    case_name = args.case
    evidence_paths = args.evidence

    orchestrator = SIFTOrchestrator()

    # Check if environment is already running
    container_id = None
    if os.path.exists("scratch/container_id.txt"):
        with open("scratch/container_id.txt", "r") as f:
            container_id = f.read().strip()

    if container_id:
        try:
            client = docker.DockerClient(base_url=get_docker_socket())
            orchestrator.container = client.containers.get(container_id)
            print(f"[*] Using existing SIFT container: {container_id[:12]}")
        except Exception:
            container_id = None

    if not container_id:
        print("[*] Environment not running. Initializing...")
        orchestrator.start_container()
        with open("scratch/container_id.txt", "w") as f:
            f.write(orchestrator.container.id)

    print(f"[*] Initializing Case: {case_name}")

    mounted_paths = []
    for evidence_path in evidence_paths:
        if not os.path.exists(evidence_path):
            print(f"[-] Evidence file not found: {evidence_path}")
            continue

        # Mount evidence
        mount_path = orchestrator.mount_evidence(evidence_path, case_name)
        if mount_path:
            print(f"[+] Evidence {evidence_path} mounted at {mount_path}")
            mounted_paths.append(mount_path)
        else:
            print(f"[-] Failed to mount {evidence_path}")


if __name__ == "__main__":
    main()
