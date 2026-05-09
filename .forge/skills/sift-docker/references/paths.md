# Path Mappings

Understanding the relationship between the local host and the SIFT container is critical for moving data and executing tools correctly.

## 1. Local Project to Container
| Local Path | Container Path | Purpose |
|---|---|---|
| `./` | `/cases/` | Project root (Source of truth) |
| `scratch/` | `/cases/scratch/` | Shared temporary storage |
| `images/` | `/cases/images/` | Forensic images |

## 2. Evidence Mounts (Inside Container)
| Container Path | Purpose |
|---|---|
| `/mnt/ewf/<CASEID>/<IMAGENAME>` | Mount point for raw expert witness E01 files (via ewfmount) |
| `/mnt/cases/<CASEID>/<IMAGENAME>` | Mount point for the target NTFS partition |

## 3. Tool Locations (Inside Container)
| Tool | Path |
|---|---|
| `fls`, `mmls`, `icat` | `/usr/bin/` |
| `rip.pl` | `/usr/local/bin/rip.pl` |
| `regfexport` | `/usr/bin/regfexport` |
| `vol` (volatility) | `/usr/local/bin/vol` |
| misc utilities | `/opt` |
