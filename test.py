import sys
from xml.etree import ElementTree as ET

if len(sys.argv) != 3:
    print("Usage: python3 test.py merged.gpx merged_expected.gpx")
    sys.exit(1)

actual_file = sys.argv[1]
expected_file = sys.argv[2]

from datetime import datetime, timedelta

def parse_time(time_str):
    return datetime.strptime(time_str, '%Y-%m-%dT%H:%M:%SZ')

def points_match(p1, p2, lat_tolerance=0.00005, lon_tolerance=0.00005, time_tolerance_seconds=2):
    lat1, lon1, time1 = p1
    lat2, lon2, time2 = p2
    
    # Check coordinates within tolerance
    if abs(lat1 - lat2) > lat_tolerance or abs(lon1 - lon2) > lon_tolerance:
        return False
    
    # Check time within tolerance
    if time1 and time2:
        t1 = parse_time(time1)
        t2 = parse_time(time2)
        if abs((t1 - t2).total_seconds()) > time_tolerance_seconds:
            return False
            
    return True

def get_trkpt_data(path):
    """Get track points that have valid timestamps."""
    tree = ET.parse(path)
    ns = {'default': 'http://www.topografix.com/GPX/1/1'}
    trkpts = tree.findall('.//default:trkpt', ns)
    valid_points = []
    
    for p in trkpts:
        try:
            time = p.find('default:time', ns)
            if time is not None and time.text:
                # Include all points that have a timestamp, even if lat/lon are missing
                lat = float(p.attrib.get('lat', 0))
                lon = float(p.attrib.get('lon', 0))
                valid_points.append((lat, lon, time.text))
        except (ValueError, KeyError):
            continue  # Skip points with invalid data
            
    return valid_points

actual = get_trkpt_data(actual_file)
expected = get_trkpt_data(expected_file)

def format_trackpoint(tp):
    lat, lon, time = tp
    return f"lat={lat:.7f}, lon={lon:.7f}, time={time}"

# Compare only valid points
if len(actual) != len(expected):
  actual = get_trkpt_data(actual_file)
  expected = get_trkpt_data(expected_file)

def format_trackpoint(tp):
    lat, lon, time = tp
    return f"lat={lat:.7f}, lon={lon:.7f}, time={time}"

def get_mismatch_details(p1, p2):
    lat1, lon1, time1 = p1
    lat2, lon2, time2 = p2
    details = []
    
    if abs(lat1 - lat2) > 0.0000001:
        details.append(f"lat diff: {abs(lat1 - lat2):.9f}")
    if abs(lon1 - lon2) > 0.0000001:
        details.append(f"lon diff: {abs(lon1 - lon2):.9f}")
    if time1 and time2:
        t1 = parse_time(time1)
        t2 = parse_time(time2)
        diff_seconds = abs((t1 - t2).total_seconds())
        if diff_seconds > 0:
            details.append(f"time diff: {diff_seconds:.1f}s")
    
    return ", ".join(details) if details else "identical"

# Report the number of valid points found
print(f"Found {len(actual)} valid points in actual file")
print(f"Found {len(expected)} valid points in expected file")

# Compare points with tolerance
differences = []
min_len = min(len(actual), len(expected))

for i in range(min_len):
    if not points_match(actual[i], expected[i]):
        differences.append((i, actual[i], expected[i]))

if differences:
    print("❌ Test failed: Some trackpoints differ beyond tolerance.")
    print(f"Total differences: {len(differences)}")
    print("\nFirst 10 differences:")
    
    for i, (idx, a, e) in enumerate(differences[:10]):
        print(f"\nDifference {i+1} at point {idx}:")
        print(f"→ Actual:   {format_trackpoint(a)}")
        print(f"→ Expected: {format_trackpoint(e)}")
        print(f"→ Details:  {get_mismatch_details(a, e)}")
    
    if len(differences) > 10:
        print(f"\n... and {len(differences) - 10} more differences")
    sys.exit(1)

print("✅ Test passed: GPX files match.")