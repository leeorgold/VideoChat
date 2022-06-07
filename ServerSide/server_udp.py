# This is server code to send video frames over UDP
# import base64
import time
import numpy as np
import cv2
import imutils
import socket
from threading import Thread

BUFF_SIZE = 65536
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '0.0.0.0'  # socket.gethostbyname(host_name)
# print(host_ip)
port = 9999
socket_address = (host_ip, port)
server_socket.bind(socket_address)
print('Listening at:', socket_address)
packet, client_addr = server_socket.recvfrom(BUFF_SIZE)
while packet != b'hello server':
    packet, client_addr = server_socket.recvfrom(BUFF_SIZE)
server_socket.sendto(b'hello client', client_addr)
print('Received connection from:', client_addr)

vid = cv2.VideoCapture(0)


def receiver(sock: socket.socket):
    while True:
        packet, addr = sock.recvfrom(BUFF_SIZE)
        if addr == client_addr:
            npdata = np.frombuffer(packet, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            cv2.imshow("RECEIVING VIDEO", frame)
            cv2.waitKey(1)


Thread(target=receiver, daemon=True, args=[server_socket]).start()

while vid.isOpened():
    read_successfully, frame = vid.read()
    if read_successfully:
        frame = imutils.resize(frame, width=400)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        message = np.array(buffer).tobytes()
        # print(f'{len(message) = }')
        server_socket.sendto(message, client_addr)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            server_socket.close()
            break

time.sleep(.1)