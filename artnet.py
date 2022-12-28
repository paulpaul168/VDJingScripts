import socket

# Create an Art-Net socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("", 6454))

# Receive Art-Net packets
while True:
    data, addr = sock.recvfrom(1024)

    # Parse the Art-Net packet
    opcode = data[0] | (data[1] << 8)  # Art-Net opcode is a 16-bit value
    protocol_version = data[2] | (data[3] << 8)
    sequence = data[4]
    physical = data[5]
    universe = data[6] | (data[7] << 8)
    net = data[8]
    length = data[9] | (data[10] << 8)
    payload = data[11:]

    # Print the packet information
    print(
        f"Received Art-Net packet from {addr} (opcode: {opcode}, universe: {universe}, length: {length})")

    # Enable unicast support
    if opcode == 0x5000:  # Art-Net OpPoll
        # Send an Art-Net OpPollReply packet
        reply_packet = b"\x00\x50\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        sock.sendto(reply_packet, addr)

    # Device detection
    if opcode == 0x6000:  # Art-Net OpAddress
        # Send an Art-Net OpAddressReply packet
        reply_packet = b"\x00\x61\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"
        sock.sendto(reply_packet, addr)
