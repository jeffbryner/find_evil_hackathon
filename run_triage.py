from sift_tools import SIFTOrchestrator
import docker
import os
import sys

def main():
    # Load container ID
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Case not initialized. Run init_case.py first.")
        sys.exit(1)
    
    with open("scratch/container_id.txt", "r") as f:
        container_id = f.read().strip()

    client = docker.DockerClient(base_url="unix:///Users/jeffbryner/.colima/default/docker.sock")
    container = client.containers.get(container_id)
    
    # We need a SIFTOrchestrator-like execution context
    class ContainerContext:
        def __init__(self, container):
            self.container = container
        def execute(self, command):
            print(f"[*] Executing in container: {command}")
            result = self.container.exec_run(command)
            return result.output.decode('utf-8'), result.exit_code

    ctx = ContainerContext(container)
    
    print("[*] Starting Triage Extraction...")
    
    # 1. Generate bodyfile using tsk_gettimes
    # Since we mounted directly, we point to the raw image /mnt/ewf/ewf1
    bodyfile_path = "/scratch/win7_bodyfile.txt"
    gettimes_cmd = f"tsk_gettimes /mnt/ewf/ewf1 > {bodyfile_path}"
    output, code = ctx.execute(f"bash -c '{gettimes_cmd}'")
    
    if code != 0:
        print(f"[-] tsk_gettimes failed: {output}")
        sys.exit(1)
    
    print("[+] Bodyfile generated in scratch space.")
    
    # 2. Convert to Parquet (runs on host)
    local_bodyfile = "scratch/win7_bodyfile.txt"
    local_parquet = "scratch/file_metadata.parquet"
    
    print("[*] Converting bodyfile to Parquet...")
    # Using the existing utility
    from bodyfile_to_parquet import parse_bodyfile
    parse_bodyfile(local_bodyfile, local_parquet)
    
    print(f"[+] Triage complete. Metadata saved to {local_parquet}")

if __name__ == "__main__":
    main()
