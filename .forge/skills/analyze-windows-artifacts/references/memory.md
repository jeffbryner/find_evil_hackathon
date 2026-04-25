# Memory Analysis (Volatility 3)

Analyze a RAM image to find live activity and hidden threats using **Volatility 3**.

> **CRITICAL**: This environment uses Volatility 3. Do NOT use Volatility 2 syntax (e.g., `--profile` is NOT used).

## Tools

| Tool | Binary | Purpose |
|------|--------|---------|
| Volatility 3 | `vol` | Process, network, registry, injection, and artifact extraction |

## Volatility 3 Usage Rules
1. **Plugin Names**: Always use the full plugin name (e.g., `windows.pslist.PsList` or `windows.pslist`).
2. **PID Filtering**: Multiple PIDs MUST be space-separated, NOT comma-separated (e.g., `--pid 123 456`).
3. **Output Formatting**: Use `-r jsonl` to output results in jsonl format for easier ingestion into DuckDB.
4. **Symbol Tables**: Volatility 3 automatically handles symbols; you do not need to specify a profile.
5. **Reduce noise**: Always run silently (-q), offline (--offline), and output jsonl (-r jsonl)
6. **Import to parquet**: Import as duckDB accessible parquet via: COPY (SELECT * FROM read_json_auto('{jsonl_path}')) TO '{parquet_path}' (FORMAT PARQUET)

## 1. Process Enumeration
- **`windows.pslist.PsList`**: Walk the linked list of processes (fast, but misses hidden).
- **`windows.psscan.PsScan`**: Scan for process pool tags (finds hidden and exited processes).
- **`windows.pstree.PsTree`**: Visualize parent-child relationships.

```bash
# Run psscan via docker and output to CSV
docker exec $(cat scratch/container_id.txt) vol \
  -f /evidence/memdump.mem -r csv windows.psscan > scratch/psscan.csv
```

## 2. Network Connections
- **`windows.netscan.NetScan`**: Find active and closed network connections (TCP/UDP).

```bash
docker exec $(cat scratch/container_id.txt) vol \
  -f /evidence/memdump.mem -r csv windows.netscan > scratch/netscan.csv
```

## 3. Code Injection & Malware
- **`windows.malware.malfind.Malfind`**: Find RWX memory regions that look like injected code.
- **`windows.vadinfo.VadInfo`**: Detailed information about Virtual Address Descriptors.

```bash
# Find injected code and dump the suspicious regions
docker exec $(cat scratch/container_id.txt) vol \
  -f /evidence/memdump.mem windows.malfind --dump
```

## 4. Extraction & Dumping
- **`windows.dumpfiles.DumpFiles`**: Extract a file from the memory cache.
- **`windows.pslist.PsList --dump`**: Dump a process executable.

```bash
# Dump a specific process by PID (space-separated for multiple)
docker exec $(cat scratch/container_id.txt) vol \
  -f /evidence/memdump.mem windows.pslist --pid 1234 --dump
```

## 5. Registry in Memory
- **`windows.registry.hivelist.HiveList`**: List registry hives in memory.
- **`windows.registry.printkey.PrintKey`**: Print specific registry keys from memory.

```bash
docker exec $(cat scratch/container_id.txt) vol \
  -f /evidence/memdump.mem windows.registry.printkey --key "Software\Microsoft\Windows\CurrentVersion\Run"
```
