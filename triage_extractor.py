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
    def __init__(self, orchestrator, container_id, mount_path, case_name):
        self.orchestrator = orchestrator
        self.container_id = container_id
        self.mount_path = mount_path
        # mount_path is /mnt/cases/<case_name>/<evidence_name>
        # OR /cases/images/<evidence_name> for memory images
        parts = self.mount_path.split("/")
        self.evidence_name = parts[-1]
        self.real_case_name = case_name
        # Host-side scratch dir: cases/<case_name>/scratch/<evidence_name>
        self.scratch_dir = os.path.join(
            os.getcwd(), "cases", self.real_case_name, "scratch", self.evidence_name
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
        output, _ = self.orchestrator.execute(
            f"target-info -qJ /case/images/{self.evidence_name}"
        )
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

        # In container
        # Evidence source images are in /case/images/
        # mounts at /mnt/cases/<case_name>/<evidence_basename>
        # And ewfmount at /mnt/ewf/<case_name>/<evidence_basename>

        raw_image = f"/mnt/ewf/{self.real_case_name}/{self.evidence_name}/ewf1"

        # Check for partition offset
        offset_file = f"/scratch/{self.evidence_name}/offset.txt"
        offset_output, offset_code = self.orchestrator.execute(
            f"cat {offset_file} 2>/dev/null || true"
        )
        offset_output = offset_output.strip()

        offset_cmd = ""
        if offset_code == 0 and offset_output.isdigit():
            offset_val = int(offset_output)
            if offset_val > 0:
                logging.info(
                    f"[+] Found custom partition sector offset for fls: {offset_val}"
                )
                offset_cmd = f"-o {offset_val} "
            else:
                logging.info(
                    "[*] Custom partition sector offset is 0, running fls without custom offset"
                )
        else:
            logging.info(
                "[*] No custom partition offset found, running fls without custom offset"
            )

        # Inside container, /scratch is cases/<case_name>/scratch
        cmd = f"bash -c 'mkdir -p /scratch/{self.evidence_name} && fls -r -m / {offset_cmd}{raw_image} > /scratch/{self.evidence_name}/bodyfile.txt'"
        self.orchestrator.execute(cmd)

        # Run mactime replacement LOCALLY for speed and to avoid timeouts
        bodyfile_local = os.path.join(self.scratch_dir, "bodyfile.txt")
        timeline_local = os.path.join(self.scratch_dir, "fs_timeline.csv")
        logging.info(f"[*] Running local mactime replacement on {bodyfile_local}...")

        mactime_cmd = [
            "uv",
            "run",
            "helpers/mactime.py",
            "-b",
            bodyfile_local,
            "-z",
            "UTC",
            "-d",
        ]
        try:
            with open(timeline_local, "w") as f:
                subprocess.run(mactime_cmd, stdout=f, check=True)
            logging.info(f"[+] Filesystem timeline saved to {timeline_local}")
        except subprocess.CalledProcessError as e:
            logging.error(f"[-] Local mactime failed: {e}")

    def _extract_windows_artifacts(self):
        """Extract Windows-specific artifacts (Registry, EVTX, MFT) into a unified timeline."""
        logging.info("[*] Extracting Windows artifacts...")

        # Paths for Plaso /  parquet files (view point inside container)
        parquet_storage = (
            f"/scratch/{self.evidence_name}/parquet/artifacts_timeline.parquet"
        )
        plaso_storage = f"/scratch/{self.evidence_name}/plaso.artifacts.tmp"

        # 1. Targeted plaso Artifacts
        logging.info("[*] Parsing targeted artifacts from plaso to parquet")
        # for speed, don't spend time hashing, use a filter file, no status view
        cmd = f"psteal_parquet.py --hasher_file_size_limit 10 --status-view none --single_process -f /home/sansforensics/psteal_filter.yaml -w {parquet_storage} --source {self.mount_path} --storage-file {plaso_storage}"
        self.orchestrator.execute(cmd)

        # browser history
        logging.info("[*] Extracting browser history...")
        cmd = f"target-query {self.mount_path} -f browser.history | rdump_to_parquet.py /scratch/{self.evidence_name}/parquet/browser_history.parquet"
        self.orchestrator.execute(cmd)

        # MFT
        # logging.info("[*] Extracting MFT...")
        # raw_image = f"/mnt/ewf/{self.real_case_name}/{self.evidence_name}/ewf1"
        # output, _ = self.orchestrator.execute("mount")
        # offset = 0
        # for line in output.splitlines():
        #     if self.mount_path in line and "offset=" in line:
        #         match = re.search(r"offset=(\d+)", line)
        #         if match:
        #             offset = int(match.group(1)) // 512

        # if offset > 0:
        #     self.orchestrator.execute(
        #         f"bash -c 'icat -o {offset} {raw_image} 0 > /scratch/{self.evidence_name}/MFT'"
        #     )
        # else:
        #     self.orchestrator.execute(
        #         f"bash -c 'icat {raw_image} 0 > /scratch/{self.evidence_name}/MFT'"
        #     )

    def _extract_linux_artifacts(self):
        """Extract Linux-specific artifacts."""
        logging.info("[*] Extracting Linux artifacts...")
        self.orchestrator.execute(f"mkdir -p /scratch/{self.evidence_name}/linux")

        files = [
            "/etc/passwd",
            "/etc/shadow",
            "/etc/group",
            "/var/log/auth.log",
            "/var/log/syslog",
        ]
        for f in files:
            self.orchestrator.execute(
                f"cp {self.mount_path}{f} /scratch/{self.evidence_name}/linux/ 2>/dev/null || true"
            )

    def _extract_memory_artifacts(self):
        """Extract artifacts from a memory image using Volatility 3 locally."""
        logging.info("[*] Extracting memory artifacts LOCALLY...")

        # Evidence path on host: cases/<case_name>/images/<evidence_name>
        local_evidence_path = os.path.join(
            "cases", self.real_case_name, "images", self.evidence_name
        )

        plugins = [
            ("windows.netscan.NetScan", "netscan.jsonl"),
            ("windows.pslist.PsList", "pslist.jsonl"),
            (
                "timeliner.Timeliner",
                "timeliner.jsonl",
            ),
        ]

        for plugin, output_file in plugins:
            logging.info(f"[*] Running Volatility plugin locally: {plugin}...")
            output_path = os.path.join(self.scratch_dir, output_file)

            # Run with uv run vol
            cmd = [
                "uv",
                "run",
                "vol",
                "-f",
                local_evidence_path,
                "-r",
                "jsonl",
                plugin,
            ]
            if plugin == "timeliner.Timeliner":
                # Filter to speed up timeliner by only scanning for processes, network connections, and common Windows artifacts, excluding MFTScan which provides limited value
                cmd.extend(
                    [
                        "--plugin-filter",
                        "PsScan",
                        "Threads",
                        "DllList",
                        "Amcache",
                        "ShimcacheMem",
                        "ScheduledTasks",
                        "NetScan",
                        "SymlinkScan",
                        "PsList",
                        "Sessions",
                        "UserAssist",
                    ]
                )
            try:
                with open(output_path, "w") as f:
                    subprocess.run(cmd, stdout=f, check=True)
                logging.info(f"[+] Volatility output saved to {output_path}")
            except subprocess.CalledProcessError as e:
                logging.error(f"[-] Volatility failed for {plugin}: {e}")

    def _convert_to_parquet(self):
        """Convert all extracted artifacts to Parquet."""
        convert_to_parquet(self.scratch_dir, self.parquet_dir)


def convert_to_parquet(scratch_dir, parquet_dir, target_file=None):
    """Convert extracted artifacts (CSV and JSONL) to Parquet using DuckDB."""
    logging.info(f"[*] Converting artifacts in {scratch_dir} to Parquet...")
    con = duckdb.connect()

    def process_file(file):
        # 1. FS Timeline (CSV)
        if file == "fs_timeline.csv":
            timeline_csv = os.path.join(scratch_dir, "fs_timeline.csv")
            if os.path.exists(timeline_csv):
                parquet_path = os.path.join(parquet_dir, "fs_timeline.parquet")
                logging.info(f"[*] Converting fs_timeline.csv to Parquet...")
                try:
                    # Check if the file has actual data lines beyond the header
                    # A non-empty fs_timeline.csv must have at least 2 lines (header + 1 data line)
                    has_data = False
                    if (
                        os.path.exists(timeline_csv)
                        and os.path.getsize(timeline_csv) > 50
                    ):
                        with open(timeline_csv, "r") as f_in:
                            lines = [f_in.readline() for _ in range(2)]
                            if len(lines) >= 2 and lines[1].strip():
                                has_data = True

                    if has_data:
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
                    else:
                        raise Exception("fs_timeline.csv has no data lines.")
                except Exception as e:
                    logging.warning(
                        f"[*] Timeline CSV is empty or invalid ({e}). Creating empty fallback Parquet..."
                    )
                    try:
                        con.execute("DROP TABLE IF EXISTS empty_timeline;")
                        con.execute("""
                            CREATE TABLE empty_timeline (
                                timestamp TIMESTAMP,
                                data_type VARCHAR,
                                parser VARCHAR,
                                message VARCHAR,
                                file_name_lower VARCHAR,
                                details VARCHAR
                            );
                        """)
                        con.execute(
                            f"COPY empty_timeline TO '{parquet_path}' (FORMAT PARQUET)"
                        )
                        logging.info(
                            f"[+] Created empty fallback Parquet at {parquet_path}"
                        )
                    except Exception as ex:
                        logging.error(
                            f"[-] Failed to create empty fallback Parquet: {ex}"
                        )

        # 2. Unified Artifacts (from .plaso storage)
        elif file == "artifacts.plaso":
            plaso_file = os.path.join(scratch_dir, "artifacts.plaso")
            if os.path.exists(plaso_file):
                parquet_path = os.path.join(parquet_dir, "artifacts_timeline.parquet")
                logging.info(f"[*] Converting artifacts.plaso to Parquet...")
                try:
                    # Use our optimized standalone script
                    helper_script = os.path.join("helpers", "plaso_to_parquet.py")
                    cmd = [sys.executable, helper_script, plaso_file, parquet_path]
                    # Log the output for visibility
                    result = subprocess.run(
                        cmd, check=True, capture_output=True, text=True
                    )
                    if result.stdout:
                        for line in result.stdout.splitlines():
                            logging.info(f"[plaso_to_parquet] {line}")
                    logging.info(f"[+] Created {parquet_path}")
                except Exception as e:
                    logging.error(f"[-] Failed to convert unified artifacts: {e}")

        # 3. Memory artifacts from Volatility (JSONL)
        elif file in ["pslist.jsonl", "netscan.jsonl", "timeliner.jsonl"]:
            jsonl_path = os.path.join(scratch_dir, file)
            if os.path.exists(jsonl_path):
                parquet_name = f"memory_{file.replace('.jsonl', '.parquet')}"
                parquet_path = os.path.join(parquet_dir, parquet_name)
                logging.info(f"[*] Converting {file} to Parquet...")
                try:
                    con.execute(
                        f"COPY (SELECT * FROM read_json_auto('{jsonl_path}')) TO '{parquet_path}' (FORMAT PARQUET)"
                    )
                    logging.info(f"[+] Created {parquet_path}")
                except Exception as e:
                    logging.error(f"[-] Failed to convert {file}: {e}")

        # 4. Other CSVs
        elif file.endswith(".csv") and not file.startswith("memory_"):
            csv_path = os.path.join(scratch_dir, file)
            parquet_path = os.path.join(parquet_dir, file.replace(".csv", ".parquet"))
            logging.info(f"[*] Converting {file} to Parquet...")
            try:
                con.execute(
                    f"COPY (SELECT * FROM read_csv_auto('{csv_path}', ignore_errors=true)) TO '{parquet_path}' (FORMAT PARQUET)"
                )
                logging.info(f"[+] Created {parquet_path}")
            except Exception as e:
                logging.error(f"[-] Failed to convert {file}: {e}")

    if target_file:
        process_file(target_file)
    else:
        # Standard flow: process all known files in scratch_dir
        files_to_check = [
            "fs_timeline.csv",
            "artifacts.plaso",
            "pslist.jsonl",
            "netscan.jsonl",
            "timeliner.jsonl",
        ]
        # Add all other CSVs found in the directory
        for f in os.listdir(scratch_dir):
            if f.endswith(".csv") and f not in files_to_check:
                files_to_check.append(f)

        for f in files_to_check:
            process_file(f)


def run_triage_worker(orchestrator, container_id, mount_path, case_name):
    """Worker function for ThreadPoolExecutor."""
    try:
        extractor = TriageExtractor(orchestrator, container_id, mount_path, case_name)
        extractor.run_triage()
    except Exception as e:
        logging.error(f"[-] Error during triage for {mount_path}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Extract triage artifacts.")
    parser.add_argument("--case", help="Name of the forensic case")
    parser.add_argument(
        "--evidence", nargs="+", help="Specific evidence names to process"
    )
    parser.add_argument(
        "--all", action="store_true", help="Process all mounted evidence for the case"
    )
    parser.add_argument(
        "--background", action="store_true", help="Run extraction in the background"
    )
    parser.add_argument(
        "--convert-only",
        action="store_true",
        help="Only run Parquet conversion on a directory",
    )
    parser.add_argument("--dir", help="Directory to process (used with --convert-only)")
    parser.add_argument(
        "--file", help="Specific file to process (used with --convert-only)"
    )

    args = parser.parse_args()

    # Standalone Parquet Conversion Flow
    if args.convert_only:
        if not args.dir and not args.file:
            logging.error("[-] --dir or --file is required with --convert-only")
            sys.exit(1)

        if args.file and not args.dir:
            # If only file is provided, derive dir from it
            if os.path.exists(args.file):
                scratch_dir = os.path.dirname(os.path.abspath(args.file))
                target_file = os.path.basename(args.file)
            else:
                logging.error(f"[-] File not found: {args.file}")
                sys.exit(1)
        else:
            scratch_dir = args.dir
            target_file = args.file

        if not scratch_dir:
            logging.error("[-] Could not determine scratch directory.")
            sys.exit(1)

        parquet_dir = os.path.join(scratch_dir, "parquet")
        os.makedirs(parquet_dir, exist_ok=True)

        convert_to_parquet(scratch_dir, parquet_dir, target_file=target_file)
        logging.info("[+] Parquet conversion complete.")
        sys.exit(0)

    if not args.case:
        logging.error("[-] --case is required")
        sys.exit(1)

    case_scratch_dir = os.path.join("cases", args.case, "scratch")
    container_id_file = os.path.join(case_scratch_dir, "container_id.txt")

    if args.background:
        cmd = [sys.executable, sys.argv[0], "--case", args.case]
        if args.all:
            cmd.append("--all")
        elif args.evidence:
            cmd.extend(["--evidence"] + args.evidence)

        os.makedirs(case_scratch_dir, exist_ok=True)
        log_file = os.path.join(case_scratch_dir, "triage.log")

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
    if not os.path.exists(container_id_file):
        logging.error(
            f"[-] Container ID not found at {container_id_file}. Run init_case.py first."
        )
        sys.exit(1)

    with open(container_id_file, "r") as f:
        container_id = f.read().strip()

    orchestrator = SIFTOrchestrator(case_name=args.case)
    orchestrator.container = orchestrator.client.containers.get(container_id)

    # Discover mounts for the case inside the container
    case_path = f"/mnt/cases/{args.case}"
    output, _ = orchestrator.execute(
        f"find {case_path} -maxdepth 1 -mindepth 1 -type d"
    )
    available_mounts = output.splitlines()

    target_mounts = []
    if args.all:
        target_mounts = available_mounts
        # Automatically discover memory images which aren't mounted like disk images
        local_images_dir = os.path.join("cases", args.case, "images")
        if os.path.exists(local_images_dir):
            for f in os.listdir(local_images_dir):
                if "memory" in f.lower() and os.path.isfile(
                    os.path.join(local_images_dir, f)
                ):
                    # Internal path should match orchestrator mapping: /case/images/filename
                    mem_path = f"/case/images/{f}"
                    if mem_path not in target_mounts:
                        target_mounts.append(mem_path)
    elif args.evidence:
        for ev in args.evidence:
            # Extract basename in case user passed a full path via tab completion
            ev_basename = os.path.basename(ev)

            # Check if it's a directory mount
            expected_path = f"{case_path}/{ev_basename}"
            if expected_path in available_mounts:
                target_mounts.append(expected_path)
            elif "memory" in ev_basename.lower():
                # For memory images, we assume they are in /case/images/
                target_mounts.append(f"/case/images/{ev_basename}")
            else:
                logging.error(
                    f"[-] Evidence '{ev_basename}' not found mounted at {expected_path}"
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
