# BLE Occupancy Detector

This project uses Bluetooth Low Energy (BLE) beacons and a scanner to detect room occupancy, sending the status over MQTT using Raspberry Pi Pico 2W.

## 📦 Project Structure

- `beacon.py` – Broadcasts a BLE advertisement with a unique name (e.g., `Beacon-1`)
- `scanner.py` – Scans for BLE beacons, determines occupancy, and publishes status to MQTT
- `ble_helper.py` – Utility functions for BLE advertisement and name decoding

## 🛠 Requirements

- MicroPython-compatible board (e.g., ESP32, Pico W)
- BLE support
- Wi-Fi access
- MQTT broker (e.g., [HiveMQ](https://www.hivemq.com/public-mqtt-broker/))

## 📡 How It Works

1. Beacons advertise a BLE signal with a unique name like `Beacon-1`.
2. The scanner listens for BLE devices with names starting with `Beacon-`.
3. If a beacon is seen with RSSI above a threshold, the room is marked as "occupied".
4. Occupancy status is sent to an MQTT broker every 5 seconds.
