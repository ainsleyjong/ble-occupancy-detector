from ubluetooth import BLE
import ble_helper
import time

ble = BLE()
ble.active(True)

# Choose a unique name per board, e.g. "Beacon-1", "Beacon-2"
DEVICE_NAME = "Beacon-1"

adv_payload = ble_helpers.advertising_payload(name=DEVICE_NAME)

# Start advertising every 100 ms (100_000 µs)
ble.gap_advertise(100_000, adv_payload)

print("Advertising as", DEVICE_NAME)
# Nothing more to do—just keep the script alive
while True:
    time.sleep(60)
