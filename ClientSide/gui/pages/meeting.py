# import tkinter

from template import *
from PIL import Image, ImageTk
# import base64
import time
import numpy as np
import cv2
import imutils
import socket
from threading import Thread

BUFF_SIZE = 65536


def connect_to_server_images(host_ip, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_addr = (host_ip, 9999)

    client_socket.sendto(b'hello server', server_addr)
    packet, addr = client_socket.recvfrom(1024)
    while addr != server_addr and packet != b'hello client':
        packet, addr = client_socket.recvfrom(1024)
    return client_socket, addr


def run_meeting():
    canvas.delete('all')
    exit_button = tk.Button(canvas, image=exit_button_img, command=root.destroy, bd=0)
    # exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=NE)
    canvas.create_text(20, 20, text="Cyberous - Meeting", font=('Cascadia Mono', 60, 'bold'), anchor=tk.NW,
                       fill='white')

    sock, addr = connect_to_server_images('192.168.0.109', 9999)
    # from ClientSide.audio import record, play

    vid = cv2.VideoCapture(0)
    # run_thread(play)
    run_thread(sender, vid, sock, addr)
    run_thread(receiver, sock, addr)
    # record()

    update_photos()


def run_thread(target, *args):
    Thread(target=target, daemon=True, args=(*args,)).start()


def sender(vid, sock, addr):
    """The function grabs a new frame of the camera and sends it to the other client.
    :param vid - connection to the camera
    :param sock - socket connection
    :param addr - address to send the image. (a tuple with ipv4 address and a port number)"""

    while vid.isOpened():
        read_successfully, frame = vid.read()
        if read_successfully:
            # saves a reference to the image
            my_image_container.img = frame
            # resizing the image
            frame = imutils.resize(frame, width=400)
            # compress image data formats in order to make network transfer easier
            message = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])[1]
            # send the photo to the other client
            sock.sendto(message, addr)


def receiver(sock, addr):
    """The function receives an image from the other client.
    :param sock - socket connection
    :addr - the other client address"""

    while True:
        # receives a packet
        packet, received_addr = sock.recvfrom(BUFF_SIZE)
        # if the packet received from the other client IP address and port
        if addr == received_addr:
            # converts the received bytes to a numpy array
            npdata = np.frombuffer(packet, dtype=np.uint8)
            # converts the numpy array to an image
            frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
            # saves a reference to the image
            other_image_container.img = frame


def update_photos():
    """The function updates the photos on the screen to create a video illusion"""

    # update the photos on the image containers
    my_image_container.update()
    other_image_container.update()

    # displaying the changes to the screen
    canvas.create_image(1400, 700, image=my_image_container.img)
    canvas.create_image(400, 700, image=other_image_container.img)

    # calling this function again after 10 milliseconds to update the screen again
    canvas.after(10, update_photos)


class ImageContainer:
    """This class is used to save a reference to the images in order to display them on the screen.
    without saving a reference, the garbage-collector will delete the images,
    witch results blinking images on the screen."""

    def __init__(self):
        """Initializing the object.
        self._received is used to save a reference to a new image.
        self._displayed is used to save a reference to the TK image displayed on the canvas."""
        self._received = None
        self._displayed = None

    @property
    def img(self):
        """Getter method. returns the TK image displayed on the canvas."""
        return self._displayed

    @img.setter
    def img(self, val):
        """Setter method. sets a new image to contain"""
        self._received = val

    def update(self):
        """This methods updates the displayed image to the newest image."""
        if self._received is not None:
            # converts to BGR because PhotoImage works with BGR format only.
            self._displayed = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self._received, cv2.COLOR_RGB2BGR)))


# creating the containers
my_image_container = ImageContainer()
other_image_container = ImageContainer()
