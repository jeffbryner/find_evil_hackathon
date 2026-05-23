import argparse
import os
import sys
import docker
from helpers.sift_tools import SIFTOrchestrator


def main():
    parser = argparse.ArgumentParser(
        description="Clean up the forensic environment by stopping the SIFT container associated with a specific case."
    )
    parser.add_argument("--case", required=True, help="Name of the forensic case")
    args = parser.parse_args()
    case_name = args.case

    orchestrator = SIFTOrchestrator(case_name=case_name)
    container_id_file = os.path.join(orchestrator.scratch_dir, "container_id.txt")

    if not os.path.exists(container_id_file):
        print(
            f"[-] Container ID file not found for case {case_name}. No container to clean up."
        )
        return

    try:
        with open(container_id_file, "r") as f:
            container_id = f.read().strip()

        try:
            orchestrator.container = orchestrator.client.containers.get(container_id)
        except Exception:
            print(f"[*] Container {container_id[:12]} already gone.")
            os.remove(container_id_file)
            return

        orchestrator.stop()

        if os.path.exists(container_id_file):
            os.remove(container_id_file)

    except Exception as e:
        print(f"[-] Cleanup failed: {e}")


if __name__ == "__main__":
    main()
