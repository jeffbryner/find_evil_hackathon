# Path Mappings

Understanding the relationship between the local host and the SIFT container is critical for moving data and executing tools correctly.

Each case gets it's own container so the mount points and directories will be relevent to the case. 
For this reason always be sure to reference .cases/<CASE_NAME>/scratch/container_id.txt in your docker exec


```shell
docker exec $(cat cases/<CASE_NAME>/scratch/container_id.txt) bash -c "mount; ls /mnt/cases;"
```

## 1. Local Project to Container
| Local Path | Container Path | Purpose |
|---|---|---|
| `./` | `/case/` | Project root (Source of truth) |
| `scratch/` | `/case/scratch/` | Shared temporary storage |
| `images/` | `/case/images/` | Forensic images |

## 2. Evidence Mounts (Inside Container)
Inside the container the /mnt directory will have local host images mounted by the container. We will still reference the CASEID in the mount path as a safety measure to ensure we are operating in the correct container. 

| Container Path | Purpose |
|---|---|
| `/mnt/ewf/<CASEID>/<IMAGENAME>` | Mount point for raw expert witness E01 files (via ewfmount) |
| `/mnt/cases/<CASEID>/<IMAGENAME>` | Mount point for the target partitions (NTFS, efs, etc) |

### Example: 
Local path: ./case/<CASEID>/images/disk_image.E01
Container accessable as: /case/images/disk_image.E01
Filesystem Mounted as: /mnt/cases/<CASEID>/disk_image.E01

## 3. Tool Locations (Inside Container)
| Tool | Path |
|---|---|
| `fls`, `mmls`, `icat` | `/usr/bin/` |
| `rip.pl` | `/usr/local/bin/rip.pl` |
| `regfexport` | `/usr/bin/regfexport` |
| `vol` (volatility) | `/usr/local/bin/vol` |
| misc utilities | `/opt` |
