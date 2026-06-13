---
name: analyze-network-traffic
description: Standard operating procedure for analyzing network traffic and packet captures (PCAP/PCAPNG) using a hybrid funnel of DuckDB SQL querying and containerized tshark/tcpdump. Use when asked to investigate network activity, analyze packet captures, perform network-based threat hunting, trace web/mail traffic, or carve files/credentials from PCAPs.
---

# Analyze Network Traffic

This skill provides the technical documentation, standard operating procedures, and command recipes for investigating network traffic and packet captures (PCAPs). 

## The Hybrid Funnel Methodology

Network forensic investigations are most efficient when executed as a "Hybrid Funnel":
1. **Phase 1: High-Speed SQL Triage (DuckDB/Parquet)**: Use SQL queries against the parsed `packets.parquet` table to perform a macro-level sweep, profile protocols, identify top talkers, and locate targeted time windows.
2. **Phase 2: Deep-Dive Packet Inspection (SIFT + tcpdump/tshark)**: Pivot to containerized command-line utilities to reassemble TCP streams, extract application headers, inspect raw payloads, and carve transmitted files.

---
## Prerequisites
- Ensure the PCAP file has been parsed into a Parquet format using `uv run helpers/pcap_to_parquet.py` and is accessible in the case's `scratch/` directory: `cases/<CASEID>/scratch/<pcap_image_name>/parquet/packets.parquet`.

## Phase 1: High-Speed SQL Triage (DuckDB)

Use `uv run helpers/query_parquet.py` to analyze parsed packet metadata. If the schema is unknown, run with `--schema` first.

### 1. Protocol Distribution Baseline
Identify the dominant traffic profiles in the capture to understand the network's behavior.
```sql
SELECT protocol, COUNT(*) as packet_count 
FROM packets 
GROUP BY protocol 
ORDER BY packet_count DESC;
```

### 2. Identifying "Top Talkers" (Active IPs)
Map out local and external hosts by aggregating packets sent and received.
```sql
SELECT ip, SUM(sent) as sent_packets, SUM(rcvd) as rcvd_packets 
FROM (
    SELECT source_ip as ip, COUNT(*) as sent, 0 as rcvd FROM packets GROUP BY source_ip 
    UNION ALL 
    SELECT dest_ip as ip, 0 as sent, COUNT(*) as rcvd FROM packets GROUP BY dest_ip
) 
GROUP BY ip 
ORDER BY (sent_packets + rcvd_packets) DESC;
```

### 3. Targeted Time-Window Sweep
Narrow down traffic to a specific timeframe surrounding an known incident (e.g., when a threat email was sent).
```sql
SELECT timestamp, source_ip, dest_ip, protocol, info 
FROM packets 
WHERE timestamp BETWEEN 'YYYY-MM-DDTHH:MM:SS' AND 'YYYY-MM-DDTHH:MM:SS'
ORDER BY timestamp ASC;
```

### 4. HTTP Hostname and URL Profiling
Extract visited hostnames or specific search queries from the `info` column.
```sql
SELECT regexp_extract(info, 'Host: ([a-zA-Z0-9.-]+)', 1) as host, COUNT(*) as count 
FROM packets 
WHERE protocol = 'HTTP' 
GROUP BY host 
ORDER BY count DESC;
```

---

## Phase 2: Deep-Dive Packet Inspection (SIFT + tshark/tcpdump)

When raw payload analysis, stream reassembly, or protocol decoding is required, execute standard network utilities inside the SIFT Docker container.

### 1. Running tshark/tcpdump in the SIFT Container
Standard SIFT container mounts the sourc images in the  `/case/images/` directory. 
The host machine scratch directory is mounted at `/scratch/` for outputting extracted files, decoded payloads, or intermediate text dumps.
Always map paths relative to the container mount points.

```bash
# Example: Running tshark on a PCAP in the mounted case directory
uv run helpers/start_case_container.py --case <CASEID>
docker exec <CASEID> tshark -r /case/images/<filename.pcap> -Y "http.request" -c 10
```

### 2. tshark Query Recipes

#### A. Follow and Reassemble TCP Streams
Reassemble entire conversational streams to view full HTTP transactions, email bodies, or interactive sessions.
```bash
# Step 1: Find the stream ID for a targeted packet using a display filter
tshark -r <pcap_path> -Y "http.request.uri contains \"submit\"" -T fields -e tcp.stream

# Step 2: Follow the specific TCP stream (e.g., stream 12) in ASCII format
tshark -r <pcap_path> -q -z follow,tcp,ascii,12
```

#### B. Extract HTTP POST Payloads and Form Data
Directly extract submitted form fields, passwords, or message bodies from HTTP POST requests.
```bash
tshark -r <pcap_path> -Y "http.request.method == POST" -T fields -e http.file_data
```

#### C. Profile Browser User-Agents
Identify the exact browser and operating system profiles active on the suspect IP to correlate sessions or detect VM usage.
```bash
tshark -r <pcap_path> -Y "http.user_agent and ip.addr == <IP>" -T fields -e http.user_agent | sort -u
```

#### D. Extract DNS Queries
Map domain name resolutions to identify command-and-control (C2) domains, lookups for staging sites, or data exfiltration via DNS.
```bash
tshark -r <pcap_path> -Y "dns.flags.response == 0" -T fields -e dns.qry.name | sort -u
```

#### E. Filter by Specific Credentials or Keywords
Search raw packet payloads for usernames, email addresses, or specific threat keywords.
```bash
tshark -r <pcap_path> -Y "frame contains \"@gmail.com\"" -T fields -e ip.src -e ip.dst -e http.user_agent -e http.request.uri
```

---

## Phase 3: File Carving and Object Extraction

To recover documents, executables, or scripts transferred over unencrypted protocols (HTTP, FTP, SMB, SMTP), use automated carving features.

### 1. Automated HTTP Object Carving
Export all files transferred over HTTP directly to a target scratch directory.
```bash
# Run inside the SIFT container to carve HTTP objects
tshark -r /case/images/evidence.pcap --export-objects http,/scratch/extracted_files/
```

### 2. Carving SMTP/Email Attachments
Extract raw MIME email attachments from SMTP streams.
```bash
# Reassemble the SMTP stream containing the attachment
tshark -r <pcap_path> -q -z follow,tcp,ascii,<stream_id> > /scratch/raw_email.eml
# Use standard email parsers to extract attachments from the .eml file
```

---

## Investigative Workflow Strategy

1. **Baseline First**: Never jump straight into raw PCAP hex dumps. Run a protocol and top talkers sweep first to map the local topology.
2. **Isolate NAT and VM Environments**: Watch for multiple distinct User-Agent strings (e.g., a Mac OS X User-Agent and a Windows XP User-Agent) sharing the same IP address. This indicates a physical host running virtual machines in NAT mode.
3. **Correlate Time Windows**: Threat actors often log into personal accounts (Gmail, Facebook, Yahoo) immediately before or after sending malicious traffic. Map a 15-minute window around the threat timestamp to capture personal login sessions sharing the same IP and User-Agent.
4. **Preserve Integrity**: Never modify the source PCAP file. Always output carved files and text streams to the case's `scratch/` directory.
