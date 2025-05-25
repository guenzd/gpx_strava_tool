import sys
from xml.etree import ElementTree as ET

if len(sys.argv) != 3:
    print("Usage: python3 remove_heartrate.py input.gpx output.gpx")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

ns = {
    'default': 'http://www.topografix.com/GPX/1/1',
    'gpxtpx': 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1'
}
ET.register_namespace('', ns['default'])
ET.register_namespace('gpxtpx', ns['gpxtpx'])

tree = ET.parse(input_file)
root = tree.getroot()

for hr in root.findall('.//gpxtpx:hr', ns):
    parent = hr.getparent() if hasattr(hr, 'getparent') else None
    if parent:
        parent.remove(hr)

# fallback for ElementTree (no getparent support)
for ext in root.findall('.//gpxtpx:TrackPointExtension', ns):
    for hr in ext.findall('gpxtpx:hr', ns):
        ext.remove(hr)

tree.write(output_file, encoding='utf-8', xml_declaration=True)
print(f"✅ Saved cleaned GPX to {output_file}")