import base64

def compute_checksum(source_port: int, dest_port: int, payload: bytearray) -> int:
    packet = bytearray()
    size = 8 + len(payload)
    size = size.to_bytes(2, byteorder='little')
    source = source_port.to_bytes(2, byteorder='little')
    dest = dest_port.to_bytes(2, byteorder='little')
    
    packet += dest + source + size + payload
    
    #make even
    if len(packet)%2 == 1:
        packet += b'\x00'
    
    #combine into 16bits
    pairs = 0
    for i in range(0, len(packet), 2):
        pairs += (packet[i] << 8) + (packet[i+1])
    
    #handle overflow
    pairs = (pairs & 0xFFFF) + (pairs >> 16)
    #1s comp
    return(~pairs & 0xFFFF)

#CHANGE INPUT FOR TESTING INPUTS HERE
payload=b'TESTING'
source_port=20
dest_port=0

size = 8 + len(payload)
checksum = compute_checksum(source_port, dest_port, payload)

packet = bytearray()
packet += source_port.to_bytes(2, byteorder="little")
packet += dest_port.to_bytes(2, byteorder="little")
packet += size.to_bytes(2, byteorder="little")
packet += checksum.to_bytes(2, byteorder="little")
packet += payload


encoded = base64.b64encode(packet)
en_bytes = int.from_bytes((encoded), byteorder='little')

print("B64: ", encoded)#base64
print("BYTES: ",en_bytes)#recieved
print("source: ", source_port)
print("dest: ", dest_port)
print("payload: ", payload)
print("checksum: ", checksum)