import sys
from xml.etree import ElementTree as ET

if len(sys.argv) != 3:
    print("Usage: python3 test.py merged.gpx merged_expected.gpx")
    sys.exit(1)

actual_file = sys.argv[1]
expected_file = sys.argv[2]

def get_trkpt_data(path):
    tree = ET.parse(path)
    ns = {'default': 'http://www.topografix.com/GPX/1/1'}
    trkpts = tree.findall('.//default:trkpt', ns)
    return [
        (
            float(p.attrib['lat']),
            float(p.attrib['lon']),
            p.find('default:time', ns).text if p.find('default:time', ns) is not None else None
        )
        for p in trkpts
    ]

actual = get_trkpt_data(actual_file)
expected = get_trkpt_data(expected_file)

if actual != expected:
    print("❌ Test failed: Merged trackpoints differ.")
    print("→ Actual:", actual)
    print("→ Expected:", expected)
    sys.exit(1)

print("✅ Test passed: GPX files match.")