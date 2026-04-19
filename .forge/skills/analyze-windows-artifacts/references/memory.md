# Memory Analysis (Volatility 3)

Analyze a RAM image to find live activity and hidden threats.


## Tools

| Tool | Binary | Purpose |
|------|--------|---------|
| Volatility 3 | `vol.py or just vol` | Process, network, registry, injection, and artifact extraction |



## 1. Process Enumeration
- **`windows.pslist`**: Walk the linked list of processes (fast, but misses hidden).
- **`windows.psscan`**: Scan for process pool tags (finds hidden and exited processes).
- **`windows.pstree`**: Visualize parent-child relationships.

```bash
# Run psscan via docker (assuming memory image is in scratch/)
docker exec $(cat scratch/container_id.txt) /opt/volatility3-2.20.0/vol.py \
  -f /evidence/scratch/memdump.mem windows.psscan
```

## 2. Network Connections
- **`windows.netscan`**: Find active and closed network connections.

```bash
docker exec $(cat scratch/container_id.txt) /opt/volatility3-2.20.0/vol.py \
  -f /evidence/scratch/memdump.mem windows.netscan
```

## 3. Code Injection
- **`windows.malfind`**: Find RWX memory regions that look like injected code.

```bash
docker exec $(cat scratch/container_id.txt) /opt/volatility3-2.20.0/vol.py \
  -f /evidence/scratch/memdump.mem windows.malfind --dump
```

## 4. Extraction
- **`windows.dumpfiles`**: Extract a file from the memory cache (using virtaddr from filescan).
- **`windows.pslist --dump`**: Dump a process executable.

## 5. Memory Baselining
Compare the image against a known-good baseline to surface anomalies.

```bash
docker exec $(cat scratch/container_id.txt) python3 /opt/memory-baseliner/baseline.py \
  -proc -i /evidence/scratch/memdump.mem --loadbaseline --jsonbaseline /path/to/baseline.json
```
