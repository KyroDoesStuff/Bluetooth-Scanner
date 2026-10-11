# Bluetooth LE Scanner

A Python-based Bluetooth Low Energy (BLE) scanner built using [Bleak](https://github.com/hbldh/bleak).

### Features
- Discovers nearby BLE devices.
- Displays device names, Bluetooth addresses, and signal strength (RSSI).
- Extracts manufacturer company IDs and displays possible manufacturer names.
- Displays advertised service UUIDs.
- Sorts scan results from strongest to weakest signal.
- Provides basic device identification using available advertising data.

### Tech Stack
- Python
- Bleak
- Asyncio

### Limitations
- Device names may be unavailable if not included in advertisements.
- Manufacturer IDs do not necessarily identify the physical device manufacturer.
- Exact device models cannot reliably be determined from advertising data alone.
- Devices using randomized Bluetooth addresses may appear as separate entries.
- Only BLE devices advertising during the scan window may be discovered.
- Signal strength varies with distance, obstacles, and interference, so RSSI is not an exact distance measurement.
