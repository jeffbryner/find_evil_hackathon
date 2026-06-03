#!/usr/bin/env uv run python
# /// script
# dependencies = [
#   "scapy",
#   "pandas",
#   "pyarrow",
#   "duckdb",
# ]
# ///

import os
import sys
import argparse
import datetime
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

# Import scapy layers
from scapy.all import PcapReader, IP, IPv6, TCP, UDP, ICMP, ARP
from scapy.layers.dns import DNS, DNSQR, DNSRR

def extract_tls_sni(payload: bytes) -> str:
    try:
        if len(payload) < 43:
            return None
        # Check for TLS Handshake (0x16) and Client Hello (0x01)
        if payload[0] != 0x16:
            return None
        # Handshake record length
        record_len = int.from_bytes(payload[3:5], byteorder='big')
        
        # Handshake payload
        hs = payload[5:5+record_len]
        if len(hs) < 38 or hs[0] != 0x01: # 0x01 is Client Hello
            return None
        
        # Session ID
        session_id_len = hs[34]
        offset = 35 + session_id_len
        if len(hs) < offset + 2:
            return None
            
        # Cipher Suites
        cipher_suites_len = int.from_bytes(hs[offset:offset+2], byteorder='big')
        offset += 2 + cipher_suites_len
        if len(hs) < offset + 1:
            return None
            
        # Compression Methods
        comp_methods_len = hs[offset]
        offset += 1 + comp_methods_len
        if len(hs) < offset + 2:
            return None
            
        # Extensions
        extensions_len = int.from_bytes(hs[offset:offset+2], byteorder='big')
        offset += 2
        ext_end = offset + extensions_len
        
        while offset < ext_end and offset + 4 <= len(hs):
            ext_type = int.from_bytes(hs[offset:offset+2], byteorder='big')
            ext_len = int.from_bytes(hs[offset+2:offset+4], byteorder='big')
            offset += 4
            if ext_type == 0: # Server Name Indication (SNI)
                if offset + ext_len <= len(hs):
                    sni_data = hs[offset:offset+ext_len]
                    if len(sni_data) >= 5:
                        list_len = int.from_bytes(sni_data[0:2], byteorder='big')
                        name_type = sni_data[2]
                        if name_type == 0: # host_name
                            name_len = int.from_bytes(sni_data[3:5], byteorder='big')
                            if len(sni_data) >= 5 + name_len:
                                return sni_data[5:5+name_len].decode('utf-8', errors='ignore')
            offset += ext_len
    except Exception:
        pass
    return None

def extract_http_info(payload: bytes) -> tuple:
    try:
        lines = payload.split(b'\r\n')
        if not lines:
            return None
        first_line = lines[0]
        parts = first_line.split(b' ')
        if len(parts) >= 3 and parts[2].startswith(b'HTTP/'):
            method = parts[0].decode('utf-8', errors='ignore')
            uri = parts[1].decode('utf-8', errors='ignore')
            host = ""
            for line in lines[1:]:
                if line.lower().startswith(b'host:'):
                    host = line[5:].strip().decode('utf-8', errors='ignore')
                    break
            info = f"{method} {uri}"
            if host:
                info += f" Host: {host}"
            return "HTTP", info
        if first_line.startswith(b'HTTP/'):
            info = first_line.decode('utf-8', errors='ignore')
            return "HTTP", f"HTTP Response: {info}"
    except Exception:
        pass
    return None

def extract_dns_info(packet) -> tuple:
    try:
        if packet.haslayer(DNS):
            dns = packet[DNS]
            qr = dns.qr  # 0 = query, 1 = response
            rcode = dns.rcode
            
            qname = ""
            if packet.haslayer(DNSQR) and dns.qd:
                qname = dns.qd.qname.decode('utf-8', errors='ignore') if isinstance(dns.qd.qname, bytes) else str(dns.qd.qname)
                if qname.endswith('.'):
                    qname = qname[:-1]
            
            if qr == 0:
                return "DNS", f"DNS Query: {qname}"
            else:
                answers = []
                if dns.an:
                    for i in range(dns.ancount):
                        try:
                            rr = dns.an[i]
                            rdata = rr.rdata
                            if isinstance(rdata, bytes):
                                rdata = rdata.decode('utf-8', errors='ignore')
                            rrname = rr.rrname.decode('utf-8', errors='ignore') if isinstance(rr.rrname, bytes) else str(rr.rrname)
                            if rrname.endswith('.'):
                                rrname = rrname[:-1]
                            answers.append(f"{rrname} -> {rdata}")
                        except Exception:
                            pass
                ans_str = ", ".join(answers[:3])
                if len(answers) > 3:
                    ans_str += f" ... (+{len(answers)-3} more)"
                return "DNS", f"DNS Response: {qname} -> [{ans_str}] (RCODE: {rcode})"
    except Exception:
        pass
    return None

def get_tcp_flags(tcp_layer) -> str:
    flags = []
    f = tcp_layer.flags
    if f & 0x01: flags.append("FIN")
    if f & 0x02: flags.append("SYN")
    if f & 0x04: flags.append("RST")
    if f & 0x08: flags.append("PSH")
    if f & 0x10: flags.append("ACK")
    if f & 0x20: flags.append("URG")
    return "+".join(flags) if flags else "None"

def process_pcap(pcap_path, output_path, batch_size=50000):
    print(f"[*] Starting PCAP conversion: {pcap_path} -> {output_path}")
    
    # Define PyArrow schema
    schema = pa.schema([
        ('timestamp', pa.string()),
        ('source_ip', pa.string()),
        ('dest_ip', pa.string()),
        ('source_port', pa.int32()),
        ('dest_port', pa.int32()),
        ('protocol', pa.string()),
        ('length', pa.int32()),
        ('info', pa.string())
    ])
    
    # Create output directory
    output_dir = os.path.dirname(output_path)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
        print(f"[*] Created output directory: {output_dir}")
        
    writer = None
    records = {
        'timestamp': [],
        'source_ip': [],
        'dest_ip': [],
        'source_port': [],
        'dest_port': [],
        'protocol': [],
        'length': [],
        'info': []
    }
    
    count = 0
    written_count = 0
    
    try:
        with PcapReader(pcap_path) as reader:
            for packet in reader:
                try:
                    # Basic packet attributes
                    # Convert scapy packet.time (float or Decimal) to float, then datetime
                    pkt_time = float(packet.time)
                    dt = datetime.datetime.fromtimestamp(pkt_time, datetime.timezone.utc)
                    timestamp_str = dt.isoformat()
                    
                    length = len(packet)
                    
                    source_ip = None
                    dest_ip = None
                    source_port = None
                    dest_port = None
                    protocol = "Unknown"
                    info = ""
                    
                    # Layer identification
                    if packet.haslayer(IP):
                        source_ip = packet[IP].src
                        dest_ip = packet[IP].dst
                        protocol = "IPv4"
                    elif packet.haslayer(IPv6):
                        source_ip = packet[IPv6].src
                        dest_ip = packet[IPv6].dst
                        protocol = "IPv6"
                    elif packet.haslayer(ARP):
                        arp = packet[ARP]
                        source_ip = arp.psrc
                        dest_ip = arp.pdst
                        protocol = "ARP"
                        if arp.op == 1:
                            info = f"Who has {arp.pdst}? Tell {arp.psrc}"
                        elif arp.op == 2:
                            info = f"Is-at {arp.hwsrc} (IP: {arp.psrc})"
                        else:
                            info = f"ARP op={arp.op}"
                    
                    # Transport & Application layers
                    if packet.haslayer(TCP):
                        tcp = packet[TCP]
                        source_port = int(tcp.sport)
                        dest_port = int(tcp.dport)
                        protocol = "TCP"
                        flags = get_tcp_flags(tcp)
                        info = f"TCP {source_port} -> {dest_port} [{flags}] Seq={tcp.seq} Ack={tcp.ack}"
                        
                        if tcp.payload:
                            payload_bytes = bytes(tcp.payload)
                            
                            # Try HTTP
                            http_res = extract_http_info(payload_bytes)
                            if http_res:
                                protocol, info = http_res
                            else:
                                # Try TLS
                                sni = extract_tls_sni(payload_bytes)
                                if sni:
                                    protocol = "TLS"
                                    info = f"TLS Client Hello SNI: {sni}"
                                elif len(payload_bytes) >= 5 and payload_bytes[0] == 0x16 and payload_bytes[1] == 0x03:
                                    protocol = "TLS"
                                    handshake_type = payload_bytes[5] if len(payload_bytes) > 5 else "unknown"
                                    info = f"TLS Handshake (Type: {handshake_type})"
                                elif len(payload_bytes) >= 5 and payload_bytes[0] == 0x17 and payload_bytes[1] == 0x03:
                                    protocol = "TLS"
                                    info = "TLS Application Data"
                                    
                    elif packet.haslayer(UDP):
                        udp = packet[UDP]
                        source_port = int(udp.sport)
                        dest_port = int(udp.dport)
                        protocol = "UDP"
                        info = f"UDP {source_port} -> {dest_port}"
                        
                        if packet.haslayer(DNS):
                            dns_res = extract_dns_info(packet)
                            if dns_res:
                                protocol, info = dns_res
                                
                    elif packet.haslayer(ICMP):
                        icmp = packet[ICMP]
                        protocol = "ICMP"
                        info = f"ICMP Type={icmp.type} Code={icmp.code}"
                        
                    if not info and protocol == "Unknown":
                        info = packet.summary()
                        
                    # Append to lists
                    records['timestamp'].append(timestamp_str)
                    records['source_ip'].append(source_ip)
                    records['dest_ip'].append(dest_ip)
                    records['source_port'].append(source_port)
                    records['dest_port'].append(dest_port)
                    records['protocol'].append(protocol)
                    records['length'].append(length)
                    records['info'].append(info)
                    
                    count += 1
                    
                    if count % batch_size == 0:
                        df = pd.DataFrame(records)
                        table = pa.Table.from_pandas(df, schema=schema)
                        if writer is None:
                            writer = pq.ParquetWriter(output_path, schema)
                        writer.write_table(table)
                        written_count += len(df)
                        print(f"[*] Processed and wrote {written_count} packets...")
                        # Reset records
                        records = {k: [] for k in records}
                        
                except Exception as pe:
                    # Log packet parsing errors but continue
                    print(f"[-] Error parsing packet {count}: {pe}", file=sys.stderr)
                    continue
                    
        # Write any remaining records
        if records['timestamp']:
            df = pd.DataFrame(records)
            table = pa.Table.from_pandas(df, schema=schema)
            if writer is None:
                writer = pq.ParquetWriter(output_path, schema)
            writer.write_table(table)
            written_count += len(df)
            print(f"[*] Processed and wrote remaining {len(df)} packets. Total: {written_count}")
            
    finally:
        if writer is not None:
            writer.close()
            
    print(f"[+] Successfully converted {written_count} packets to {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Convert PCAP network capture to Parquet format.")
    parser.add_argument("--pcap", required=True, help="Path to the input PCAP file")
    parser.add_argument("--output", required=True, help="Path to the output Parquet file")
    parser.add_argument("--batch-size", type=int, default=50000, help="Batch size for writing to Parquet (default: 50000)")
    
    args = parser.parse_args()
    
    if not os.path.exists(args.pcap):
        print(f"[-] Error: Input PCAP file does not exist: {args.pcap}", file=sys.stderr)
        sys.exit(1)
        
    process_pcap(args.pcap, args.output, args.batch_size)

if __name__ == "__main__":
    main()
