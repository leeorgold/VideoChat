# The client connects to the main server in a constant IP and a constant PORT.
# The main server will respond to the client with a json contains the following format:
# {
#     ip_address: <ip>,
#     video_port: <port>,
#     audio_port: <port>,
#     text_port: <port>
# }
#
#

# import socket
# from threading import Thread
#
#
# def run_as_a_thread(f):
#     """This function is for decorating. Calling the decorated function will run it as a thread."""
#     return Thread(target=f, daemon=True).start

from server_image_handler import ServerImageHandler
from itertools import count

class Participant:
    counter = count()

    def __init__(self, ip_address: str):
        self.name = f'temp{next(self.counter)}'
        self.ip_address = ip_address
        self.image_handler: ServerImageHandler = None

    def is_same_ip(self, ip_addr: str):
        return self.ip_address == ip_addr

    def set_image_handler(self, sock):
        self.image_handler = ServerImageHandler(sock)


