#!/bin/bash
set -e

if [ "$#" -ne 3 ]; then
  echo "Usage: ./merge_gpx.sh original.gpx helper.gpx output.gpx"
  exit 1
fi

python3 merge_gpx.py --prepend "$1" "$2" "$3"