# import struct
from socket import socket
BUFF_SIZE = 1024*20

class ServerImageHandler:

    def __init__(self, sock: socket):
        self.sock = sock  # socket object witch is used to communicate with the client
        self.frame = b''  # the latest image frame of the client

    def handle(self):
        """The method handles the communication with the client about the image."""
        self.frame = self.sock.recv(BUFF_SIZE)
