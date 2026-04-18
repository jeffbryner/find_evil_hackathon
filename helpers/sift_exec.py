#!/usr/bin/env uv run python
# Description: Execute a command inside the SIFT container.
# Usage: sift_exec <command>
# Example: sift_exec fls -r /mnt/ewf/ewf1

import sys
import os

# Ensure project root is in path to import sift_tools
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if project_root not in sys.path:
    sys.path.append(project_root)

import docker
from sift_tools import get_docker_socket


def main():
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Error: Container not started. Run 'init_case' first.")
        sys.exit(1)

    with open("scratch/container_id.txt", "r") as f:
        container_id = f.read().strip()

    if len(sys.argv) < 2:
        print("Usage: sift_exec <command>")
        print('Example: sift_exec "fls -r /mnt/ewf/ewf1"')
        sys.exit(1)

    # Use the first argument if it's a single string, or join if they are separate
    if len(sys.argv) == 2:
        command = sys.argv[1]
    else:
        command = " ".join(sys.argv[1:])

    try:
        client = docker.DockerClient(base_url=get_docker_socket())
        container = client.containers.get(container_id)

        print(f"[*] Executing in SIFT: {command}")
        result = container.exec_run(command)

        print(result.output.decode("utf-8"))
        if result.exit_code != 0:
            sys.exit(result.exit_code)

    except Exception as e:
        print(f"[-] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
