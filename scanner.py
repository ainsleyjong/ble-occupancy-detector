from umqtt.simple import MQTTClient
from ubluetooth import BLE
from micropython import const
import ble_helper, network, time, machine

# IRQ constants
IRQ_SCAN_RESULT   = const(5)

# Wi-Fi credentials
SSID     = '*****'
PASSWORD = '*****'

# MQTT settings
mqtt_broker     = "broker.hivemq.com"
mqtt_port       = 1883
mqtt_client_id  = b"rp2350_scanner_#"       # Unique # for scanner
OCCUPANCY_TOPIC = b"home/<room>/occupancy" # Publish to correct <room> accordingly

# Threshold and timing
RSSI_THRESHOLD     = -50
ANNOUNCE_INTERVAL  = 5000       # publish every 5 seconds
BEACON_TIMEOUT_MS  = 5000       # remove beacon after 5 seconds of silence

# State variables
last_seen = {}
last_pub = 0
led = machine.Pin("LED", machine.Pin.OUT)

# Connect to Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    print("Connecting to Wi-Fi...", end="")
    while not wlan.isconnected():
        print(".", end="")
        time.sleep(0.5)
    print("\nConnected with IP:", wlan.ifconfig()[0])

# MQTT setup
def connect_mqtt():
    client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_broker,
        port=mqtt_port
    )
    client.connect()
    print("Connected to MQTT broker")
    return client

# BLE IRQ handler
def bt_irq(event, data):
    global last_seen
    if event == IRQ_SCAN_RESULT:
        _, _, _, rssi, adv = data
        name = ble_helper.decode_name(adv)
        if name and name.startswith("Beacon-"):
            if rssi > RSSI_THRESHOLD:
                last_seen[name] = time.ticks_ms()

# BLE init
ble = BLE()
ble.active(True)
ble.irq(bt_irq)
ble.gap_scan(0, 30000, 30000)
print("<Room> scanner: looking for beacons…")

connect_wifi()
mqtt_client = connect_mqtt()

# Publish MQTT state
def publish_occupancy(is_occupied):
    payload = b"occupied" if is_occupied else b"vacant"
    mqtt_client.publish(OCCUPANCY_TOPIC, payload, retain=True)
    print(f"[{mqtt_client_id.decode()}] Published: {payload.decode()}")
    led.value(is_occupied)

# Main loop
while True:
    now = time.ticks_ms()

    # Remove expired beacons
    expired = [n for n, t in last_seen.items()
               if time.ticks_diff(now, t) > BEACON_TIMEOUT_MS]
    for n in expired:
        del last_seen[n]

    # Determine room occupancy
    occupied = bool(last_seen)

    # Publish at intervals
    if time.ticks_diff(now, last_pub) >= ANNOUNCE_INTERVAL:
        publish_occupancy(occupied)
        last_pub = now

    time.sleep(1)

