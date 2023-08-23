import morse, unittest, asyncio
from datetime import datetime

class TestMorse(unittest.TestCase):
    tree = morse.MorseTree()
    tree.createTree()
    
    def test_default(self):
        self.assertEqual((morse.UDPdecode(b'AAAAAA8AF7lURVNUSU5H')), (True, 0, 0, 'TESTING'))#test UDP deocde
        
    def test_default_FAIL(self):
        self.assertEqual((morse.UDPdecode(b'FAAAAA8AF6VURVNUSU5H')), (True, 0, 0, 'TESTING'))#test UDP deocde FAIL for port 20 not 0
        
    def test_checksum(self):
        self.assertEqual(morse.compute_checksum(0, 0, b'TESTING'), morse.compute_checksum(0, 0, b'TESTING'))#same checksum
    
    def test_checksum_FAIL(self):
        self.assertEqual(morse.compute_checksum(0, 0, b'TESTING'), morse.compute_checksum(0, 0, b'TESTING 2'))#same checksum FAIL TESTING CHECKSUM
        
    def test_UDP_sending(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.assertEqual(asyncio.run(morse.send_UDP_TESTING(0, 542, b'1111')), (True, 542, 0, current_time))#check sending UDP
        
    def test_UDP_sending_FAIL_PORT(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.assertEqual(asyncio.run(morse.send_UDP_TESTING(0, 540, b'1111')), (True, 540, 0, current_time)) #FAIL DUE TO INCORRECT PORT
        
    def test_UDP_sending_FAIL_SOURCE(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.assertEqual(asyncio.run(morse.send_UDP_TESTING(999, 542, b'1111')), (True, 542, 999, current_time)) #FAIL DUE TO INCORRECT PAYLOAD
        
    print("2 fails expected")

if __name__ == '__main__':
    unittest.main()