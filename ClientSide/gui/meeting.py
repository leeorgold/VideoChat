import tkinter

from ClientSide.gui.template import *
from PIL import ImageTk
import base64
import time
import numpy as np
import cv2
import imutils
import socket
from threading import Thread

BUFF_SIZE = 65536


def connect_to_server_images(host_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (host_ip, port)

    client_socket.sendto(b'hello server', server_addr)
    packet, addr = client_socket.recvfrom(1024)
    while addr != server_addr and packet != b'hello client':
        packet, addr = client_socket.recvfrom(1024)
    return client_socket, addr


def run_meeting():
    canvas.delete('all')
    exit_button = Button(canvas, image=exit_button_img, command=root.destroy, bd=0)
    exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=NE)
    canvas.create_text(20, 20, text="Cyberous - Meeting", font=('Cascadia Mono', 60, 'bold'), anchor=NW,
                       fill='white')

    sock, addr = connect_to_server_images('192.168.0.114', 9999)
    from ClientSide.audio import record, play

    vid = cv2.VideoCapture(0)
    run_thread(play)
    run_thread(sender, vid, sock, addr)
    run_thread(receiver, sock, addr)
    record()
    update_photos()


def run_thread(target, *args):
    Thread(target=target, daemon=True, args=(*args,)).start()


def sender(vid, sock, addr):
    while vid.isOpened():
        read_successfully, frame = vid.read()
        if read_successfully:
            ImageContainer.my_img2 = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            # canvas.create_image(1400, 700, image=ImageContainer.my_image)
            frame = imutils.resize(frame, width=400)
            encoded, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
            message = base64.b64encode(buffer)
            sock.sendto(message, addr)


def receiver(sock: socket.socket, addr):
    global my_labal
    while True:
        packet, received_addr = sock.recvfrom(BUFF_SIZE)
        if addr == received_addr:
            data = base64.b64decode(packet)
            npdata = np.frombuffer(data, dtype=np.uint8)
            frame = cv2.imdecode(npdata, 1)
            ImageContainer.other_img2 = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            # canvas.create_image(400, 700, image=ImageContainer.other_image)


def update_photos():
    ImageContainer.my_img = ImageContainer.my_img2
    canvas.create_image(1400, 700, image=ImageContainer.my_img)
    ImageContainer.other_img = ImageContainer.other_img2
    canvas.create_image(400, 700, image=ImageContainer.other_img)

    canvas.after(10, update_photos)


class ImageContainer:
    my_img = my_img2 = None
    other_img = other_img2 = None
