# SIFT Command Library

This reference provides common command templates for forensic analysis in the SIFT container.

**Note**: you are encouraged to batch commands in a single shell call to preserve tool budgets.
Instead of running ls, then mount, then fls sequentially, use a single shell call to gather all environment context at once. This preserves the budget for actual forensic work.

### Examples: ### 

```shell
docker exec $(cat scratch/container_id.txt) bash -c "mount; ls /mnt/cases;"
```
You can also use HEREDOC format
```shell
cat <<EOF | docker exec --interactive $(cat scratch/container_id.txt) bash
cd /mnt
ls cases
mount
EOF
```

## 1. File System Analysis
### List files with timestamps (fls)
```bash
docker exec $(cat scratch/container_id.txt) fls -r /mnt/ewf/<CASEID>/<IMAGENAME>
```

### Calculate MD5 for a file
```bash
docker exec $(cat scratch/container_id.txt) md5sum /mnt/cases/<CASEID>/<IMAGENAME>/path/to/file.exe
```

## 2. Registry Analysis
### Dump hive contents (regfexport)
```bash
docker exec $(cat scratch/container_id.txt) regfexport /mnt/<CASEID>/<IMAGENAME>/Windows/System32/config/SOFTWARE
```

### Search for a key in a hive
```bash
docker exec $(cat scratch/container_id.txt) regfexport /mnt/<CASEID>/<IMAGENAME>/Windows/System32/config/SYSTEM | grep -i "KeyName" -A 10 -B 2
```

## 3. Tool Discovery
### Find executable
```bash
docker exec $(cat scratch/container_id.txt) find /usr -name "*tool*" -type f -executable
```

### Check if a tool is in the path
```bash
docker exec $(cat scratch/container_id.txt) which <toolname>
```

### Run a complex command including pipes in the container
```bash
cat <<EOF | docker exec --interactive $(cat scratch/container_id.txt) bash
fls -r /mnt/<path to ewf1 file> | grep -i <searchterm>
EOF
```
Otherwise using a pattern like 
```bash 
docker exec $(cat scratch/container_id.txt) fls -r /mnt/<path to ewf1 file | grep -i <searchterm> 
```

Will run the first part in the container and the piped part in the native host OS. 