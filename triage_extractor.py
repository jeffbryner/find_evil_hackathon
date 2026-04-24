import os
import sys
import duckdb
import re
import argparse
import subprocess
import logging
from concurrent.futures import ThreadPoolExecutor
from helpers.sift_tools import SIFTOrchestrator

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)


class TriageExtractor:
    def __init__(self, orchestrator, container_id, mount_path, case_name=None):
        self.orchestrator = orchestrator
        self.container_id = container_id
        self.mount_path = mount_path
        # mount_path is /mnt/cases/<case_name>/<evidence_name>
        # OR /cases/images/<evidence_name> for memory images
        parts = self.mount_path.split("/")
        self.evidence_name = parts[-1]
        self.real_case_name = case_name if case_name else parts[-2]
        self.scratch_dir = os.path.join(
            os.getcwd(), "scratch", self.real_case_name, self.evidence_name
        )
        os.makedirs(self.scratch_dir, exist_ok=True)
        self.parquet_dir = os.path.join(self.scratch_dir, "parquet")
        os.makedirs(self.parquet_dir, exist_ok=True)
        self.os_type = self._detect_os()

    def _detect_os(self):
        """Detect the OS type of the mounted evidence."""
        logging.info(f"[*] Detecting OS for {self.mount_path}...")

        # Check for Memory Image
        if "memory" in self.evidence_name.lower():
            logging.info("[+] Detected OS: Memory Image")
            return "memory"

        # Check for Windows
        output, _ = self.orchestrator.execute(f"ls {self.mount_path}")
        if "Windows" in output or "WINDOWS" in output:
            logging.info("[+] Detected OS: Windows")
            return "windows"

        # Check for Linux
        if "etc" in output and "var" in output and "bin" in output:
            logging.info("[+] Detected OS: Linux")
            return "linux"

        logging.info("[*] OS not recognized. Using generic profile.")
        return "generic"

    def run_triage(self):
        """Run the triage process based on the detected OS."""
        logging.info(
            f"[*] Starting triage for {self.evidence_name} ({self.os_type})..."
        )

        # Handle Memory Image triage separately
        if self.os_type == "memory":
            self._extract_memory_artifacts()
            self._convert_to_parquet()
            return

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
        logging.info("[*] Extracting filesystem timeline...")

        raw_image = f"/mnt/ewf/{self.real_case_name}/{self.evidence_name}/ewf1"

        cmd = f"bash -c 'mkdir -p /scratch/{self.real_case_name}/{self.evidence_name} && fls -r -m / {raw_image} > /scratch/{self.real_case_name}/{self.evidence_name}/bodyfile.txt'"
        self.orchestrator.execute(cmd)

        cmd = f"bash -c 'mactime -b /scratch/{self.real_case_name}/{self.evidence_name}/bodyfile.txt -z UTC -d > /scratch/{self.real_case_name}/{self.evidence_name}/fs_timeline.csv'"
        self.orchestrator.execute(cmd)

    def _extract_windows_artifacts(self):
        """Extract Windows-specific artifacts (Registry, EVTX, MFT) into a unified timeline."""
        logging.info("[*] Extracting Windows artifacts...")

        # Paths for Plaso
        plaso_storage = (
            f"/scratch/{self.real_case_name}/{self.evidence_name}/artifacts.plaso"
        )
        jsonl_output = (
            f"/scratch/{self.real_case_name}/{self.evidence_name}/artifacts.jsonl"
        )

        # 1. Targeted Registry and Event Log Artifacts
        logging.info(
            "[*] Parsing targeted Registry and Event Log artifacts in a single pass..."
        )
        artifacts = (
            "WindowsRunKeys,WindowsServices,WindowsUserAssist,WindowsAppCompatCache,"
            "WindowsEventLogSecurity,WindowsEventLogSystem, WindowsXMLEventLogSecurity,WindowsXMLEventLogSystem,WindowsPrefetchFiles"
        )
        cmd = f"log2timeline.py --artifact_filters '{artifacts}' --storage_file {plaso_storage} {self.mount_path}"
        self.orchestrator.execute(cmd)

        # 2. Export to JSONL for DuckDB ingestion
        logging.info("[*] Exporting unified artifacts to JSONL...")
        cmd = f"psort.py -o json_line -w {jsonl_output} {plaso_storage}"
        self.orchestrator.execute(cmd)

        # MFT
        logging.info("[*] Extracting MFT...")
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
        logging.info("[*] Extracting Linux artifacts...")
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

    def _extract_memory_artifacts(self):
        """Extract artifacts from a memory image using Volatility 3."""
        logging.info("[*] Extracting memory artifacts...")

        # Volatility 3 commands
        # We run silently (-q), offline (--offline), and output jsonl (-r jsonl)
        plugins = [
            ("windows.netscan.NetScan", "netscan.jsonl"),
            ("windows.pslist.PsList", "pslist.jsonl"),
        ]

        for plugin, output_file in plugins:
            logging.info(f"[*] Running Volatility plugin: {plugin}...")
            output_path = (
                f"/scratch/{self.real_case_name}/{self.evidence_name}/{output_file}"
            )
            cmd = f"bash -c 'vol -f {self.mount_path} -q --offline -r jsonl {plugin} > {output_path}'"
            self.orchestrator.execute(cmd)

    def _convert_to_parquet(self):
        """Convert all extracted artifacts (CSV and JSONL) to Parquet using DuckDB."""
        logging.info("[*] Converting extracted artifacts to Parquet...")
        con = duckdb.connect()

        # 1. FS Timeline (CSV)
        timeline_csv = os.path.join(self.scratch_dir, "fs_timeline.csv")
        if os.path.exists(timeline_csv):
            parquet_path = os.path.join(self.parquet_dir, "fs_timeline.parquet")
            logging.info(f"[*] Converting fs_timeline.csv to Parquet...")
            try:
                # Extract Big Five + file_name_lower, pack the rest into JSON 'details'
                sql = f"""
                COPY (
                    SELECT 
                        try_strptime("Date", '%a %b %d %Y %H:%M:%S') AS timestamp,
                        'fs:mactime' AS data_type,
                        'mactime' AS parser,
                        "File Name" AS message,
                        lower("File Name") AS file_name_lower,
                        to_json({{
                            'Size': "Size", 
                            'Type': "Type", 
                            'Mode': "Mode", 
                            'UID': "UID", 
                            'GID': "GID", 
                            'Meta': "Meta"
                        }}) AS details
                    FROM read_csv_auto('{timeline_csv}', ignore_errors=true)
                ) TO '{parquet_path}' (FORMAT PARQUET)
                """
                con.execute(sql)
                logging.info(f"[+] Created {parquet_path}")
            except Exception as e:
                logging.error(f"[-] Failed to convert timeline: {e}")

        # 2. Unified Artifacts (JSONL from Plaso)
        artifacts_jsonl = os.path.join(self.scratch_dir, "artifacts.jsonl")
        if os.path.exists(artifacts_jsonl):
            parquet_path = os.path.join(self.parquet_dir, "artifacts_timeline.parquet")
            logging.info(f"[*] Converting artifacts.jsonl to Parquet...")
            try:
                # Use read_json_objects to avoid schema bloat, extract Big Five, pack rest into JSON 'details'
                sql = f"""
                COPY (
                    SELECT 
                        to_timestamp(CAST(json->>'timestamp' AS BIGINT) / 1000000) AT TIME ZONE 'UTC' AS timestamp,
                        json->>'data_type' AS data_type,
                        json->>'parser' AS parser,
                        json->>'message' AS message,
                        lower(COALESCE(json->>'filename', json->>'display_name')) AS file_name_lower,
                        json_merge_patch(json, '{{"timestamp": null, "data_type": null, "parser": null, "message": null}}'::JSON) AS details
                    FROM read_json_objects('{artifacts_jsonl}')
                ) TO '{parquet_path}' (FORMAT PARQUET)
                """
                con.execute(sql)
                logging.info(f"[+] Created {parquet_path}")
            except Exception as e:
                logging.error(f"[-] Failed to convert unified artifacts: {e}")

        # 3. Other CSVs (if any)
        for file in os.listdir(self.scratch_dir):
            if file.endswith(".csv") and file != "fs_timeline.csv":
                csv_path = os.path.join(self.scratch_dir, file)
                parquet_path = os.path.join(
                    self.parquet_dir, file.replace(".csv", ".parquet")
                )
                logging.info(f"[*] Converting {file} to Parquet...")
                try:
                    con.execute(
                        f"COPY (SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=true)) TO '{parquet_path}' (FORMAT PARQUET)"
                    )
                    logging.info(f"[+] Created {parquet_path}")
                except Exception as e:
                    logging.error(f"[-] Failed to convert {file}: {e}")

        # 4. Volatility JSONL output
        for file in ["pslist.jsonl", "netscan.jsonl"]:
            jsonl_path = os.path.join(self.scratch_dir, file)
            if os.path.exists(jsonl_path):
                parquet_name = f"memory_{file.replace('.jsonl', '.parquet')}"
                parquet_path = os.path.join(self.parquet_dir, parquet_name)
                logging.info(f"[*] Converting {file} to Parquet...")
                try:
                    # Volatility JSONL output is very structured and clean
                    con.execute(
                        f"COPY (SELECT * FROM read_json_auto('{jsonl_path}')) TO '{parquet_path}' (FORMAT PARQUET)"
                    )
                    logging.info(f"[+] Created {parquet_path}")
                except Exception as e:
                    logging.error(f"[-] Failed to convert {file}: {e}")


def run_triage_worker(orchestrator, container_id, mount_path, case_name):
    """Worker function for ThreadPoolExecutor."""
    try:
        extractor = TriageExtractor(orchestrator, container_id, mount_path, case_name)
        extractor.run_triage()
    except Exception as e:
        logging.error(f"[-] Error during triage for {mount_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Extract triage artifacts.")
    parser.add_argument("--case", required=True, help="Name of the forensic case")
    parser.add_argument(
        "--evidence", nargs="+", help="Specific evidence names to process"
    )
    parser.add_argument(
        "--all", action="store_true", help="Process all mounted evidence for the case"
    )
    parser.add_argument(
        "--background", action="store_true", help="Run extraction in the background"
    )

    args = parser.parse_args()

    if args.background:
        # Re-run the current script without the --background flag
        cmd = [sys.executable, sys.argv[0], "--case", args.case]
        if args.all:
            cmd.append("--all")
        elif args.evidence:
            cmd.extend(["--evidence"] + args.evidence)

        log_dir = os.path.join("scratch", args.case)
        os.makedirs(log_dir, exist_ok=True)
        log_file = os.path.join(log_dir, "triage.log")

        logging.info(
            f"[*] Launching triage extraction in background for case: {args.case}"
        )
        with open(log_file, "a") as f:
            f.write(f"\n--- Triage started at {os.popen('date').read().strip()} ---\n")
            subprocess.Popen(
                cmd, stdout=f, stderr=subprocess.STDOUT, start_new_session=True
            )

        logging.info(
            f"[+] Background process started. Monitor progress with: tail -f {log_file}"
        )
        sys.exit(0)

    # Synchronous processing
    if not os.path.exists("scratch/container_id.txt"):
        logging.error("[-] Container ID not found. Run init_case.py first.")
        sys.exit(1)

    with open("scratch/container_id.txt", "r") as f:
        container_id = f.read().strip()

    orchestrator = SIFTOrchestrator()
    orchestrator.container = orchestrator.client.containers.get(container_id)

    # Discover mounts for the case
    case_path = f"/mnt/cases/{args.case}"
    output, _ = orchestrator.execute(
        f"find {case_path} -maxdepth 1 -mindepth 1 -type d"
    )
    available_mounts = output.splitlines()

    target_mounts = []
    if args.all:
        target_mounts = available_mounts
    elif args.evidence:
        for ev in args.evidence:
            # Check if it's a directory mount
            expected_path = f"{case_path}/{ev}"
            if expected_path in available_mounts:
                target_mounts.append(expected_path)
            elif "memory" in ev.lower():
                # For memory images, we assume they are in /cases/images/
                target_mounts.append(f"/cases/images/{ev}")
            else:
                logging.error(
                    f"[-] Evidence '{ev}' not found mounted at {expected_path}"
                )
    else:
        logging.error("[-] Must specify --all or --evidence <names>")
        sys.exit(1)

    if not target_mounts:
        logging.error("[-] No valid mounts found to process.")
        sys.exit(1)

    logging.info(
        f"[*] Processing {len(target_mounts)} evidence images for case: {args.case}"
    )

    # Parallel execution
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 4) as executor:
        for mount in target_mounts:
            executor.submit(
                run_triage_worker,
                orchestrator,
                container_id,
                mount.strip(),
                args.case,
            )

    logging.info("[+] Triage extraction complete.")


if __name__ == "__main__":
    main()
