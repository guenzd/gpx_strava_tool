#!/usr/bin/env python3
import sys
from fitparse import FitFile
from geographiclib.geodesic import Geodesic
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from xml.dom import minidom

def create_gpx_element():
    gpx = ET.Element('gpx')
    gpx.set('version', '1.1')
    gpx.set('creator', 'StravaGPX')
    gpx.set('xmlns', 'http://www.topografix.com/GPX/1/1')
    gpx.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')
    gpx.set('xmlns:gpxtpx', 'http://www.garmin.com/xmlschemas/TrackPointExtension/v1')
    gpx.set('xmlns:gpxx', 'http://www.garmin.com/xmlschemas/GpxExtensions/v3')
    gpx.set('xsi:schemaLocation',
        'http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd ' +
        'http://www.garmin.com/xmlschemas/GpxExtensions/v3 http://www.garmin.com/xmlschemas/GpxExtensionsv3.xsd ' +
        'http://www.garmin.com/xmlschemas/TrackPointExtension/v1 http://www.garmin.com/xmlschemas/TrackPointExtensionv1.xsd')
    return gpx

def semicircles_to_degrees(semicircles):
    if semicircles is None:
        return None
    return semicircles * 180.0 / (2 ** 31)

def fit_to_gpx(fit_file, gpx_file):
    try:
        fitfile = FitFile(fit_file)
        fitfile.parse()
    except Exception as e:
        print(f"Error parsing FIT file: {e}")
        sys.exit(1)

    gpx = create_gpx_element()
    metadata = ET.SubElement(gpx, 'metadata')
    time_elem = ET.SubElement(metadata, 'time')
    time_elem.text = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    trk = ET.SubElement(gpx, 'trk')
    name_elem = ET.SubElement(trk, 'name')
    activity_name = None

    for record in fitfile.get_messages('session'):
        vals = record.get_values()
        if vals.get('name'):
            activity_name = vals['name']
            break
    if not activity_name:
        for record in fitfile.get_messages('session'):
            vals = record.get_values()
            if vals.get('sport'):
                activity_name = str(vals['sport']).title()
                break
    name_elem.text = activity_name or 'Activity'

    type_elem = ET.SubElement(trk, 'type')
    type_elem.text = 'cycling'
    trkseg = ET.SubElement(trk, 'trkseg')

    total_records = valid_records = skipped_records = 0
    skipped_reasons = {'time': 0}

    points = []
    for record in fitfile.get_messages('record'):
        total_records += 1
        vals = record.get_values()
        timestamp = vals.get('timestamp')
        if timestamp is None:
            skipped_reasons['time'] += 1
            continue
        lat = semicircles_to_degrees(vals.get('position_lat'))
        lon = semicircles_to_degrees(vals.get('position_long'))
        points.append({'timestamp': timestamp, 'lat': lat, 'lon': lon, 'values': vals})

    i = 0
    while i < len(points):
        if points[i]['lat'] is None or points[i]['lon'] is None:
            gap_start = i
            last_valid = None if gap_start == 0 else points[gap_start - 1]
            gap_end = gap_start
            while gap_end < len(points) and (points[gap_end]['lat'] is None or points[gap_end]['lon'] is None):
                gap_end += 1
            next_valid = points[gap_end] if gap_end < len(points) else None

            if last_valid and next_valid:
                total_secs = (next_valid['timestamp'] - last_valid['timestamp']).total_seconds()
                line = Geodesic.WGS84.InverseLine(
                    last_valid['lat'], last_valid['lon'],
                    next_valid['lat'], next_valid['lon']
                )
                dist = line.s13
                for j in range(gap_start, gap_end):
                    prog = (points[j]['timestamp'] - last_valid['timestamp']).total_seconds()
                    frac = prog / total_secs
                    s = dist * frac
                    pos = line.Position(s, Geodesic.LATITUDE | Geodesic.LONGITUDE)
                    points[j]['lat'] = pos['lat2']
                    points[j]['lon'] = pos['lon2']
            elif last_valid:
                for j in range(gap_start, gap_end):
                    points[j]['lat'] = last_valid['lat']
                    points[j]['lon'] = last_valid['lon']
            elif next_valid:
                for j in range(gap_start, gap_end):
                    points[j]['lat'] = next_valid['lat']
                    points[j]['lon'] = next_valid['lon']

            i = gap_end + 1
        else:
            i += 1

    for pt in points:
        valid_records += 1
        trkpt = ET.SubElement(trkseg, 'trkpt')
        if pt['lat'] is not None:
            trkpt.set('lat', f"{pt['lat']:.7f}")
        if pt['lon'] is not None:
            trkpt.set('lon', f"{pt['lon']:.7f}")
        vals = pt['values']
        if vals.get('altitude') is not None:
            ele = ET.SubElement(trkpt, 'ele')
            ele.text = f"{vals['altitude']:.1f}"
        time_e = ET.SubElement(trkpt, 'time')
        time_e.text = pt['timestamp'].strftime('%Y-%m-%dT%H:%M:%SZ')
        ext = ET.SubElement(trkpt, 'extensions')
        tpe = ET.SubElement(ext, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}TrackPointExtension')
        if vals.get('temperature') is not None:
            at = ET.SubElement(tpe, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}atemp')
            at.text = str(int(vals['temperature']))
        if vals.get('heart_rate') is not None:
            hr = ET.SubElement(tpe, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}hr')
            hr.text = str(int(vals['heart_rate']))
        if vals.get('cadence') is not None:
            cad = ET.SubElement(tpe, '{http://www.garmin.com/xmlschemas/TrackPointExtension/v1}cad')
            cad.text = str(int(vals['cadence']))
        if vals.get('power') is not None and vals['power'] > 0:
            pw = ET.SubElement(ext, 'power')
            pw.text = str(int(vals['power']))

    rough = ET.tostring(gpx, encoding='utf-8')
    reparsed = minidom.parseString(rough)
    pretty = reparsed.toprettyxml(indent=' ')
    with open(gpx_file, 'w', encoding='utf-8') as f:
        lines = [ln for ln in pretty.split('\n') if ln.strip()]
        f.write('\n'.join(lines))

    print(f"\nConversion Summary:")
    print(f"Total records processed: {total_records}")
    print(f"Valid points written: {valid_records}")
    print(f"Points skipped: {skipped_records}")
    print("\nSkipped due to missing:")
    for reason, count in skipped_reasons.items():
        if count:
            print(f"- {reason}: {count} points")
    print(f"\n✅ Successfully converted {fit_file} to {gpx_file}")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python3 convert_fit.py input.fit output.gpx")
        sys.exit(1)
    fit_to_gpx(sys.argv[1], sys.argv[2])