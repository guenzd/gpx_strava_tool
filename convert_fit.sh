#!/bin/bash
set -euo pipefail

if [ "$#" -ne 2 ]; then
  echo "Usage: ./convert_fit.sh input.fit output.gpx"
  exit 1
fi

# Check if fitparse is installed
if ! python3 -c "import fitparse" 2>/dev/null; then
  echo "Installing required package 'fitparse'..."
  pip3 install fitparse
fi

python3 convert_fit.py "$1" "$2"
