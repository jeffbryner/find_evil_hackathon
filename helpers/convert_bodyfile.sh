#!/bin/bash
# Description: Convert a Sleuthkit bodyfile to Parquet format.
# Usage: convert_bodyfile <input_bodyfile.txt> <output.parquet>
# Example: convert_bodyfile scratch/bodyfile.txt scratch/file_metadata.parquet

if [ "$#" -ne 2 ]; then
    echo "Usage: convert_bodyfile <input_bodyfile.txt> <output.parquet>"
    exit 1
fi

uv run bodyfile_to_parquet.py "$1" "$2"
