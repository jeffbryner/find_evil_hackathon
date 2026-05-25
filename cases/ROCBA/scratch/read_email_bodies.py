import os
import re
from email import message_from_file
from email.header import decode_header

def decode_mime_header(s):
    if not s:
        return ""
    try:
        parts = decode_header(s)
        decoded = []
        for part, encoding in parts:
            if isinstance(part, bytes):
                decoded.append(part.decode(encoding or 'utf-8', errors='replace'))
            else:
                decoded.append(part)
        return "".join(decoded)
    except Exception:
        return s

def get_email_body(msg):
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    body += payload.decode('utf-8', errors='replace')
                except Exception:
                    pass
            elif content_type == "text/html" and not body and "attachment" not in content_disposition:
                try:
                    payload = part.get_payload(decode=True)
                    body += payload.decode('utf-8', errors='replace')
                except Exception:
                    pass
    else:
        try:
            payload = msg.get_payload(decode=True)
            body = payload.decode('utf-8', errors='replace')
        except Exception:
            pass
    return body

base_dir = "cases/ROCBA/scratch/extracted_pst/Outlook Data File"
emails = []

for root, dirs, files in os.walk(base_dir):
    folder_name = os.path.relpath(root, base_dir)
    for file in files:
        if file.isdigit():
            file_path = os.path.join(root, file)
            try:
                with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                    msg = message_from_file(f)
                
                subject = decode_mime_header(msg.get("Subject"))
                sender = decode_mime_header(msg.get("From"))
                to = decode_mime_header(msg.get("To"))
                date = decode_mime_header(msg.get("Date"))
                body = get_email_body(msg)
                
                # Find attachments on disk for this email
                prefix = f"{file}-"
                attachments = []
                for other_file in files:
                    if other_file.startswith(prefix):
                        attachments.append(other_file[len(prefix):])
                
                emails.append({
                    "folder": folder_name,
                    "id": file,
                    "subject": subject,
                    "sender": sender,
                    "to": to,
                    "date": date,
                    "body": body,
                    "attachments": attachments
                })
            except Exception as e:
                print(f"Error parsing {file_path}: {e}")

# Sort emails by folder and id
emails.sort(key=lambda x: (x["folder"], int(x["id"])))

output_path = "cases/ROCBA/scratch/all_emails_bodies.md"
with open(output_path, "w", encoding="utf-8") as out:
    out.write("# Recovered PST Email Contents\n\n")
    out.write(f"Total Emails: {len(emails)}\n\n")
    
    for email in emails:
        out.write(f"## Folder: {email['folder']} / ID: {email['id']}\n")
        out.write(f"**Date:** {email['date']}\n")
        out.write(f"**From:** {email['sender']}\n")
        out.write(f"**To:** {email['to']}\n")
        out.write(f"**Subject:** {email['subject']}\n")
        if email['attachments']:
            out.write(f"**Attachments:** {', '.join(email['attachments'])}\n")
        out.write("\n**Body:**\n")
        # Clean up html body if it looks like html
        body_text = email['body']
        if "<html" in body_text.lower() or "<body" in body_text.lower():
            # strip HTML tags roughly
            body_text = re.sub(r'<style[^>]*>[\s\S]*?</style>', '', body_text, flags=re.IGNORECASE)
            body_text = re.sub(r'<script[^>]*>[\s\S]*?</script>', '', body_text, flags=re.IGNORECASE)
            body_text = re.sub(r'<[^>]+>', '', body_text)
            body_text = re.sub(r'\n\s*\n+', '\n\n', body_text)
        out.write(f"```text\n{body_text.strip()}\n```\n")
        out.write("\n" + "="*80 + "\n\n")

print(f"Successfully wrote {len(emails)} emails to {output_path}")
