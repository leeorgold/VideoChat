import struct
from socket import socket


class ServerImageHandler:
    payload_size = struct.calcsize("Q")  # Q: unsigned long long integer(8 bytes)

    def __init__(self, sock: socket):
        self.sock = sock  # socket object witch is used to communicate with the client
        self.data = b''  # the data sent by the client
        self.frame = b''  # the latest image frame of the client

    def handle(self):
        """The method handles the communication with the client about the image."""
        while len(self.data) < self.payload_size:
            packet = self.sock.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
            if not packet: break
            self.data += packet  # append the data packet got from server into data variable
        packed_msg_size = self.data[:self.payload_size]  # will find the packed message size i.e. 8 byte.
        self.data = self.data[self.payload_size:]  # Actual frame data
        msg_size = struct.unpack("Q", packed_msg_size)[0]  # meassage size
        # print(msg_size)

        while len(self.data) < msg_size:
            self.data += self.sock.recv(4 * 1024)  # will receive all frame data from client socket
        self.frame = self.data[:msg_size]  # recover actual frame data
        self.data = self.data[msg_size:]
