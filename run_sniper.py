import docker
import os
import sys
import re

def main():
    if len(sys.argv) < 2:
        print("Usage: uv run run_sniper.py <file_path>")
        sys.exit(1)

    target_path = sys.argv[1]

    # Load container ID
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Case not initialized. Run init_case.py first.")
        sys.exit(1)
    
    with open("scratch/container_id.txt", "r") as f:
        container_id = f.read().strip()

    client = docker.DockerClient(base_url="unix:///Users/jeffbryner/.colima/default/docker.sock")
    container = client.containers.get(container_id)
    
    def execute(command):
        print(f"[*] Executing in container: {command}")
        result = container.exec_run(command)
        return result.output.decode('utf-8'), result.exit_code

    print(f"[*] Sniper Specialist: Investigating {target_path}")
    
    # 1. Find Inode using fls
    # We need to find the parent directory first
    parts = target_path.split('/')
    filename = parts[-1]
    # fls needs the path relative to the mount point or we can just grep the whole fls -r
    # But fls -r is slow. Let's try to find it in the metadata we already have.
    
    import duckdb
    con = duckdb.connect(database=':memory:')
    con.execute("CREATE TABLE file_metadata AS SELECT * FROM read_parquet('scratch/file_metadata.parquet')")
    res = con.execute(f"SELECT inode FROM file_metadata WHERE file_path = '{target_path}'").fetchone()
    
    if not res:
        print(f"[-] Could not find inode for {target_path} in metadata.")
        sys.exit(1)
    
    inode = str(res[0]).split('-')[0] # Sleuthkit inodes can be 123-128-1
    print(f"[+] Found Inode: {inode}")

    # 2. Extract file using icat
    extracted_path = f"/scratch/extracted_{filename}"
    icat_cmd = f"icat -r /mnt/ewf/ewf1 {inode} > {extracted_path}"
    output, code = execute(f"bash -c '{icat_cmd}'")
    
    if code != 0:
        print(f"[-] icat failed: {output}")
        sys.exit(1)
    
    print(f"[+] File extracted to host scratch space as extracted_{filename}")

    # 3. Analyze headers (on host)
    local_path = f"scratch/extracted_{filename}"
    print("[*] Analyzing file headers...")
    with open(local_path, "rb") as f:
        header = f.read(2)
        if header == b"MZ":
            print("[+] Header Match: Windows PE Executable (MZ)")
        else:
            print(f"[-] Header Mismatch: Found {header}")

    # 4. Strings analysis (on host)
    print("[*] Extracting suspicious strings...")
    import subprocess
    try:
        strings_output = subprocess.check_output(["strings", local_path]).decode('utf-8', errors='ignore')
        suspicious = [line for line in strings_output.split('\n') if re.search(r'http|https|cmd|powershell|kernel32|createprocess', line, re.I)]
        print(f"[+] Found {len(suspicious)} suspicious strings.")
        for s in suspicious[:10]:
            print(f"    {s.strip()}")
    except Exception as e:
        print(f"[-] Strings analysis failed: {e}")

if __name__ == "__main__":
    main()
