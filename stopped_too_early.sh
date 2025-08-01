#!/bin/bash
set -e

if [ "$#" -ne 3 ]; then
  echo "Usage: ./merge_gpx.sh file1.gpx file2.gpx output.gpx"
  exit 1
fi

python3 merge_gpx.py "$1" "$2" "$3"