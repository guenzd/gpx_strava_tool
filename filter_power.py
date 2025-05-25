import sys
from xml.etree import ElementTree as ET
from datetime import datetime

if len(sys.argv) != 3:
    print("Usage: python3 filter_power.py input.gpx output.gpx")
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

removed_minutes = set()

for trkseg in root.findall('.//default:trkseg', ns):
    for pt in trkseg.findall('default:trkpt', ns):
        power = pt.find('default:extensions/default:power', ns)
        if power is None:
            time_elem = pt.find('default:time', ns)
            if time_elem is not None:
                try:
                    dt = datetime.fromisoformat(time_elem.text.replace('Z', '+00:00'))
                    removed_minutes.add(dt.strftime("%H:%M"))
                except Exception:
                    removed_minutes.add(f"INVALID({time_elem.text})")
            trkseg.remove(pt)

tree.write(output_file, encoding='utf-8', xml_declaration=True)

print(f"✅ Saved filtered GPX to {output_file}")
if removed_minutes:
    print("🗑 Removed entries in minutes:")
    for t in sorted(removed_minutes):
        print(f" - {t}")
else:
    print("✅ No entries removed")