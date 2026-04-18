import duckdb
import pandas as pd
import os

def main():
    parquet_path = "scratch/file_metadata.parquet"
    if not os.path.exists(parquet_path):
        print(f"[-] Parquet file not found: {parquet_path}")
        return

    print("[*] Initializing DuckDB Analysis...")
    con = duckdb.connect(database=':memory:')
    
    # Load Parquet into a table
    con.execute(f"CREATE TABLE file_metadata AS SELECT * FROM read_parquet('{parquet_path}')")
    
    print(f"[+] Loaded {con.execute('SELECT count(*) FROM file_metadata').fetchone()[0]} entries.")

    # 1. Persistence Check
    print("\n[*] --- Persistence Check (Run Keys & Services) ---")
    persistence_query = """
    SELECT file_path, mtime, crtime 
    FROM file_metadata 
    WHERE file_path ILIKE 'Microsoft/Windows/CurrentVersion/Run%'
       OR file_path ILIKE 'SystemControlSet%/Services%'
       OR file_path ILIKE '%/Microsoft/Windows/CurrentVersion/Run%'
       OR file_path ILIKE '%/SystemControlSet%/Services%'
    ORDER BY mtime DESC
    LIMIT 10;
    """
    # Note: Sleuthkit uses forward slashes in bodyfiles usually
    print(con.execute(persistence_query).fetchdf())

    # 2. Suspicious System32 Activity
    print("\n[*] --- Suspicious System32 Activity (Non-EXE/DLL) ---")
    system32_query = """
    SELECT file_path, size, crtime, mtime 
    FROM file_metadata 
    WHERE (file_path ILIKE 'Windows/System32/%' OR file_path ILIKE '%/Windows/System32/%')
      AND (file_path NOT ILIKE '%.dll' AND file_path NOT ILIKE '%.exe')
      AND size > 0
    ORDER BY crtime DESC
    LIMIT 10;
    """
    print(con.execute(system32_query).fetchdf())

    # 3. User Execution (Temp/AppData)
    print("\n[*] --- User Execution (Temp/AppData) ---")
    user_exec_query = """
    SELECT file_path, size, crtime 
    FROM file_metadata 
    WHERE (file_path ILIKE 'Users/%/AppData/Local/Temp/%'
           OR file_path ILIKE '%/Users/%/AppData/Local/Temp/%'
           OR file_path ILIKE 'Users/%/AppData/Roaming/%'
           OR file_path ILIKE '%/Users/%/AppData/Roaming/%')
      AND (file_path ILIKE '%.exe' OR file_path ILIKE '%.ps1' OR file_path ILIKE '%.bat')
    ORDER BY crtime DESC
    LIMIT 10;
    """
    print(con.execute(user_exec_query).fetchdf())

if __name__ == "__main__":
    main()
