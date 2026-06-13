# SIFT Command Library

This reference provides common command templates for forensic analysis in the SIFT container.

## ⚡ Forensic Chain Templates
Batching commands into a single execution preserves tool budget and context.

### 1. The "Locate & Hash" Chain
Search for a file, get its metadata, and calculate its hash in one go.
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) bash -c "find /mnt/cases -name 'target.exe' -exec ls -l {} \; -exec md5sum {} \; -exec exiftool {} \;"
```

### 2. The "Extract & Verify" Chain
Extract a file from an image and perform initial analysis.
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) bash -c "cp /mnt/cases/<CASEID>/<IMAGE>/path/to/file /scratch/ && cd /scratch/ && md5sum file && strings file | grep -i 'keyword'"
```

### 3. The "Multi-Path Orientation" Chain
Check multiple potential locations for a file to avoid trial-and-error.
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) bash -c "ls -l /mnt/cases/<CASEID>/<IMAGE>/Path1/file /mnt/cases/<CASEID>/<IMAGE>/Path2/file 2>/dev/null"
```

## ⚠️ Anti-Patterns (Avoid These)
- **Verbose Noise**: Never run `ls -R /mnt/cases/` or recursive `fls` on a large system drive unless absolutely necessary. It will saturate the context and waste tokens.
- **External Piping for Large Data**: Running `docker exec ... fls | grep` sends the entire file list to the host. Use `docker exec ... bash -c "fls | grep"` to filter inside the container.

## 1. File System Analysis
### List files with timestamps (fls)
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) fls -r /mnt/ewf/<CASEID>/<IMAGENAME>
```

### Calculate MD5 for a file
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) md5sum /mnt/cases/<CASEID>/<IMAGENAME>/path/to/file.exe
```

## 2. Registry Analysis
### Dump hive contents (regfexport)
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) target-reg -k "HKEY_LOCAL_MACHINE\\Software\\" -d 1 -q /case/images/<IMAGENAME>
```

### Search for a key in a hive
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) regfexport /mnt/<CASEID>/<IMAGENAME>/Windows/System32/config/SYSTEM | grep -i "KeyName" -A 10 -B 2
```

## 3. Tool Discovery
### Find executable
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) find /usr -name "*tool*" -type f -executable
```

### Check if a tool is in the path
```bash
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) which <toolname>
```

### Run a complex command including pipes in the container
```bash
cat <<EOF | docker exec --interactive $(cat cases/<CASE_NAME>/scratch/container_id.txt) bash
fls -r /mnt/<path to ewf1 file> | grep -i <searchterm>
EOF
```
Otherwise using a pattern like 
```bash 
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) fls -r /mnt/<path to ewf1 file | grep -i <searchterm> 
```

Will run the first part in the container and the piped part in the native host OS. 