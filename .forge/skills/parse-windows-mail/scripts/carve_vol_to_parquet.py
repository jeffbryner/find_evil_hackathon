import os
import re
import sys
import pandas as pd


def carve_vol(file_path, output_parquet, domains=None):
    print(f"Carving raw text and emails from: {file_path}")
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return False

    if not domains:
        # Default domains of interest if none are specified
        domains = ["gmail.com", "icloud.com", "qq.com"]

    print(f"Searching for domains: {domains}")
    with open(file_path, "rb") as f:
        data = f.read()

    # Decode the entire file as UTF-16LE and ASCII/UTF-8 with replacement
    text_utf16 = data.decode("utf-16le", errors="replace")
    text_ascii = data.decode("utf-8", errors="replace")

    carved_records = []

    # Scan UTF-16LE text
    for domain in domains:
        for match in re.finditer(re.escape(domain), text_utf16, re.IGNORECASE):
            idx = match.start()
            # Extract a window of 600 characters around the match
            start_idx = max(0, idx - 300)
            end_idx = min(len(text_utf16), idx + 300)
            context = text_utf16[start_idx:end_idx]

            # Clean context (printable ASCII characters and standard spacing)
            context_cleaned = "".join(
                c if (32 <= ord(c) <= 126 or c in "\n\r\t") else "." for c in context
            )

            # Try to extract headers from context using heuristics
            sender = "Unknown"
            recipient = "Unknown"
            subject = "Carved Email Fragment"

            sender_match = re.search(
                r"(?:From|Sender|SenderAddress)\s*:\s*([^\s\r\n]+)",
                context,
                re.IGNORECASE,
            )
            if sender_match:
                sender = sender_match.group(1)
            recipient_match = re.search(
                r"(?:To|Recipient|RecipientAddress)\s*:\s*([^\s\r\n]+)",
                context,
                re.IGNORECASE,
            )
            if recipient_match:
                recipient = recipient_match.group(1)
            subject_match = re.search(
                r"(?:Subject|Title)\s*:\s*([^\r\n]+)", context, re.IGNORECASE
            )
            if subject_match:
                subject = subject_match.group(1)

            carved_records.append(
                {
                    "source": "UTF-16LE",
                    "offset": idx * 2,  # byte offset
                    "sender": sender,
                    "recipient": recipient,
                    "subject": subject,
                    "body": context_cleaned,
                }
            )

    # Scan ASCII/UTF-8 text
    for domain in domains:
        for match in re.finditer(re.escape(domain), text_ascii, re.IGNORECASE):
            idx = match.start()
            # Extract a window of 600 characters around the match
            start_idx = max(0, idx - 300)
            end_idx = min(len(text_ascii), idx + 300)
            context = text_ascii[start_idx:end_idx]

            # Clean context
            context_cleaned = "".join(
                c if (32 <= ord(c) <= 126 or c in "\n\r\t") else "." for c in context
            )

            sender = "Unknown"
            recipient = "Unknown"
            subject = "Carved Email Fragment"

            sender_match = re.search(
                r"(?:From|Sender|SenderAddress)\s*:\s*([^\s\r\n]+)",
                context,
                re.IGNORECASE,
            )
            if sender_match:
                sender = sender_match.group(1)
            recipient_match = re.search(
                r"(?:To|Recipient|RecipientAddress)\s*:\s*([^\s\r\n]+)",
                context,
                re.IGNORECASE,
            )
            if recipient_match:
                recipient = recipient_match.group(1)
            subject_match = re.search(
                r"(?:Subject|Title)\s*:\s*([^\r\n]+)", context, re.IGNORECASE
            )
            if subject_match:
                subject = subject_match.group(1)

            carved_records.append(
                {
                    "source": "ASCII",
                    "offset": idx,
                    "sender": sender,
                    "recipient": recipient,
                    "subject": subject,
                    "body": context_cleaned,
                }
            )

    if not carved_records:
        print("No email fragments carved!")
        return False

    df = pd.DataFrame(carved_records)
    # Deduplicate similar overlaps
    df = df.drop_duplicates(subset=["body"])

    # Save to Parquet
    os.makedirs(os.path.dirname(output_parquet), exist_ok=True)
    df.to_parquet(output_parquet, index=False)
    print(f"Successfully carved {len(df)} email fragments to Parquet: {output_parquet}")
    return True


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(
            "Usage: python carve_vol_to_parquet.py <vol_file> <output_parquet> [domains_comma_separated]"
        )
        sys.exit(1)

    domains = None
    if len(sys.argv) > 3:
        domains = [d.strip() for d in sys.argv[3].split(",") if d.strip()]

    carve_vol(sys.argv[1], sys.argv[2], domains)
