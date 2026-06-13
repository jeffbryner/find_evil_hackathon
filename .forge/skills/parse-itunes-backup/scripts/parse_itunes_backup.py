#!/usr/bin/env python3
import os
import sys
import sqlite3
import plistlib
import json
import argparse
import datetime


def convert_cocoa_time(cocoa_time):
    try:
        dt = datetime.datetime(2001, 1, 1) + datetime.timedelta(
            seconds=float(cocoa_time)
        )
        return dt.strftime("%Y-%m-%d %H:%M:%S UTC")
    except Exception as e:
        return f"Unknown ({cocoa_time})"


def parse_twitter_drafts(backup_dir):
    # Find all Twitter draft directories
    drafts_root = os.path.join(
        backup_dir,
        "AppDomain-com.atebits.Tweetie2",
        "Documents",
        "com.atebits.tweetie.application-important-state",
    )
    if not os.path.exists(drafts_root):
        print("[-] Twitter drafts directory not found.")
        return

    print("\n=== [ Twitter Drafts ] ===")
    draft_count = 0
    for root, dirs, files in os.walk(drafts_root):
        for file in files:
            if file.startswith("composition."):
                draft_count += 1
                draft_path = os.path.join(root, file)
                print(f"\n[+] Found draft file: {draft_path}")
                try:
                    with open(draft_path, "rb") as f:
                        plist_data = plistlib.load(f)
                        # Extract text and dates from binary plist
                        objs = plist_data.get("$objects", [])
                        text = "None"
                        created_date = "None"
                        retry_date = "None"

                        # Find the text and date objects
                        for idx, obj in enumerate(objs):
                            if isinstance(obj, str) or (
                                isinstance(obj, str)
                                and len(obj) > 10
                                and obj
                                not in [
                                    "NSUUID",
                                    "NSObject",
                                    "NSNull",
                                    "NSURL",
                                    "NSMutableArray",
                                    "NSArray",
                                    "TFNTwitterMediaAssetImage",
                                    "TFNTwitterMediaAssetALAsset",
                                    "TFNTwitterMediaAsset",
                                    "com.atebits.tweetie.compose.attachments",
                                ]
                            ):
                                text = obj
                            if isinstance(obj, dict) and "NS.time" in obj:
                                time_val = obj["NS.time"]
                                # The first time object is usually the creation date, second is retry expiration
                                if created_date == "None":
                                    created_date = convert_cocoa_time(time_val)
                                else:
                                    retry_date = convert_cocoa_time(time_val)

                        print(f"  Draft Text:   {text}")
                        print(f"  Created Date: {created_date}")
                        print(f"  Retry Date:   {retry_date}")

                        # Look for attachments
                        attachments = [
                            obj
                            for obj in objs
                            if isinstance(obj, dict) and "localBackupFileName" in obj
                        ]
                        for att in attachments:
                            att_name = att.get("localBackupFileName")
                            att_dir = att.get("localBackupDirectory")
                            print(f"  Attachment:   {att_dir}/{att_name}")
                except Exception as e:
                    print(f"  [-] Error parsing draft plist: {e}")

    if draft_count == 0:
        print("[*] No Twitter drafts found.")


def parse_notes(backup_dir):
    notes_db = os.path.join(
        backup_dir, "AppDomainGroup-group.com.apple.notes", "NoteStore.sqlite"
    )
    if not os.path.exists(notes_db):
        print("[-] Notes database not found.")
        return

    print("\n=== [ iOS Notes ] ===")
    try:
        conn = sqlite3.connect(notes_db)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = [t[0] for t in cursor.fetchall()]

        note_table = None
        for t in ["ZICCLOUDSYNCINGOBJECT", "ZNOTE", "ZSFNOTE"]:
            if t in tables:
                note_table = t
                break

        if not note_table:
            print("[-] Standard Notes tables not found in database.")
            conn.close()
            return

        print(f"[+] Querying table: {note_table}")
        if note_table == "ZICCLOUDSYNCINGOBJECT":
            cursor.execute(
                "SELECT Z_PK, ZTITLE, ZSNIPPET, ZCREATIONDATE, ZMODIFICATIONDATE FROM ZICCLOUDSYNCINGOBJECT WHERE ZTITLE IS NOT NULL;"
            )
            rows = cursor.fetchall()
            print(f"Total Notes found: {len(rows)}")
            for r in rows:
                print(f"  Note ID: {r[0]}")
                print(f"    Title: {r[1]}")
                print(f"    Snippet: {r[2]}")
                print(f"    Created: {convert_cocoa_time(r[3])}")
                print(f"    Modified: {convert_cocoa_time(r[4])}")
        else:
            cursor.execute(f"SELECT * FROM {note_table} LIMIT 5;")
            print(f"Sample rows from {note_table}:")
            for r in cursor.fetchall()[:5]:
                print(f"  {r}")

        conn.close()
    except Exception as e:
        print(f"[-] Error reading Notes database: {e}")


def parse_call_history(backup_dir):
    call_db = os.path.join(
        backup_dir, "WirelessDomain", "Library", "CallHistory", "call_history.db"
    )
    if not os.path.exists(call_db):
        print("[-] Call history database not found.")
        return

    print("\n=== [ Call History ] ===")
    try:
        conn = sqlite3.connect(call_db)
        cursor = conn.cursor()

        # Check if table 'call' exists
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='call';"
        )
        if not cursor.fetchone():
            print("[-] Table 'call' not found in CallHistory database.")
            conn.close()
            return

        cursor.execute(
            "SELECT datetime(date, 'unixepoch') as date_utc, address, duration, answered FROM call ORDER BY date DESC LIMIT 50;"
        )
        rows = cursor.fetchall()
        print(f"Total Calls: {len(rows)}")
        for r in rows:
            status = "Answered" if r[3] == 1 else "Missed/No Answer"
            print(
                f"  Date: {r[0]} | Number: {r[1]} | Duration: {r[2]}s | Status: {status}"
            )

        conn.close()
    except Exception as e:
        print(f"[-] Error reading Call History database: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse extracted iOS iTunes backup files and databases."
    )
    parser.add_argument("backup_dir", help="Path to the unpacked backup directory")
    args = parser.parse_args()

    if not os.path.exists(args.backup_dir):
        print(f"[-] Backup directory does not exist: {args.backup_dir}")
        sys.exit(1)

    print(f"[*] Starting iTunes backup parser on: {args.backup_dir}")
    parse_twitter_drafts(args.backup_dir)
    parse_notes(args.backup_dir)
    parse_call_history(args.backup_dir)
    print("\n[*] Parsing completed.")


if __name__ == "__main__":
    main()
