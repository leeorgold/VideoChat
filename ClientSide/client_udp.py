
# import base64
import time
import numpy as np
import cv2
import imutils
import socket
from threading import Thread

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
host_name = socket.gethostname()
host_ip = '172.19.231.25'  # socket.gethostbyname(host_name)
# print(host_ip)
port = 9999
server_addr = (host_ip, port)

client_socket.sendto(b'hello server', server_addr)
packet, addr2 = client_socket.recvfrom(BUFF_SIZE)
while addr2 != server_addr and packet != b'hello client':
    packet, addr2 = client_socket.recvfrom(BUFF_SIZE)


vid = cv2.VideoCapture(0)
fps, st, frames_to_count, cnt = (0, 0, 20, 0)


# def receiver(sock: socket.socket):
#     while True:
#         packet, addr = sock.recvfrom(BUFF_SIZE)
#         if addr == server_addr:
#             data = base64.b64decode(packet)
#             npdata = np.frombuffer(data, dtype=np.uint8)
#             frame = cv2.imdecode(npdata, 1)
#
#             cv2.imshow("RECEIVING VIDEO", frame)
#             key = cv2.waitKey(1) & 0xFF


def receiver(sock: socket.socket):
    while True:
        packet, addr = sock.recvfrom(BUFF_SIZE)
        if addr == server_addr:
            # data = base64.b64decode(packet)
            npdata = np.frombuffer(packet, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)

            cv2.imshow("RECEIVING VIDEO", frame)
            key = cv2.waitKey(1) & 0xFF


Thread(target=receiver, daemon=True, args=[client_socket]).start()

while vid.isOpened():
    read_successfully, frame = vid.read()
    if read_successfully:
        # frame = imutils.resize(frame, width=400)
        encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        # message = base64.b64encode(buffer)
        message = np.array(buffer).tobytes()
        client_socket.sendto(message, server_addr)
        cv2.imshow('TRANSMITTING VIDEO', frame)
        key = cv2.waitKey(1) & 0xFF
        # if key == ord('q'):
        #     client_socket.close()
        #     break

time.sleep(.1)


