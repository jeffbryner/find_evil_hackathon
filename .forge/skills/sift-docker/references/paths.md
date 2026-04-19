# Path Mappings

Understanding the relationship between the local host and the SIFT container is critical for moving data and executing tools correctly.

## 1. Local Project to Container
| Local Path | Container Path | Purpose |
|---|---|---|
| `./` | `/evidence/` | Project root (Source of truth) |
| `scratch/` | `/evidence/scratch/` | Shared temporary storage |
| `images/` | `/evidence/images/` | Forensic images |

## 2. Evidence Mounts (Inside Container)
| Container Path | Purpose |
|---|---|
| `/mnt/ewf/` | Mount point for E01 files (via ewfmount) |
| `/mnt/windows/` | Mount point for the target NTFS partition |

## 3. Tool Locations (Inside Container)
| Tool | Typical Path |
|---|---|
| `fls`, `mmls`, `icat` | `/usr/bin/` |
| `rip.pl` | `/usr/local/bin/rip.pl` |
| `regfexport` | `/usr/bin/regfexport` |
