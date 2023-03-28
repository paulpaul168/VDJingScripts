import socket
import struct
import time


class ArtNetNode:
    def __init__(self, name, ip, port):
        self.name = name
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def start(self):
        # Send a registration message to the SoundSwitch software
        msg = struct.pack(
            "!4s4s4s4s4s4sHBBH16s",
            b"S\0S\0",  # protocol
            b"\x00\x10",  # opcode
            b"\x00\x00\x00\x00",  # reserved
            self.ip.encode("ascii"),  # node IP address
            b"\x00\x00\x00\x00",  # reserved
            self.name.encode("ascii"),  # node short name
            0,  # node report rate
            0x00,  # node status 1
            0x00,  # node status 2
            self.port,  # node port
            "Art-Net".encode("ascii"),
        )  # node long name
        self.sock.sendto(msg, ("127.0.0.1", 6454))

        # Start listening for incoming ArtDMX packets
        while True:
            data, addr = self.sock.recvfrom(1024)
            opcode = (data[8] << 8) | data[9]
            if opcode == 0x5000:  # ArtDMX packet
                universe = data[14]
                channels = data[17]
                values = data[18 : 18 + channels]
                # Process the incoming packet data here


# Create an ArtNetNode object and start it
node = ArtNetNode("MyArtnetDevice", "127.0.0.1", 6454)
node.start()
