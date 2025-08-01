import sys
from xml.etree import ElementTree as ET

if len(sys.argv) != 3:
    print("Usage: python3 remove_power.py input.gpx output.gpx")
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

# Remove power tags under extensions with default namespace
for ext in root.findall('.//default:extensions', ns):
    for power in ext.findall('default:power', ns):
        ext.remove(power)
    # Also try without namespace
    for power in ext.findall('power'):
        ext.remove(power)
    # Also try with explicit namespace
    for power in ext.findall('{http://www.topografix.com/GPX/1/1}power'):
        ext.remove(power)

# Also check under TrackPointExtension
for ext in root.findall('.//gpxtpx:TrackPointExtension', ns):
    for power in ext.findall('gpxtpx:power', ns):
        ext.remove(power)

tree.write(output_file, encoding='utf-8', xml_declaration=True)
print(f"✅ Saved cleaned GPX to {output_file}")