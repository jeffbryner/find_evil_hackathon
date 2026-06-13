import argparse
import os
import sys
import docker
from sift_tools import SIFTOrchestrator, get_docker_socket


def main():
    parser = argparse.ArgumentParser(
        description="Easy helper for mere humans to execute a command inside the SIFT container."
    )
    parser.add_argument("--case", required=True, help="Name of the forensic case")
    parser.add_argument("cmd", nargs="+", help="Command to execute")

    args = parser.parse_args()
    case_name = args.case
    command = " ".join(args.cmd)

    case_scratch_dir = os.path.join("cases", case_name, "scratch")
    container_id_file = os.path.join(case_scratch_dir, "container_id.txt")

    if not os.path.exists(container_id_file):
        print(
            f"[-] Error: Container not started for case {case_name}. Run 'uv run start_case_container.py' first."
        )
        sys.exit(1)

    with open(container_id_file, "r") as f:
        container_id = f.read().strip()

    orchestrator = SIFTOrchestrator(case_name=case_name)
    try:
        orchestrator.container = orchestrator.client.containers.get(container_id)
    except docker.errors.NotFound:
        print(f"[-] Error: Container {container_id[:12]} not found.")
        sys.exit(1)

    output, code = orchestrator.execute(command)
    print(output)
    sys.exit(code)


if __name__ == "__main__":
    main()
