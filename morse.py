import asyncio, websockets, aioconsole, time, base64
class Node():
    def __init__(self,value=''):
        self.value = value
        self.left = None
        self.right = None
        

class MorseTree():
    def __init__(self):
        self.root = Node()
        
    #just to create the initial tree
    def createTree(self):
        morseCode = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....', 'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.', 'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-', 'Y': '-.--', 'Z': '--..', '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '+': '.-.-.', '/': '-..-.', '=': '-...-', '.': '.-.-.-', '(': '-.--.', ')': '-.--.-', ',': '--..--', '?': '..--..', "'": '.----.', ':': '---...', '-': '-....-', '/': '-..-.', '!': '-.-.--', '@': '.--.-.', ';': '-.-.-.', '&': '.-...', '_': '..--.-', '"': '.-..-.', '$': '...-..-', ' ': '/'}
        for x in morseCode: #loops through the dict
            cur = self.root
            for char in morseCode[x]: #loops through each "morse"
                if char == '.':
                    if cur.left == None:
                        cur.left = Node()
                    cur = cur.left
                    
                elif char == '-':
                    if cur.right == None:
                        cur.right = Node()
                    cur = cur.right
            
            #check if node is taken
            if cur.value == "":
                cur.value = x
            else:
                print("Error, atleast 2 characters have the same code")
                exit()
            
    #pre order traversal
    def getMorse(self, node, character, code):
        if node == None:
            return False
        
        elif node.value == character:
            return True
        
        else:
            if self.getMorse(node.left, character, code):
                print(code)
                code.insert(0, ".")
                return True
            elif self.getMorse(node.right, character, code):
                code.insert(0, "-")
                return True

    #encode function
    def encode(self, message):
        encodedMessage = ''
        morse = []
        node = self.root
                
        for char in message.upper():
            print(char)
            if char == " ":
                encodedMessage += "/ "
            else:
                self.getMorse(node, char, morse)
                encodedMessage += "".join(morse) + " "
                morse = []
                
        return encodedMessage.rstrip()
    
    #decode function
    def decode(self, message):
        cur = self.root
        decodedMessage = ''
        
        #loop through each stroke
        for char in message:
            
            if char == '.' and cur.left != None:
                cur = cur.left
                
            elif char == '-' and cur.right != None:
                cur = cur.right
                
            elif char == ' ':
                #at a space log letter
                decodedMessage = decodedMessage + cur.value
                cur = self.root
        
        #when end ofmessage
        decodedMessage = decodedMessage + cur.value
        return decodedMessage

tree = MorseTree()
tree.createTree() #shortcut to create tree quicker

client = ''
uri = "ws://localhost:10102"

#---=== Worksheet 3 ===---
async def udpFetch():
    async with websockets.connect(uriUDP) as websocket:
        rawMsg = await websocket.recv()
        #decode the message recieved
        UDPdecode(rawMsg)
        print(rawMsg)
            
def UDPdecode(rawMsg):
    print("Base64: ",rawMsg)
    
    packet = base64.b64decode(rawMsg)
    print("Server sent: ", packet)
    
    source_port = int.from_bytes(packet[0:2], 'little')
    print("Source Port: ", source_port)
    
    dest_port = int.from_bytes(packet[2:4], 'little')
    print("Dest Port: ", dest_port)
    
    msgLen = int.from_bytes(packet[4:6], 'little')
    print("Data Length: ", msgLen)
    print("Checksum: ", int.from_bytes(packet[6:8], 'little'))
    
    payload = packet[8:(msgLen+8)].decode("utf-8")
    print("Payload: ", payload)
    
    #check the checksum
    print("-========-")
    checked = compute_checksum(source_port, dest_port, packet[8:(msgLen+8)])
    if checked == int.from_bytes(packet[6:8], 'little'):
        print("RECIEVED SCORE: ", int.from_bytes(packet[6:8], 'little'))
        print("CHECKED SCORE: ", checked)
        print("-= TRUE =-")
        #return for testing
        return(True, source_port, dest_port, payload)
    else:
        print("RECIEVED SCORE: ", int.from_bytes(packet[6:8], 'little'))
        print("CHECKED SCORE: ", checked)
        print("-= FLASE =-")
        #return for testing
        return(False, source_port, dest_port, payload)
    
#W3T2
#testing binary checkscore
    
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

print("\n---=== UDP server ===---")
uriUDP = "ws://localhost:5612"
asyncio.run(udpFetch())

#W3T3
async def recv_and_decode_packet(websocket):
    response = await websocket.recv()
    return(UDPdecode(response))

async def send_packet(websocket, source: int, dest: int, payload):
    checksum = compute_checksum(source, dest, payload)
    size = 8 + len(payload)
    
    packet = bytearray()
    packet += source.to_bytes(2, byteorder="little")
    packet += dest.to_bytes(2, byteorder="little")
    packet += size.to_bytes(2, byteorder="little")
    packet += checksum.to_bytes(2, byteorder="little")
    packet += payload
    encoded = base64.b64encode(packet)
    print(packet)
    print(encoded)
    await websocket.send(encoded)
    print("---=== PACKET SENT ===---")

async def send_UDP():
    async with websockets.connect(uriUDP) as websocket:
        await (recv_and_decode_packet(websocket))
        while True:
            print("\n---=== TIME UPDATE ===---")
            await send_packet(websocket, 0, 542, b'1111')
            print(await recv_and_decode_packet(websocket))
            
            time.sleep(10)
            
async def send_UDP_TESTING(source, dest, payload):
    async with websockets.connect(uriUDP) as websocket:
        await (recv_and_decode_packet(websocket))
        print("\n---=== TIME UPDATE ===---")
        await send_packet(websocket, source, dest, payload)
        return (await recv_and_decode_packet(websocket))

print("\n---=== UDP ===---")
#asyncio.run(send_UDP()) #COMMENT OUT FOR TESTING