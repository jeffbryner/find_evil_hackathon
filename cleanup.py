import docker
import os

def main():
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Container ID not found. No container to clean up.")
        return

    try:
        with open("scratch/container_id.txt", "r") as f:
            container_id = f.read().strip()
        
        client = docker.DockerClient(base_url="unix:///Users/jeffbryner/.colima/default/docker.sock")
        container = client.containers.get(container_id)
        
        print(f"[*] Stopping container {container_id[:12]}...")
        container.stop()
        container.remove()
        print("[+] Container removed.")
        
        os.remove("scratch/container_id.txt")
    except Exception as e:
        print(f"[-] Cleanup failed: {e}")

if __name__ == "__main__":
    main()
