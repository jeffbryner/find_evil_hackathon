import docker
import os
import subprocess
import time
import sys
import re


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

    def start_container(self, case_root=None):
        """Start the SIFT container with the case root mounted as read-only."""
        if case_root is None:
            case_root = os.getcwd()

        abs_case_root = os.path.abspath(case_root)

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
                    abs_case_root: {"bind": "/cases", "mode": "ro"},
                    self.scratch_dir: {"bind": "/scratch", "mode": "rw"},
                },
                privileged=True,  # Needed for mounting inside container
                command="/bin/bash",
            )
            print(f"[+] Container {self.container.id[:12]} started.")
            return True
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

    def mount_evidence(self, evidence_file, case_name):
        """Mount the E01 image using ewfmount and then mount the resulting raw image."""
        evidence_basename = os.path.basename(evidence_file)

        # Safeguard: Do not attempt to mount memory images as disk images
        if "memory" in evidence_basename.lower():
            print(
                f"[!] Skipping mount for {evidence_basename}: Memory images should be analyzed with Volatility, not mounted as disks."
            )
            return False

        print(f"[*] Mounting evidence file: {evidence_file} for case: {case_name}")

        # Create unique mount points
        ewf_mount_dir = f"/mnt/ewf/{case_name}/{evidence_basename}"
        mount_path = f"/mnt/cases/{case_name}/{evidence_basename}"

        # 1. Create mount points inside container
        self.execute(f"mkdir -p {ewf_mount_dir} {mount_path}")

        # 2. Use ewfmount to mount the E01
        # evidence_file is relative to the case root (mounted at /cases)
        ewf_cmd = f"ewfmount /cases/{evidence_file} {ewf_mount_dir}"
        output, code = self.execute(ewf_cmd)
        if code != 0:
            print(f"[-] ewfmount failed: {output}")
            return False

        # Brief delay for mount propagation
        time.sleep(2)

        raw_image = f"{ewf_mount_dir}/ewf1"

        # 3. Discovery loop
        discovery_methods = [
            ("mmls", self._get_ntfs_offsets_mmls),
            ("parted", self._get_ntfs_offsets_parted),
            ("brute-force", self._get_ntfs_offsets_bruteforce),
        ]

        for method_name, discovery_func in discovery_methods:
            print(f"[*] Attempting discovery via {method_name}...")
            offsets = discovery_func(raw_image)
            for offset in offsets:
                print(
                    f"[*] Attempting mount at offset {offset} (Method: {method_name})"
                )
                mount_cmd = (
                    f"mount -t ntfs -o ro,loop,offset={offset} {raw_image} {mount_path}"
                )
                output, code = self.execute(mount_cmd)
                if code == 0:
                    if self._validate_mount(mount_path):
                        print(
                            f"[+] Successfully mounted NTFS partition at {mount_path} using {method_name} (offset: {offset})"
                        )
                        return mount_path
                    else:
                        print(
                            f"[*] Mount succeeded but validation failed at {mount_path}. Unmounting..."
                        )
                        self.execute(f"umount {mount_path}")

        # Final fallback: direct mount
        print("[*] All offset-based discovery failed. Trying direct mount...")
        mount_cmd = f"mount -t ntfs -o ro,loop {raw_image} {mount_path}"
        output, code = self.execute(mount_cmd)
        if code == 0:
            if self._validate_mount(mount_path):
                print(
                    f"[+] Successfully mounted NTFS partition directly at {mount_path}"
                )
                return mount_path
            else:
                self.execute(f"umount {mount_path}")

        return False

    def _get_ntfs_offsets_mmls(self, raw_image):
        """Find NTFS offsets using mmls."""
        output, _ = self.execute(f"mmls {raw_image}")
        offsets = []
        for line in output.splitlines():
            if "NTFS" in line:
                match = re.search(r"(\d+)\s+.*NTFS", line)
                if match:
                    offsets.append(int(match.group(1)) * 512)
        return offsets

    def _get_ntfs_offsets_parted(self, raw_image):
        """Find NTFS offsets using parted."""
        output, _ = self.execute(f"parted -s {raw_image} unit b print")
        offsets = []
        for line in output.splitlines():
            if "ntfs" in line.lower():
                # parted output format: Number  Start  End  Size  File system  Name  Flags
                # Example: 1      1048576B  25578255359B  25577206784B  ntfs          boot
                match = re.search(r"^\s*\d+\s+(\d+)B", line)
                if match:
                    offsets.append(int(match.group(1)))
        return offsets

    def _get_ntfs_offsets_bruteforce(self, raw_image):
        """Brute-force scan for NTFS headers in the first 1GB."""
        # We look for the NTFS signature 'NTFS    ' (EB 52 90 4E 54 46 53 20)
        # We'll use grep on the raw image to find the offset of 'NTFS'
        # Since we are in a container, we can use 'grep -a -b -o'
        # But grep offset is byte-level.
        cmd = f"head -c 1G {raw_image} | grep -a -b -o 'NTFS    ' | head -n 5"
        output, _ = self.execute(cmd)
        offsets = []
        for line in output.splitlines():
            # Format is offset:match
            match = re.search(r"^(\d+):", line)
            if match:
                # Signature is 3 bytes in (EB 52 90) then 'NTFS'
                # So the 'NTFS' match starts at offset 3 of the sector.
                byte_offset = int(match.group(1)) - 3
                if byte_offset >= 0 and byte_offset % 512 == 0:
                    offsets.append(byte_offset)
        return offsets

    def _validate_mount(self, mount_path):
        """Validate the mount by checking for common Windows directories."""
        output, _ = self.execute(f"ls {mount_path}")
        output_lower = output.lower()
        common_dirs = ["windows", "users", "program files", "documents and settings"]
        found = [d for d in common_dirs if d in output_lower]
        return len(found) >= 2

    def stop(self):
        if self.container:
            print(f"[*] Stopping container {self.container.id[:12]}...")
            # Try to unmount everything first
            self.execute("umount -a -t ntfs")
            self.execute("umount -a -t fuse.ewf")
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
