import json
import socket
import base64
from constants import IP_ADDRESS, IMAGE_PORT
import imutils
import cv2
import numpy as np



class ClientImageHandler:

    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((ip, port))
        self.data = {}
        self.vid = cv2.VideoCapture(0)
        self.frame = None
        self.to_send = self.last_sent = b''


    def receive_json_data(self):
        while True:
            length = self.sock.recv(8)
            length = int(length)
            # print(m:=self.sock.recv(1024*60))
            m=self.sock.recv(length).decode()
            # print(m)
            self.data = json.loads(m)
            # self.data = json.loads(self.sock.recv(1024*60))

    def grab_frame(self):
        while True:
            read_successfully, self.frame = self.vid.read()
            if read_successfully:
                self.frame = imutils.resize(self.frame, width=320)
                encoded, buffer = cv2.imencode('.jpg', self.frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
                self.to_send = base64.b64encode(buffer)

    def send_image(self):
        while True:
            if self.to_send and self.to_send != self.last_sent:
                self.sock.sendall(self.to_send)
                self.last_sent = self.to_send

    def display(self):
        while True:
            if self.frame is not None and self.frame.shape == (240, 320, 3):
                cv2.imshow('MY VIDEO', self.frame)  # will show video frame on server side.

            for name, data in self.data.items():
                data = base64.b64decode(data)
                data = np.frombuffer(data, dtype=np.uint8)
                if type(data) is np.ndarray and data.shape == (240, 320, 3):
                    frame = cv2.imdecode(data, 1)
                    try:
                        cv2.imshow(f"{name}", frame)
                    except Exception:
                        pass
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                exit()
