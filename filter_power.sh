#!/bin/bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: ./filter_power.sh input.gpx output.gpx"
  exit 1
fi

python3 filter_power.py "$1" "$2"