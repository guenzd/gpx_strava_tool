#!/usr/bin/env python3
import sys
from xml.etree import ElementTree as ET
from datetime import datetime

def parse_time(elem, ns):
    time_elem = elem.find('.//default:time', ns)
    if time_elem is not None:
        return datetime.fromisoformat(time_elem.text.replace('Z', '+00:00'))
    return None

def latest_time(root, ns):
    times = [parse_time(pt, ns) for pt in root.findall('.//default:trkpt', ns)]
    times = [t for t in times if t is not None]
    return max(times) if times else None

def merge_gpx_files_filtered(file1, file2, output_file):
    tree1 = ET.parse(file1)
    root1 = tree1.getroot()
    trkseg1 = root1.find('.//default:trkseg', {'default': root1.tag.split('}')[0].strip('{')})

    tree2 = ET.parse(file2)
    root2 = tree2.getroot()

    ns = {'default': 'http://www.topografix.com/GPX/1/1'}
    ET.register_namespace('', ns['default'])

    cutoff = latest_time(root1, ns)
    print(f"Splitting files at {cutoff}")

    has_later_points = False

    for pt in root2.findall('.//default:trkpt', ns):
        pt_time = parse_time(pt, ns)
        if pt_time and pt_time > cutoff:
            trkseg1.append(pt)
            has_later_points = True

    if not has_later_points:
        raise ValueError("No points in file2 are later than the latest point in file1.")

    tree1.write(output_file, encoding='utf-8', xml_declaration=True)

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print("Usage: merge_gpx.py file1.gpx file2.gpx output.gpx")
        sys.exit(1)
    merge_gpx_files_filtered(sys.argv[1], sys.argv[2], sys.argv[3])