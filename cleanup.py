import docker
import os
from helpers.sift_tools import get_docker_socket

def main():
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Container ID not found. No container to clean up.")
        return

    try:
        with open("scratch/container_id.txt", "r") as f:
            container_id = f.read().strip()
        
        client = docker.DockerClient(base_url=get_docker_socket())
        container = client.containers.get(container_id)
        
        print(f"[*] Stopping container {container_id[:12]}...")
        # Try to unmount first
        container.exec_run("umount -a -t ntfs")
        container.exec_run("umount -a -t fuse.ewf")
        
        container.stop()
        container.remove()
        print("[+] Container removed.")
        
        os.remove("scratch/container_id.txt")
    except Exception as e:
        print(f"[-] Cleanup failed: {e}")

if __name__ == "__main__":
    main()
