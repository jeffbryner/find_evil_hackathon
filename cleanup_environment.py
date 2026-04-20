import os
import docker
from helpers.sift_tools import SIFTOrchestrator, get_docker_socket


def main():
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Container ID not found. No container to clean up.")
        return

    try:
        with open("scratch/container_id.txt", "r") as f:
            container_id = f.read().strip()

        orchestrator = SIFTOrchestrator()
        try:
            orchestrator.container = orchestrator.client.containers.get(container_id)
        except docker.errors.NotFound:
            print(f"[*] Container {container_id[:12]} already gone.")
            os.remove("scratch/container_id.txt")
            return

        orchestrator.stop()

        if os.path.exists("scratch/container_id.txt"):
            os.remove("scratch/container_id.txt")

    except Exception as e:
        print(f"[-] Cleanup failed: {e}")


if __name__ == "__main__":
    main()
