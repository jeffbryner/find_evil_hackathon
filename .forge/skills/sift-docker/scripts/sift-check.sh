#!/bin/bash
# Check if SIFT container is running and evidence is mounted

if [ ! -f "cases/<CASE_NAME>/scratch/container_id.txt" ]; then
    echo "[-] Error: cases/<CASE_NAME>/scratch/container_id.txt not found."
    exit 1
fi

CONTAINER_ID=$(cat cases/<CASE_NAME>/scratch/container_id.txt)

# Check container status
if ! docker ps --format '{{.ID}}' | grep -q "^${CONTAINER_ID:0:12}"; then
    echo "[-] Error: Container $CONTAINER_ID is not running."
    exit 1
fi

# Check mount point
if ! docker exec "$CONTAINER_ID" ls /mnt/cases > /dev/null 2>&1; then
    echo "[-] Warning: /mnt/cases is not accessible inside the container."
else
    echo "[+] SIFT container is running and evidence is mounted."
fi

