import os
import sys
import duckdb
import re
from helpers.sift_tools import SIFTOrchestrator


class TriageExtractor:
    def __init__(self, orchestrator, container_id, mount_path):
        self.orchestrator = orchestrator
        self.container_id = container_id
        self.mount_path = mount_path
        # mount_path is /mnt/cases/<case_name>/<evidence_name>
        parts = self.mount_path.split("/")
        self.real_case_name = parts[-2]
        self.evidence_name = parts[-1]
        self.scratch_dir = os.path.join(
            os.getcwd(), "scratch", self.real_case_name, self.evidence_name
        )
        os.makedirs(self.scratch_dir, exist_ok=True)
        self.parquet_dir = os.path.join(self.scratch_dir, "parquet")
        os.makedirs(self.parquet_dir, exist_ok=True)
        self.os_type = self._detect_os()

    def _detect_os(self):
        """Detect the OS type of the mounted evidence."""
        print(f"[*] Detecting OS for {self.mount_path}...")

        # Check for Windows
        output, _ = self.orchestrator.execute(f"ls {self.mount_path}")
        if "Windows" in output or "WINDOWS" in output:
            print("[+] Detected OS: Windows")
            return "windows"

        # Check for Linux
        if "etc" in output and "var" in output and "bin" in output:
            print("[+] Detected OS: Linux")
            return "linux"

        print("[*] OS not recognized. Using generic profile.")
        return "generic"

    def run_triage(self):
        """Run the triage process based on the detected OS."""
        print(f"[*] Starting triage for {self.evidence_name} ({self.os_type})...")

        # 1. Generic Filesystem Timeline (Works for all OS)
        self._extract_fs_timeline()

        # 2. OS-Specific Artifacts
        if self.os_type == "windows":
            self._extract_windows_artifacts()
        elif self.os_type == "linux":
            self._extract_linux_artifacts()

        # 3. Convert all CSVs to Parquet
        self._convert_to_parquet()

    def _extract_fs_timeline(self):
        """Extract filesystem timeline using fls and mactime."""
        print("[*] Extracting filesystem timeline...")

        raw_image = f"/mnt/ewf/{self.real_case_name}/{self.evidence_name}/ewf1"

        cmd = f"bash -c 'mkdir -p /scratch/{self.real_case_name}/{self.evidence_name} && fls -r -m / {raw_image} > /scratch/{self.real_case_name}/{self.evidence_name}/bodyfile.txt'"
        self.orchestrator.execute(cmd)

        cmd = f"bash -c 'mactime -b /scratch/{self.real_case_name}/{self.evidence_name}/bodyfile.txt -z UTC -d > /scratch/{self.real_case_name}/{self.evidence_name}/fs_timeline.csv'"
        self.orchestrator.execute(cmd)

    def _extract_windows_artifacts(self):
        """Extract Windows-specific artifacts (Registry, EVTX, MFT) into a unified timeline."""
        print("[*] Extracting Windows artifacts...")

        # Paths for Plaso
        plaso_storage = (
            f"/scratch/{self.real_case_name}/{self.evidence_name}/artifacts.plaso"
        )
        jsonl_output = (
            f"/scratch/{self.real_case_name}/{self.evidence_name}/artifacts.jsonl"
        )

        # 1. Targeted Registry Artifacts
        print(
            "[*] Parsing targeted Registry artifacts (RunKeys, Services, UserAssist, ShimCache)..."
        )
        reg_artifacts = (
            "WindowsRunKeys,WindowsServices,WindowsUserAssist,WindowsAppCompatCache"
        )
        cmd = f"log2timeline.py --artifact_filters '{reg_artifacts}' --storage_file {plaso_storage} {self.mount_path}"
        self.orchestrator.execute(cmd)

        # 2. Targeted Event Logs
        # Discover Event Log location (XP vs Win7+)
        evtx_paths = [
            f"{self.mount_path}/Windows/System32/winevt/Logs/Security.evtx",
            f"{self.mount_path}/Windows/System32/winevt/Logs/System.evtx",
            f"{self.mount_path}/WINDOWS/system32/config/SecEvent.Evt",
            f"{self.mount_path}/WINDOWS/system32/config/SysEvent.Evt",
        ]

        for evtx_path in evtx_paths:
            # Check if file exists inside container
            output, code = self.orchestrator.execute(f"ls {evtx_path}")
            if code == 0:
                print(f"[*] Parsing Event Log: {evtx_path}")
                # Append to the same Plaso storage
                cmd = f"log2timeline.py --parsers 'winevtx,winevt' --storage_file {plaso_storage} {evtx_path}"
                self.orchestrator.execute(cmd)

        # 3. Export to JSONL for DuckDB ingestion
        print("[*] Exporting unified artifacts to JSONL...")
        cmd = f"psort.py -o json_line -w {jsonl_output} {plaso_storage}"
        self.orchestrator.execute(cmd)

        # MFT
        print("[*] Extracting MFT...")
        raw_image = f"/mnt/ewf/{self.real_case_name}/{self.evidence_name}/ewf1"
        # We need to find the offset again or use the one from mount
        output, _ = self.orchestrator.execute("mount")
        offset = 0
        for line in output.splitlines():
            if self.mount_path in line and "offset=" in line:
                match = re.search(r"offset=(\d+)", line)
                if match:
                    offset = int(match.group(1)) // 512

        if offset > 0:
            self.orchestrator.execute(
                f"bash -c 'icat -o {offset} {raw_image} 0 > /scratch/{self.real_case_name}/{self.evidence_name}/MFT'"
            )
        else:
            self.orchestrator.execute(
                f"bash -c 'icat {raw_image} 0 > /scratch/{self.real_case_name}/{self.evidence_name}/MFT'"
            )

    def _extract_linux_artifacts(self):
        """Extract Linux-specific artifacts."""
        print("[*] Extracting Linux artifacts...")
        linux_dir = os.path.join(self.scratch_dir, "linux")
        os.makedirs(linux_dir, exist_ok=True)
        self.orchestrator.execute(
            f"mkdir -p /scratch/{self.real_case_name}/{self.evidence_name}/linux"
        )

        files = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/group",
            "/var/log/auth.log",
            "/var/log/syslog",
        ]
        for f in files:
            self.orchestrator.execute(
                f"cp {self.mount_path}{f} /scratch/{self.real_case_name}/{self.evidence_name}/linux/ 2>/dev/null || true"
            )

    def _convert_to_parquet(self):
        """Convert all extracted artifacts (CSV and JSONL) to Parquet using DuckDB."""
        print("[*] Converting extracted artifacts to Parquet...")
        con = duckdb.connect()

        # 1. FS Timeline (CSV)
        timeline_csv = os.path.join(self.scratch_dir, "fs_timeline.csv")
        if os.path.exists(timeline_csv):
            parquet_path = os.path.join(self.parquet_dir, "fs_timeline.parquet")
            print(f"[*] Converting fs_timeline.csv to Parquet...")
            try:
                con.execute(
                    f"COPY (SELECT * FROM read_csv_auto('{timeline_csv}', ignore_errors=true)) TO '{parquet_path}' (FORMAT PARQUET)"
                )
                print(f"[+] Created {parquet_path}")
            except Exception as e:
                print(f"[-] Failed to convert timeline: {e}")

        # 2. Unified Artifacts (JSONL from Plaso)
        artifacts_jsonl = os.path.join(self.scratch_dir, "artifacts.jsonl")
        if os.path.exists(artifacts_jsonl):
            parquet_path = os.path.join(self.parquet_dir, "artifacts_timeline.parquet")
            print(f"[*] Converting artifacts.jsonl to Parquet...")
            try:
                # Use read_json_auto for JSONL
                con.execute(
                    f"COPY (SELECT * FROM read_json_auto('{artifacts_jsonl}')) TO '{parquet_path}' (FORMAT PARQUET)"
                )
                print(f"[+] Created {parquet_path}")
            except Exception as e:
                print(f"[-] Failed to convert unified artifacts: {e}")

        # 3. Other CSVs (if any)
        for file in os.listdir(self.scratch_dir):
            if file.endswith(".csv") and file != "fs_timeline.csv":
                csv_path = os.path.join(self.scratch_dir, file)
                parquet_path = os.path.join(
                    self.parquet_dir, file.replace(".csv", ".parquet")
                )
                print(f"[*] Converting {file} to Parquet...")
                try:
                    con.execute(
                        f"COPY (SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=true)) TO '{parquet_path}' (FORMAT PARQUET)"
                    )
                    print(f"[+] Created {parquet_path}")
                except Exception as e:
                    print(f"[-] Failed to convert {file}: {e}")


def main():
    if not os.path.exists("scratch/container_id.txt"):
        print("[-] Container ID not found. Run init_case.py first.")
        sys.exit(1)

    with open("scratch/container_id.txt", "r") as f:
        container_id = f.read().strip()

    orchestrator = SIFTOrchestrator()
    orchestrator.container = orchestrator.client.containers.get(container_id)

    # We need to find what's mounted. New path is /mnt/cases/<case_name>/<evidence_name>
    output, _ = orchestrator.execute("ls -R /mnt/cases")
    # This is a bit complex to parse. Let's do it better.
    # /mnt/cases:
    # case1
    # case2
    #
    # /mnt/cases/case1:
    # img1
    # img2

    output, _ = orchestrator.execute("find /mnt/cases -maxdepth 2 -mindepth 2 -type d")
    mounts = output.splitlines()

    for mount in mounts:
        if mount.strip():
            mount_path = mount.strip()
            extractor = TriageExtractor(orchestrator, container_id, mount_path)
            extractor.run_triage()


if __name__ == "__main__":
    main()
