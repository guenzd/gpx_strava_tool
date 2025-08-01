# GPX Tools for Strava

A collection of tools for handling GPX files, particularly useful when dealing with power meter data and interrupted recordings from bike computers (like Wahoo).

## 🔋 GPX Power Filter

This tool helps clean up GPX files when your power meter or bike computer has connectivity issues.

### Problem It Solves

When a power meter loses connection:

1. Your bike computer might stop recording
2. Upon reconnection, it creates new entries at the end of the track
3. This creates a discontinuous track that needs cleanup before uploading to Strava

### Features

- Filters out track points (`<trkpt>`) that don't have power data
- Keeps only valid power readings inside `<extensions>` tags
- Logs removed entries by timestamp for verification
- Preserves all other data (GPS coordinates, elevation, cadence, etc.)

### Usage

```bash
# Using the Python script directly
python3 filter_power.py input.gpx output.gpx

# Or use the convenience shell script
./filter_power.sh input.gpx output.gpx
```

## 🔄 GPX Track Merger

Merges two GPX files into one continuous track. Useful for recovering rides where recording was interrupted.

### Common Use Cases

1. **Started Recording Too Late**

   - You began riding but forgot to start recording
   - Started a backup recording on another device
   - Use `started_too_late.sh` to prepend the missing beginning

2. **Stopped Recording Early**
   - Device died or crashed (e.g., Wahoo battery died)
   - Had a backup recording running
   - Use `stopped_too_early.sh` to append the missing end

### Features

- Smart timestamp handling:
  - Removes duplicate timestamps
  - Ensures chronological ordering
  - Maintains GPS accuracy
- Preserves all track metadata and extensions
- Creates valid GPX 1.1 output
- No external dependencies

### Usage

```bash
# If you started recording too late:
./started_too_late.sh original.gpx early_portion.gpx merged.gpx

# If your device died and you need to append data:
./stopped_too_early.sh main_recording.gpx additional_data.gpx merged.gpx
```

## 🔄 FIT to GPX Converter

Converts Garmin FIT files to GPX format while preserving all important data.

### Features

- Converts FIT files from Garmin, Wahoo, and other devices
- Preserves all important data:
  - GPS coordinates with high precision
  - Elevation data
  - Heart rate, cadence, and temperature
  - Power meter readings
- Automatically detects activity type
- Creates standards-compliant GPX 1.1 files

### Usage

```bash
# Using the Python script directly
python3 convert_fit.py input.fit output.gpx

# Or use the convenience shell script (automatically installs fitparse if needed)
./convert_fit.sh input.fit output.gpx
```

## ⚙️ Requirements

- Python 3.7 or newer
- Base functionality: No dependencies (uses standard `xml.etree.ElementTree`)
- FIT conversion: `fitparse` library (auto-installed by conversion script)
- Unix-like environment (for shell scripts)

## 📝 File Format Support

- Supports GPX 1.1
- Handles Garmin extensions (`TrackPointExtension`)
- Compatible with most bike computer exports (Wahoo, Garmin, etc.)
- Preserves power, cadence, temperature, and other sensor data

## 🤝 Contributing

Issues and pull requests are welcome! Please ensure:

- Your code works with the standard library only
- You maintain compatibility with existing GPX formats
- You include test cases for new features
