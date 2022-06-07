import base64
import socket
import numpy as np

import cv2

# create socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# host_ip = '192.168.99.1'  # paste your server ip address here
host_ip = '192.168.0.114'  # paste your server ip address here
port = 9999
print('TRYING TO CONNECT:', (host_ip, port))
client_socket.connect((host_ip, port))  # a tuple
data = b""
# payload_size = 8
BUFF_SIZE = 1024*20


#Business logic to receive data frames, and unpak it and de-serialize it and show video frame on client side
while True:
    packet = client_socket.recv(BUFF_SIZE)
    data = base64.b64decode(packet)
    npdata = np.frombuffer(data, dtype=np.uint8)
    frame = cv2.imdecode(npdata, 1)
    cv2.imshow("RECEIVING VIDEO", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        client_socket.close()
        break


client_socket.close()
