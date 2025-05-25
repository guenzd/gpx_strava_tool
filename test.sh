#!/bin/bash
rm -f merged.gpx
python3 merge_gpx.py "examples/track1.gpx" "examples/track2.gpx" "merged.gpx"
python3 test.py merged.gpx examples/expected.gpx