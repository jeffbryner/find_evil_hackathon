#!/usr/bin/env python3
import os
import re
import html
import json
import argparse
import duckdb

def clean_html(raw_html):
    if not raw_html:
        return ""
    clean_re = re.compile('<style.*?>.*?</style>|<script.*?>.*?</script>', re.DOTALL | re.IGNORECASE)
    raw_html = clean_re.sub('', raw_html)
    clean_re = re.compile('<.*?>')
    text = clean_re.sub('', raw_html)
    text = html.unescape(text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def parse_recipients(recipients_path):
    recipients = []
    if not os.path.exists(recipients_path):
        return recipients
    with open(recipients_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    
    current_recipient = {}
    for line in content.splitlines():
        line = line.strip()
        if not line:
            if current_recipient:
                recipients.append(current_recipient)
                current_recipient = {}
            continue
        if ':' in line:
            key, val = line.split(':', 1)
            current_recipient[key.strip()] = val.strip()
    if current_recipient:
        recipients.append(current_recipient)
    return recipients

def parse_headers(headers_path):
    headers = {}
    if not os.path.exists(headers_path):
        return headers
    with open(headers_path, 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            line = line.strip()
            if ':' in line:
                key, val = line.split(':', 1)
                headers[key.strip()] = val.strip()
    return headers

def main():
    parser = argparse.ArgumentParser(description="Parse pffexport-extracted email folders into structured formats.")
    parser.add_argument("-e", "--export-dir", help="Path to pffexport .export directory")
    parser.add_argument("-r", "--recovered-dir", help="Path to pffexport .recovered directory")
    parser.add_argument("-j", "--output-json", help="Path to save output JSON file")
    parser.add_argument("-p", "--output-parquet", help="Path to save output Parquet file")
    parser.add_argument("-m", "--output-md", help="Path to save Markdown report")
    
    args = parser.parse_args()
    
    all_emails = []
    
    for base_dir in [args.export_dir, args.recovered_dir]:
        if not base_dir or not os.path.exists(base_dir):
            continue
        for root, dirs, files in os.walk(base_dir):
            if "OutlookHeaders.txt" in files:
                msg_dir = root
                headers = parse_headers(os.path.join(msg_dir, "OutlookHeaders.txt"))
                recipients = parse_recipients(os.path.join(msg_dir, "Recipients.txt"))
                
                body_text = ""
                body_type = ""
                for body_file in ["Message.html", "Message.txt", "Message.rtf"]:
                    bp = os.path.join(msg_dir, body_file)
                    if os.path.exists(bp):
                        with open(bp, 'r', encoding='utf-8', errors='ignore') as f:
                            body_content = f.read()
                        if body_file == "Message.html":
                            body_text = clean_html(body_content)
                            body_type = "HTML"
                        else:
                            body_text = body_content.strip()
                            body_type = "Text/RTF"
                        break
                
                rel_path = os.path.relpath(msg_dir, base_dir)
                all_emails.append({
                    "source": os.path.basename(base_dir),
                    "path": rel_path,
                    "subject": headers.get("Subject", ""),
                    "sender_name": headers.get("Sender name", ""),
                    "sender_email": headers.get("Sender email address", ""),
                    "delivery_time": headers.get("Delivery time", headers.get("Client submit time", "")),
                    "recipients": json.dumps(recipients),
                    "body": body_text,
                    "body_type": body_type
                })
                
    print(f"Parsed {len(all_emails)} emails.")
    
    if not all_emails:
        return
        
    # Write JSON
    json_path = args.output_json or "emails.json"
    json_dir = os.path.dirname(os.path.abspath(json_path))
    if json_dir:
        os.makedirs(json_dir, exist_ok=True)
    with open(json_path, "w") as f:
        json.dump(all_emails, f, indent=2)
    print(f"JSON saved to {json_path}")
    
    # Write Parquet via DuckDB
    if args.output_parquet:
        pq_dir = os.path.dirname(os.path.abspath(args.output_parquet))
        if pq_dir:
            os.makedirs(pq_dir, exist_ok=True)
        duckdb.execute(f"COPY (SELECT * FROM read_json_auto('{json_path}')) TO '{args.output_parquet}' (FORMAT 'PARQUET')")
        print(f"Parquet saved to {args.output_parquet}")
        
    # Write Markdown
    if args.output_md:
        md_dir = os.path.dirname(os.path.abspath(args.output_md))
        if md_dir:
            os.makedirs(md_dir, exist_ok=True)
        md_content = f"# Email Database Forensic Report\n\n## Summary of Findings\n- **Total Emails Extracted:** {len(all_emails)}\n\n## Email Message Log\n| ID | Source | Date | From | Subject |\n|---|---|---|---|---|\n"
        for idx, email in enumerate(all_emails, 1):
            md_content += f"| {idx} | {email['source']} | {email['delivery_time']} | {email['sender_name']} | {email['subject']} |\n"
        with open(args.output_md, "w") as f:
            f.write(md_content)
        print(f"Markdown report saved to {args.output_md}")

if __name__ == "__main__":
    main()
