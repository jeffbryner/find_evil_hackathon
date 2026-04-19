import pandas as pd
import sys
import os

def parse_bodyfile(input_path, output_path):
    """
    Parses a Sleuthkit bodyfile and saves it as a Parquet file.
    Bodyfile format: MD5|name|inode|mode_as_string|UID|GID|size|atime|mtime|ctime|crtime
    """
    if not os.path.exists(input_path):
        print(f"[-] Input file not found: {input_path}")
        sys.exit(1)

    print(f"[*] Reading bodyfile: {input_path}")
    
    # Bodyfile is pipe-separated
    columns = [
        "md5", "file_path", "inode", "mode", "uid", "gid", "size", 
        "atime", "mtime", "ctime", "crtime"
    ]
    
    try:
        df = pd.read_csv(
            input_path, 
            sep="|", 
            names=columns, 
            header=None,
            quoting=3 # QUOTE_NONE to handle special characters in paths
        )
        
        # Convert timestamps from Unix epoch to datetime
        time_cols = ["atime", "mtime", "ctime", "crtime"]
        for col in time_cols:
            df[col] = pd.to_datetime(df[col], unit='s', errors='coerce')
        
        # Optimize numeric types
        df['size'] = pd.to_numeric(df['size'], errors='coerce').fillna(0).astype('int64')
        
        print(f"[*] Processed {len(df)} entries.")
        print(f"[*] Saving to Parquet: {output_path}")
        df.to_parquet(output_path, engine='pyarrow', index=False)
        print("[+] Success.")
        
    except Exception as e:
        print(f"[-] Error processing bodyfile: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: uv run bodyfile_to_parquet.py <input_bodyfile> <output_parquet>")
        sys.exit(1)
    
    parse_bodyfile(sys.argv[1], sys.argv[2])
