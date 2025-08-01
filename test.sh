#!/bin/bash
rm -f merged.gpx
python3 merge_gpx.py "examples/track1.gpx" "examples/track2.gpx" "merged.gpx"
python3 merge_gpx.py "--prepend" "examples/track2.gpx" "examples/track1.gpx" "merged2.gpx"

python3 test.py merged.gpx examples/expected.gpx
python3 test.py merged2.gpx examples/expected_prepend.gpx