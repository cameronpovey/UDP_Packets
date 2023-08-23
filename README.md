# UDP Packets

### Worksheets
* [Worksheet 2 - Part 1 Link](https://github.com/cameronpovey/MorseCodeDecoder)
* [Worksheet 2 - Part 2 Link](https://github.com/cameronpovey/BinaryHeaps)


### Index
* [Development](#development-1)
    * [Decoding UDP](#decoding-udp---task-1)
    * [Compute Checksum](#compute-checksum---task-2)
    * [Sending UDP](#time-udp---task-3)
* [How to run](#how-to-run)
* [Testing](#testing)



# Development [^1]
## Decoding UDP - Task 1
To begin this worksheet I create a function to decode a UDP message fetched from the server. To begin this section I fetched the raw message using the websockets `websocket.recv()` as normal, fom this I was able to decode the Base64 message into encoded bytes, this was done with the base64 module using `base64.b64decode(rawMsg)`, using this I could split the code up accordingly using python's slice notation for example `packet[0:2]` to find the Source Port, this was done in 2's for the first 8 bytes, slicing the code into 4 different ouputs of the function Source Port, Destination Port, Data Length and Checksum.

### Input/Ouput
``` python
async def udpFetch():
    async with websockets.connect(uriUDP) as websocket:
        rawMsg = await websocket.recv()
        UDPdecode(rawMsg)

asyncio.run(udpFetch())
```
![UDP Decoding]()

## Compute Checksum - Task 2
To confirm the check sum of the recieved packet a `compute_checksum(source_port: int, dest_port: int, payload: bytearray) -> int` function is created. To figure out the total sum of the packet we will recieve we first need to define an empty `bytearray()` variable, after this the total size is defiend by adding 8 onto the length of the previously assigned payload. The Size, Source and Destination is then converted to bytes and added to the byte array along with the payload. If the size of the packet is an odd number an empty byte is added onto the end `packet += b'\x00'`. Then, in pars, values are combined, the first value being shifted 8bits to form a 16bit value. With this we can add the lowest 16 bits and the highest together to account for any overflow that may have occured with `(pairs & 0xFFFF) + (pairs >> 16)` we then figure out the one's complement to return the calculated checksum `return(~pairs & 0xFFFF)`.

### Input/Ouput
``` python
compute_checksum(10, 25, "Welcome to the IoT UDP Server")
```
![compute_checksum]()

## Time UDP - Task 3
To complete Task 3, I started by defining a connection and decoding the response to get the initial welcome message, within the `recv_and_decode_packet` function I call the decode function that was created previously to seperate the data and call the `compute_checksum` function. After this the original function to get the time uses a while loop where the `send_packet(websocket, source: int, dest: int, payload)` function is called which is used the send the packet with the revelevent information in, using the `compute_checksum` for the checksum and using the values passed and converting them into bytes with `foo.to_bytes(2, byteorder="litte")` after all of these being encoded we can send the message to the server. Once recieved the same process is used to decode the orginal message to process the message recieved.

> `time.sleep(10)` is used to create a gap within the code.

### Input/Ouput
``` python
asyncio.run(send_UDP())

async def send_UDP():
    async with websockets.connect(uriUDP) as websocket:
        await (recv_and_decode_packet(websocket))
        while True:
            print("\n---=== TIME UPDATE ===---")
            await send_packet(websocket, 0, 542, b'1111')
            await recv_and_decode_packet(websocket)
            
            time.sleep(10)
```
![compute_checksum]()

# How to run
This git comes with two files, a test file and the main morse.py where the morse code takes place. This codes only requirements is a valid version of python, preferably python 3.

> This code was written on python 3.8.10

Test file:
To run the test file, main.py, ensure the morse.py is in the same directory or adjust the file accordingly.

Morse file:
* aioconsole - 0.6.1
* websockets - 11.0

>If using testing file ensure the `morse.py` line 212 is commented out to prevent endless loop before testing, if using normal `morse.py` ensure the line is un-commented.

# Testing
To test out my morse code I created 7 different tests, I used a python3 script, included in the git repository, This let me adjust the inputs with ease. I wanted to test the limitations of my code and how well it can handle certain curveballs thrown at it, here are the tests I ran with the ideal ouput and actual output:
Input | Tested ouput | Actual Output | Functional | Testing
------------- | ------------- | ------------- | ------------- | -------------
`morse.UDPdecode(b'AAAAAA8AF7lURVNUSU5H')` | `(True, 0, 0, 'TESTING')` | `(True, 0, 0, 'TESTING')` | ✅ | Simple UDP Decoding
`morse.UDPdecode(b'AAAAAA8AF7lURVNUSU5H')` | `(True, 20, 0, 'TESTING')` | `(True, 0, 0, 'TESTING')` | ❌ | Simple UDP - FAIL EXPECTED - TESTING UDP ACCURACY
`compute_checksum(0, 0, b'TESTING')` | `compute_checksum(0, 0, b'TESTING') #47383` | `compute_checksum(0, 0, b'TESTING') #47383` | ✅ | Checksum CHECK - TESTING CHECKSUM ACCURACY
`compute_checksum(0, 0, b'TESTING')` | `compute_checksum(0, 0, b'TESTING 2') #34039` | `compute_checksum(0, 0, b'TESTING') #47383` | ❌ | Checksum CHECK - FAIL EXPECTED - TESTING CHECKSUM ACCURACY
`send_UDP_TESTING(0, 542, b'1111')` | `(True, 542, 0, current_time)` | `(True, 542, 0, current_time)` | ✅ | Checking sending UDP
`send_UDP_TESTING(0, 542, b'1111')` | `(True, 540, 0, current_time)` | `ERROR` | ❌ | Expected fail - Incorrect payload
`send_UDP_TESTING(999, 542, b'1111')` | `(True, 540, 999, current_time)` | `(True, 540, 0, current_time)` | ❌ | Expected pass - Source port will reset to 0(destination port) when sending


> The `main.py` file, when run, expected to return 3 out of 7 errors but should return 4 out of 7


---
[^1]: Within some of the snippets the comments and code have been altered for ease of reading, but will still function
