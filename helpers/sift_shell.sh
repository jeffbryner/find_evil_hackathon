#!/bin/bash

# Check for --case argument
if [ "$1" != "--case" ] || [ -z "$2" ]; then
    echo "Usage: $0 --case <case_name>"
    exit 1
fi

CASE_NAME=$2
CONTAINER_ID_FILE="cases/${CASE_NAME}/scratch/container_id.txt"

if [ ! -f "$CONTAINER_ID_FILE" ]; then
    echo "[-] Error: ${CONTAINER_ID_FILE} not found."
    exit 1
fi

CONTAINER_ID=$(cat "$CONTAINER_ID_FILE")
docker exec -it "$CONTAINER_ID" /bin/bash
