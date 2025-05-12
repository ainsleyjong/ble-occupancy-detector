import struct

# Build a BLE advertising payload with just a device name
def advertising_payload(name=None):
    payload = bytearray()
    def _append(adv_type, value):
        payload.extend(struct.pack("BB", len(value) + 1, adv_type) + value)
    if name:
        _append(0x09, name.encode())       # Complete Local Name
    return payload

# Scan data parser: extract the Complete Local Name (0x09) if present
def decode_name(adv_data):
    i = 0
    mv = adv_data
    while i + 1 < len(mv):
        length = mv[i]
        if length == 0:
            break
        ad_type = mv[i + 1]
        if ad_type == 0x09:  # Complete Local Name
            start = i + 2
            end = i + 1 + length
            # cast to bytes before decoding
            return bytes(mv[start:end]).decode('utf-8')
        i += 1 + length
    return None

