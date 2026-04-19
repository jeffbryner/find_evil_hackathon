import docker
import os
import subprocess
import time
import sys


def get_docker_socket():
    """Dynamically discover the Docker socket (Colima or default)."""
    try:
        # Check if Colima is used and get its socket
        output = subprocess.check_output(
            ["colima", "status"], text=True, stderr=subprocess.DEVNULL
        )
        for line in output.splitlines():
            if "docker socket:" in line:
                return line.split("docker socket:")[1].strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        pass

    # Fallback to DOCKER_HOST or default socket
    if "DOCKER_HOST" in os.environ:
        return os.environ["DOCKER_HOST"]

    # Common default locations
    defaults = [
        "unix:///var/run/docker.sock",
        f"unix://{os.path.expanduser('~')}/.colima/default/docker.sock",
    ]
    for d in defaults:
        if os.path.exists(d.replace("unix://", "")):
            return d

    return "unix:///var/run/docker.sock"


class SIFTOrchestrator:
    def __init__(self, image_name="sift-volatility:latest"):
        # Use dynamic socket discovery
        self.client = docker.DockerClient(base_url=get_docker_socket())
        self.image_name = image_name
        self.container = None
        self.mount_point = "/mnt/evidence"
        self.scratch_dir = os.path.join(os.getcwd(), "scratch")
        os.makedirs(self.scratch_dir, exist_ok=True)

    def start_container(self, evidence_path):
        """Start the SIFT container with the evidence mounted as read-only."""
        abs_evidence_path = os.path.abspath(evidence_path)
        evidence_dir = os.path.dirname(abs_evidence_path)
        evidence_file = os.path.basename(abs_evidence_path)

        # Platform check for Apple Silicon
        platform = "linux/amd64"

        try:
            print(f"[*] Starting container {self.image_name} (platform: {platform})...")
            self.container = self.client.containers.run(
                self.image_name,
                detach=True,
                tty=True,
                platform=platform,
                volumes={
                    evidence_dir: {"bind": "/evidence", "mode": "ro"},
                    self.scratch_dir: {"bind": "/scratch", "mode": "rw"},
                },
                privileged=True,  # Needed for mounting inside container
                command="/bin/bash",
            )
            print(f"[+] Container {self.container.id[:12]} started.")
            return evidence_file
        except Exception as e:
            print(f"[-] Failed to start container: {e}")
            sys.exit(1)

    def execute(self, command):
        """Execute a command inside the container and return output."""
        if not self.container:
            raise Exception("Container not started.")

        print(f"[*] Executing: {command}")
        result = self.container.exec_run(command)
        return result.output.decode("utf-8"), result.exit_code

    def mount_evidence(self, evidence_file):
        """Mount the E01 image using ewfmount and then mount the resulting raw image."""
        print(f"[*] Mounting evidence file: {evidence_file}")

        # 1. Create mount points inside container
        self.execute("mkdir -p /mnt/ewf /mnt/windows")

        # 2. Use ewfmount to mount the E01
        ewf_cmd = f"ewfmount /evidence/{evidence_file} /mnt/ewf"
        output, code = self.execute(ewf_cmd)
        print(f"[*] ewfmount output: {output}")
        if code != 0:
            print(f"[-] ewfmount failed: {output}")
            return False

        # Brief delay for mount propagation
        time.sleep(2)

        # DEBUG: Check what's in /mnt/ewf
        ls_output, _ = self.execute("ls -lh /mnt/ewf/ewf1")
        print(f"[*] ls -lh /mnt/ewf/ewf1 output:\n{ls_output}")

        # 3. Find the raw image (usually /mnt/ewf/ewf1)
        # 4. Use mmls (or fdisk) to find the partition
        mmls_output, _ = self.execute("mmls /mnt/ewf/ewf1")
        if not mmls_output.strip():
            print("[*] mmls returned no output, trying fdisk -l...")
            mmls_output, _ = self.execute("fdisk -l /mnt/ewf/ewf1")

        print(f"[*] Partition table:\n{mmls_output}")

        # Basic heuristic: find the partition with 'NTFS' or the one starting at a common offset
        # For this POC, we'll try to mount the partition directly if we know the offset or use a simple grep
        # A more robust approach would parse mmls output.

        # Try to find the start sector of the NTFS partition
        import re

        match = re.search(r"(\d+)\s+.*NTFS", mmls_output)
        if match:
            start_sector = match.group(1)
            offset = int(start_sector) * 512
            mount_cmd = (
                f"mount -t ntfs -o ro,loop,offset={offset} /mnt/ewf/ewf1 /mnt/windows"
            )
            output, code = self.execute(mount_cmd)
            if code == 0:
                print("[+] Windows partition mounted at /mnt/windows")
                return True
            else:
                print(f"[-] mount failed: {output}")
        else:
            print("[*] Could not find NTFS partition in output. Trying direct mount...")
            mount_cmd = "mount -t ntfs -o ro,loop /mnt/ewf/ewf1 /mnt/windows"
            output, code = self.execute(mount_cmd)
            if code == 0:
                print("[+] Windows partition mounted directly at /mnt/windows")
                return True
            else:
                print(f"[-] Direct mount failed: {output}")

        return False

    def stop(self):
        if self.container:
            print(f"[*] Stopping container {self.container.id[:12]}...")
            self.container.stop()
            self.container.remove()
            print("[+] Container removed.")


if __name__ == "__main__":
    # Quick sanity check
    orchestrator = SIFTOrchestrator()
    # Replace with actual image path for testing
    # evidence = "images/win7-32-nromanoff-c-drive.E01"
    # file = orchestrator.start_container(evidence)
    # orchestrator.mount_evidence(file)
    # orchestrator.stop()
