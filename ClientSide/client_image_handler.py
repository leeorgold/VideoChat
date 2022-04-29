import pickle
from socket import socket
import struct
from .constants import IP_ADDRESS, IMAGE_PORT

import cv2


class ClientImageHandler:
    payload_size = struct.calcsize("Q")  # Q: unsigned long long integer(8 bytes)

    def __init__(self, sock: socket):
        self.sock = sock
        self.data = b""

    def receive_json_data(self):
        while len(self.data) < self.payload_size:
            packet = self.sock.recv(4 * 1024)  # 4K, range(1024 byte to 64KB)
            if not packet: break
            self.data += packet  # append the data packet got from server into data variable
        packed_msg_size = self.data[:self.payload_size]  # will find the packed message size i.e. 8 byte, we packed on server side.
        self.data = self.data[self.payload_size:]  # Actual frame data
        msg_size = struct.unpack("Q", packed_msg_size)[0]  # meassage size
        # print(msg_size)

        while len(self.data) < msg_size:
            self.data += client_socket.recv(4 * 1024)  # will receive all frame data from client socket
        frame_data = self.data[:msg_size]  # recover actual frame data
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data)  # de-serialize bytes into actual frame type


# create socket
client_socket = socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect((IP_ADDRESS, IMAGE_PORT))

# Business logic to receive data frames, and unpak it and de-serialize it and show video frame on client side
while True:

    cv2.imshow("RECEIVING VIDEO", frame)  # show video frame at client side
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):  # press q to exit video
        break
client_socket.close()
