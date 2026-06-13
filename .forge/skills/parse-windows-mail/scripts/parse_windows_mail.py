import os
import sys
import glob
import pandas as pd

def parse_esedb_export(export_dir, output_parquet):
    print(f"Parsing esedbexport output in: {export_dir}")
    # Find the Message table CSV
    csv_files = glob.glob(os.path.join(export_dir, "*Message*.csv"))
    if not csv_files:
        print("No Message table CSV found in export directory!")
        return False
    
    msg_csv = csv_files[0]
    print(f"Found Message CSV: {msg_csv}")
    
    # Read the CSV file
    df = pd.read_csv(msg_csv, low_memory=False)
    print(f"Loaded {len(df)} rows from Message table.")
    
    # Dynamically find columns
    columns_map = {}
    for col in df.columns:
        col_lower = col.lower()
        if 'subject' in col_lower:
            columns_map['subject'] = col
        elif 'sender' in col_lower or 'from' in col_lower:
            columns_map['sender'] = col
        elif 'recipient' in col_lower or 'to' in col_lower:
            columns_map['recipient'] = col
        elif 'received' in col_lower or 'date' in col_lower or 'time' in col_lower:
            columns_map['date'] = col
        elif 'body' in col_lower or 'content' in col_lower:
            columns_map['body'] = col
            
    print(f"Mapped columns: {columns_map}")
    
    # Create normalized DataFrame
    normalized_data = []
    for idx, row in df.iterrows():
        msg_id = row.get('id', idx)
        subject = row.get(columns_map.get('subject'), '')
        sender = row.get(columns_map.get('sender'), '')
        recipient = row.get(columns_map.get('recipient'), '')
        date = row.get(columns_map.get('date'), '')
        body = row.get(columns_map.get('body'), '')
        
        # Check if body is a long value reference (e.g. LongValue_X.bin)
        if isinstance(body, str) and body.startswith('LongValue_'):
            # Try to read from LongValue directory
            long_val_path = os.path.join(export_dir, 'LongValue', body)
            if os.path.exists(long_val_path):
                try:
                    with open(long_val_path, 'r', encoding='utf-16le', errors='replace') as f:
                        body = f.read()
                except Exception:
                    try:
                        with open(long_val_path, 'r', encoding='utf-8', errors='replace') as f:
                            body = f.read()
                    except Exception as e:
                        print(f"Error reading long value {body}: {e}")
                        
        normalized_data.append({
            'message_id': str(msg_id),
            'subject': str(subject),
            'sender': str(sender),
            'recipient': str(recipient),
            'date': str(date),
            'body': str(body)
        })
        
    df_norm = pd.DataFrame(normalized_data)
    
    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_parquet), exist_ok=True)
    
    # Write to Parquet
    df_norm.to_parquet(output_parquet, index=False)
    print(f"Successfully wrote {len(df_norm)} emails to Parquet: {output_parquet}")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python parse_windows_mail.py <export_dir> <output_parquet>")
        sys.exit(1)
    parse_esedb_export(sys.argv[1], sys.argv[2])
