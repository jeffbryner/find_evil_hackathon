import docker
import os
import subprocess
import time
import sys
import re
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


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
    def __init__(self, image_name="0x7eff/sift-ai:latest", case_name=None):
        # Use dynamic socket discovery
        self.client = docker.DockerClient(base_url=get_docker_socket())
        self.image_name = image_name
        self.container = None
        self.mount_point = "/mnt/evidence"
        self.case_name = case_name
        if case_name:
            self.case_dir = os.path.join(os.getcwd(), "cases", case_name)
        else:
            self.case_dir = os.getcwd()
        self.scratch_dir = os.path.join(self.case_dir, "scratch")
        os.makedirs(self.scratch_dir, exist_ok=True)

    def start_container(self):
        """Start the SIFT container with the case root mounted as read-only."""
        abs_case_root = os.path.abspath(self.case_dir)

        # Platform check for Apple Silicon
        platform = "linux/amd64"

        try:
            logging.info(
                f"[*] Starting container {self.image_name} (platform: {platform})..."
            )
            self.container = self.client.containers.run(
                self.image_name,
                detach=True,
                tty=True,
                volumes={
                    abs_case_root: {"bind": "/case", "mode": "ro"},
                    self.scratch_dir: {"bind": "/scratch", "mode": "rw"},
                },
                privileged=True,  # Needed for mounting inside container
                command="/bin/bash",
                auto_remove=True,  # Automatically remove container on stop
                cpu_percent=90,  # Limit CPU usage to 90%
                name=self.case_name if self.case_name else None,
                hostname=self.case_name if self.case_name else None,
                oom_kill_disable=True,  # Prevent OOM killer from killing the container
            )
            if self.container:
                print(f"[+] Container {self.container.id[:12]} started.")
            return True
        except Exception as e:
            print(f"[-] Failed to start container: {e}")
            sys.exit(1)

    def execute(self, command):
        """Execute a command inside the container and return output."""
        if not self.container:
            raise Exception("Container not started.")

        logging.info(f"[*] Executing: {command}")
        # Use bash shell to support pipes and other shell features
        result = self.container.exec_run(["/bin/bash", "-c", command])
        logging.info(f"[-] Exit code: {result.exit_code} cmd: {command}")
        return result.output.decode("utf-8"), result.exit_code

    def mount_evidence(self, evidence_file, case_name):
        """Mount the evidence image using imount by default, falling back to other choices."""
        evidence_basename = os.path.basename(evidence_file)

        # Safeguard: Do not attempt to mount memory images as disk images
        if "memory" in evidence_basename.lower():
            logging.info(
                f"[*] Registering memory image: {evidence_basename} (will be analyzed with Volatility)"
            )
            # Memory images are not mounted, so we return the path within the container
            return f"/case/{evidence_file}"

        logging.info(
            f"[*] Mounting evidence file: {evidence_file} for case: {case_name}"
        )

        mount_path = f"/mnt/cases/{case_name}/{evidence_basename}"
        self.execute(f"mkdir -p {mount_path}")

        evidence_path_in_container = f"/case/{evidence_file}"

        # Determine if file is EWF (Expert Witness Format)
        is_ewf = evidence_basename.lower().endswith((".e01", ".ex01", ".l01", ".lx01"))

        # 1. Try imount by default on the original evidence file
        logging.info(
            f"[*] Attempting imount by default on {evidence_path_in_container}..."
        )
        mount_cmd = f"imount --no-interaction -v -k --pretty --mountdir {mount_path} {evidence_path_in_container}"
        output, code = self.execute(mount_cmd)
        if code == 0:
            if self._validate_mount(mount_path):
                logging.info(
                    f"[+] Successfully mounted partition using imount at {mount_path}"
                )
                # Perform post-mount optimization (bind mounting nested OS root and saving offset)
                self._post_mount_processing(
                    mount_path, evidence_path_in_container, evidence_basename
                )

                # Ensure compatibility for downstream tools that expect raw image at /mnt/ewf/.../ewf1
                ewf_mount_dir = f"/mnt/ewf/{case_name}/{evidence_basename}"
                self.execute(f"mkdir -p {ewf_mount_dir}")
                if is_ewf:
                    logging.info(
                        f"[*] Setting up companion ewfmount for {evidence_basename}..."
                    )
                    ewf_cmd = f"ewfmount {evidence_path_in_container} {ewf_mount_dir}"
                    self.execute(ewf_cmd)
                else:
                    logging.info(
                        f"[*] Creating companion raw image symlink for {evidence_basename}..."
                    )
                    self.execute(
                        f"ln -sf {evidence_path_in_container} {ewf_mount_dir}/ewf1"
                    )
                return mount_path
            else:
                logging.info(
                    f"[*] imount succeeded but validation failed at {mount_path}. Unmounting..."
                )
                self.execute(f"umount {mount_path}")

        # 2. Revert to other choices
        logging.info(
            "[*] Default imount failed or was invalid. Reverting to other choices..."
        )

        raw_image = None
        if is_ewf:
            ewf_mount_dir = f"/mnt/ewf/{case_name}/{evidence_basename}"
            self.execute(f"mkdir -p {ewf_mount_dir}")

            ewf_cmd = f"ewfmount {evidence_path_in_container} {ewf_mount_dir}"
            output, code = self.execute(ewf_cmd)
            if code == 0:
                # Brief delay for mount propagation
                time.sleep(2)
                raw_image = f"{ewf_mount_dir}/ewf1"
            else:
                logging.error(f"[-] ewfmount failed: {output}")
        else:
            # For non-EWF files, use the evidence file directly as raw image
            raw_image = evidence_path_in_container
            # Create a symlink to guarantee /mnt/ewf/.../ewf1 exists for downstream scripts
            ewf_mount_dir = f"/mnt/ewf/{case_name}/{evidence_basename}"
            self.execute(
                f"mkdir -p {ewf_mount_dir} && ln -sf {evidence_path_in_container} {ewf_mount_dir}/ewf1"
            )

        if not raw_image:
            logging.error("[-] No valid raw image source available.")
            return False

        # 3. Discovery loop on raw_image
        discovery_methods = [
            ("mmls", self._get_ntfs_offsets_mmls),
            ("parted", self._get_ntfs_offsets_parted),
            ("brute-force", self._get_ntfs_offsets_bruteforce),
        ]

        for method_name, discovery_func in discovery_methods:
            logging.info(
                f"[*] Attempting discovery via {method_name} on {raw_image}..."
            )
            offsets = discovery_func(raw_image)
            for offset in offsets:
                logging.info(
                    f"[*] Attempting mount at offset {offset} (Method: {method_name})"
                )
                mount_cmd = f"mount -t ntfs -o ro,loop,show_sys_files,streams_interface=windows,offset={offset} {raw_image} {mount_path}"
                output, code = self.execute(mount_cmd)
                if code != 0:
                    logging.info(
                        f"[*] Standard mount failed, trying ntfs-3g with force..."
                    )
                    if offset == 0:
                        mount_cmd = f"mount -t ntfs-3g -o ro,show_sys_files,streams_interface=windows,force {raw_image} {mount_path}"
                    else:
                        mount_cmd = f"mount -t ntfs-3g -o ro,loop,show_sys_files,streams_interface=windows,offset={offset},force {raw_image} {mount_path}"
                    output, code = self.execute(mount_cmd)

                if code == 0:
                    if self._validate_mount(mount_path):
                        logging.info(
                            f"[+] Successfully mounted NTFS partition at {mount_path} using {method_name} (offset: {offset})"
                        )
                        # Perform post-mount optimization (bind mounting nested OS root and saving offset)
                        self._post_mount_processing(
                            mount_path,
                            raw_image,
                            evidence_basename,
                            offset_bytes=offset,
                        )
                        return mount_path
                    else:
                        logging.info(
                            f"[*] Mount succeeded but validation failed at {mount_path}. Unmounting..."
                        )
                        self.execute(f"umount {mount_path}")

        # fallback: imount on raw_image
        logging.info(
            "[*] All offset-based discovery failed. Trying imount on raw image..."
        )
        mount_cmd = f"imount --no-interaction -v -k --pretty --mountdir {mount_path} {raw_image}"
        output, code = self.execute(mount_cmd)
        if code == 0:
            if self._validate_mount(mount_path):
                logging.info(
                    f"[+] Successfully mounted NTFS partition directly at {mount_path}"
                )
                # Perform post-mount optimization (bind mounting nested OS root and saving offset)
                self._post_mount_processing(mount_path, raw_image, evidence_basename)
                return mount_path
            else:
                self.execute(f"umount {mount_path}")

        # fallback to dissect's target-mount
        logging.info("[*] All offset-based discovery failed. Trying target-mount...")
        mount_cmd = f"target-mount {raw_image} {mount_path}"
        output, code = self.execute(mount_cmd)
        if code == 0:
            if self._validate_mount(mount_path):
                logging.info(
                    f"[+] Successfully mounted partition directly at {mount_path}"
                )
                # Perform post-mount optimization (bind mounting nested OS root and saving offset)
                self._post_mount_processing(mount_path, raw_image, evidence_basename)
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

    def _get_all_partition_offsets_mmls(self, raw_image):
        """Find start sectors of all valid data partitions using mmls."""
        if not raw_image:
            return []
        output, _ = self.execute(f"mmls {raw_image}")
        offsets = []
        for line in output.splitlines():
            # Exclude metadata and unallocated space
            if any(
                x in line for x in ["Meta", "Unallocated", "Table", "Extended", "-----"]
            ):
                continue
            # Look for a line with partition slot and start sector
            # Format: '02:  00:00     0000000128   0000204799   0000204672   FAT32 (0x0c)'
            match = re.search(r"^\s*\d+:\s+\S+\s+(\d+)", line)
            if not match:
                match = re.search(r"^\s*\d+:\s+(\d+)", line)
            if match:
                start_sector = int(match.group(1))
                offsets.append(start_sector)
        return offsets

    def _get_all_partition_offsets_parted(self, raw_image):
        """Find start sectors of all valid partitions using parted."""
        if not raw_image:
            return []
        output, _ = self.execute(f"parted -s {raw_image} unit s print")
        offsets = []
        for line in output.splitlines():
            # parted output units are in sectors:
            # Number  Start      End        Size       File system  Name  Flags
            #  1      128s       204799s    204672s    fat32
            match = re.search(r"^\s*\d+\s+(\d+)s", line)
            if match:
                offsets.append(int(match.group(1)))
        return offsets

    def _get_ntfs_offsets_bruteforce(self, raw_image):
        """Brute-force scan for NTFS headers in the first 1GB."""
        # We look for the NTFS signature 'NTFS    ' (EB 52 90 4E 54 46 53 20)
        # We'll use grep on the raw image to find the offset of 'NTFS'
        # Since we are in a container, we can use 'grep -a -b -o'
        # But grep offset is byte-level.
        cmd = f"head --bytes=1G {raw_image} | grep -a -b -o 'NTFS    ' | head -n 5"
        output, _ = self.execute(cmd)
        logging.info(f"[*] Brute-force scan output:\n{output}")
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
        """Validate the mount by verifying it lists at least one file or folder."""
        output, _ = self.execute(f"ls -A {mount_path}")
        return len(output.strip()) > 0

    def _get_best_mount_root(self, mount_path):
        """Evaluate mount_path and its subdirectories to find the best OS root."""
        candidates = [mount_path]

        # List direct subdirectories under mount_path
        output, _ = self.execute(f"find {mount_path} -maxdepth 1 -mindepth 1 -type d")
        for line in output.splitlines():
            line = line.strip()
            if line:
                candidates.append(line)

        common_dirs = [
            "windows",
            "users",
            "program files",
            "documents and settings",
            "filesystems",
            "volumes",
            "sysvol",
            "tmp",
            "home",
            "proc",
            "etc",
            "var",
        ]

        best_candidate = mount_path
        best_score = -1

        for candidate in candidates:
            # List direct contents of candidate (lowercase)
            ls_out, _ = self.execute(f"ls -1 {candidate}")
            contents = [line.strip().lower() for line in ls_out.splitlines()]
            score = sum(1 for d in common_dirs if d in contents)
            logging.info(
                f"[*] Evaluated mount candidate {candidate} with score: {score}"
            )
            if score > best_score:
                best_score = score
                best_candidate = candidate

        return best_candidate, best_score

    def _find_sector_for_index(self, raw_image, part_idx):
        """Find starting sector for a given partition index (slot) in mmls."""
        if not raw_image:
            return None
        output, _ = self.execute(f"mmls {raw_image}")
        for line in output.splitlines():
            # Format: '03:  00:01     0000206848   0419430399   0417361920   NTFS (0x07)'
            # or: '03:  -----     0000206848   ...'
            match = re.search(r"^\s*0*" + str(part_idx) + r":\s+\S+\s+(\d+)", line)
            if not match:
                match = re.search(r"^\s*0*" + str(part_idx) + r":\s+(\d+)", line)
            if match:
                return int(match.group(1))
        return None

    def _find_sector_for_index_parted(self, raw_image, part_idx):
        """Find starting sector using parted."""
        if not raw_image:
            return None
        output, _ = self.execute(f"parted -s {raw_image} unit s print")
        for line in output.splitlines():
            match = re.search(r"^\s*" + str(part_idx) + r"\s+(\d+)s", line)
            if match:
                return int(match.group(1))
        return None

    def _save_offset(self, evidence_basename, offset_sectors):
        """Save the calculated partition sector offset to scratch directory."""
        scratch_evidence_dir = f"/scratch/{evidence_basename}"
        self.execute(f"mkdir -p {scratch_evidence_dir}")
        self.execute(f"echo {offset_sectors} > {scratch_evidence_dir}/offset.txt")
        logging.info(
            f"[+] Saved partition offset of {offset_sectors} sectors to {scratch_evidence_dir}/offset.txt"
        )

    def _post_mount_processing(
        self, mount_path, raw_image, evidence_basename, offset_bytes=None
    ):
        """Perform post-mount validation, bind-mounting nested partitions, and recording offset."""
        best_candidate, best_score = self._get_best_mount_root(mount_path)

        offset_sectors = 0
        if offset_bytes is not None:
            offset_sectors = offset_bytes // 512
        else:
            # Try to determine partition offset sectors from the best candidate path if imount was used
            # e.g., /mnt/cases/NISTDL/cfreds_2015_data_leakage_pc.dd/cfreds_2015_data_leakage_pc-3-ntfs
            match = re.search(r"-(\d+)(?:-|$)", os.path.basename(best_candidate))
            if match and raw_image:
                part_idx = int(match.group(1))
                logging.info(
                    f"[*] Parsed partition index {part_idx} from {best_candidate}"
                )
                start_sector = self._find_sector_for_index(raw_image, part_idx)
                if start_sector is None:
                    start_sector = self._find_sector_for_index_parted(
                        raw_image, part_idx
                    )
                if start_sector is not None:
                    offset_sectors = start_sector
                else:
                    logging.warning(
                        f"[-] Could not find start sector for partition index {part_idx}"
                    )
            elif best_candidate == mount_path and raw_image:
                # If there are no nested subdirectories but the image contains partitions
                # we query mmls or parted to find the start sector of the primary/single partition
                logging.info(
                    f"[*] Best candidate is the mount root itself. Discovering partition offsets for {raw_image}..."
                )
                mmls_offsets = self._get_all_partition_offsets_mmls(raw_image)
                if mmls_offsets:
                    logging.info(
                        f"[+] Found partition start sectors via mmls: {mmls_offsets}"
                    )
                    # If we found partition offsets, use the first one as default
                    offset_sectors = mmls_offsets[0]
                else:
                    parted_offsets = self._get_all_partition_offsets_parted(raw_image)
                    if parted_offsets:
                        logging.info(
                            f"[+] Found partition start sectors via parted: {parted_offsets}"
                        )
                        offset_sectors = parted_offsets[0]

        self._save_offset(evidence_basename, offset_sectors)

        if best_score > 0 and best_candidate != mount_path:
            logging.info(
                f"[+] Nested OS partition found at {best_candidate}. Bind-mounting directly to {mount_path}..."
            )
            self.execute(f"mount --bind {best_candidate} {mount_path}")

    def stop(self):
        if self.container:
            container_id = getattr(self.container, "id", "unknown")
            print(f"[*] Stopping container {container_id[:12]}...")
            # Unmount any bind mounts recursively/lazyly first
            self.execute("umount -l /mnt/cases/*/* 2>/dev/null || true")
            self.execute("umount -l /mnt/cases/* 2>/dev/null || true")
            # Try to unmount everything first
            self.execute("umount -a -t ntfs")
            self.execute("umount -a -t fuse.ewf")
            self.execute("umount -a -t fuse.xmount")
            self.execute("umount -a -t fuse")
            self.container.stop()
            print("[+] Container removed.")


if __name__ == "__main__":
    # Quick sanity check
    orchestrator = SIFTOrchestrator()
    # Replace with actual image path for testing
    # evidence = "images/win7-32-nromanoff-c-drive.E01"
    # file = orchestrator.start_container(evidence)
    # orchestrator.mount_evidence(file)
    # orchestrator.stop()
