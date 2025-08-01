#!/bin/bash
rm -f merged.gpx
python3 merge_gpx.py "examples/track1.gpx" "examples/track2.gpx" "merged.gpx"
python3 merge_gpx.py "--prepend" "examples/track2.gpx" "examples/track1.gpx" "merged2.gpx"
python3 convert_fit.py "examples/track1.fit" "examples/track1-test.gpx"
python3 test.py merged.gpx examples/expected.gpx
python3 test.py merged2.gpx examples/expected_prepend.gpx
python3 test.py examples/track1-test.gpx examples/track1-target.gpx