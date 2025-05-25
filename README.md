# GPX Power Filter

This tool filters a GPX file and removes all track points that do not contain power data. If your headunit stopps recording when power is out, it will create new entries at the end of the track while recovering the file -> we have to delete these to be able to combine the 2 files later.

## Features

- Keeps only `<trkpt>` entries that contain a `<power>` tag inside `<extensions>`
- Logs distinct minutes of all removed entries for audit/debug purposes

## Requirements

- Python 3.7+
- No third-party dependencies (uses `xml.etree.ElementTree`)

## Usage

### 1. Run directly

```bash
python3 filter_power.py input.gpx output.gpx
```

# GPX Track Merger

Merges two GPX files into one, appending only trackpoints from the second file that are **newer** than the last timestamp in the first file.

## 🏁 Features

- Combines two GPX tracks (`<trkpt>`) into a single continuous track
- Ignores overlapping or duplicate timestamps from the second file
- Ensures clean and valid GPX 1.1 output
- Uses standard library only — no dependencies

## 🛠 Usage

### Merge two files

```bash
./merge_gpx.sh track1.gpx track2.gpx merged.gpx
```
