# import time
#
# from template import *
# from PIL import Image, ImageTk
# import numpy as np
# import cv2
# # import imutils
# import socket
# from threading import Thread
# import pyaudio
#
# BUFF_SIZE = 65536
# FORMAT = pyaudio.paInt16
# CHANNELS = 1
# RATE = 44100
# CHUNK = 1024
#
# camera_switch = False
#
#
# def udp_connection(mode, port, ip=None):
#     image_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     image_udp.settimeout(3)
#     if mode == 'join':
#         server_addr = (ip, port)
#         while True:
#             image_udp.sendto(b'hello client', server_addr)
#             print("sending 'hello client'")
#             try:
#                 packet, addr = image_udp.recvfrom(12)
#             except socket.timeout:
#                 print('waiting for response...')
#             else:
#                 if addr == server_addr and packet == b'hello client':
#                     break
#
#     else:
#         my_addr = ('0.0.0.0', port)
#         image_udp.bind(my_addr)
#         # print('Listening at:', socket_address)
#         while True:
#             try:
#                 packet, addr = image_udp.recvfrom(12)
#             except socket.timeout:
#                 print('waiting for client...')
#             else:
#                 if packet == b'hello client':
#                     image_udp.sendto(b'hello client', addr)
#                     break
#
#     image_udp.settimeout(None)
#     return image_udp, addr
#
#
# def handle_threads(mode, ip):
#     def on_off_camera():
#         global camera_switch
#         # nonlocal vid
#         #
#         # if camera_switch:
#         #     camera_switch = False
#         #     vid.release()
#         # else:
#         #     camera_switch = True
#         #     vid = cv2.VideoCapture(0)
#         camera_switch = not camera_switch
#         my_image_container.switch = camera_switch
#
#     msg = canvas.create_text(200, y // 2 - 10, text="",
#                              font=('Cascadia Mono', 40, 'bold'), anchor=tk.NW,
#                              fill='white')
#     if mode == 'host':
#         canvas.itemconfig(msg, text='Waiting fo another user to join...')
#     general = tcp_connection(mode=mode, ip=ip, port=9997)
#     print('general connection established')
#     img_sock, user_address = udp_connection(mode, 9999, ip)
#     print('img_sock connection established')
#     # audio_sock = tcp_connection(mode=mode, ip=ip, port=9998)
#     audio_sock = tcp_connection(mode=mode, ip=ip, port=9998)
#     canvas.delete(msg)
#     vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
#     # vid.release()
#     run_thread(image_sender, img_sock, vid, user_address)
#     run_thread(image_receiver, img_sock, user_address)
#
#     image_button = tk.Button(canvas, text="Turn on/off\nmy camera", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
#                              activebackground='#2060BD', fg='white',
#                              activeforeground='white', bd=3, command=on_off_camera)
#     canvas.create_window(x - 2, y - 180, anchor=tk.E, window=image_button)
#
#     audio = pyaudio.PyAudio()
#     run_thread(audio_receiver, audio, audio_sock)
#     # run_thread(audio_receiver, audio, audio_sock)
#     audio_sender(audio, audio_sock)
#
#     update_photos()
#
#
# def run_meeting_page(*, mode, ip=None, meeting_id=None):
#     assert mode == 'join' or mode == 'host', f'Unsupported mode. {mode = }.'
#     canvas.delete('all')
#     exit_button = tk.Button(canvas, image=exit_button_img, command=close_window, bd=0)
#     canvas.create_window(x - 24, 15, window=exit_button)
#     canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
#     # canvas.create_image(x - 50, 20, image=logo, anchor=NE)
#     canvas.create_text(20, 20, text="Cyberous - Meeting", font=('Cascadia Mono', 60, 'bold'), anchor=tk.NW,
#                        fill='white')
#     if mode == 'host':
#         canvas.create_text(20, 150, text=f"ID: {meeting_id}", font=('Cascadia Mono', 30, 'bold'), anchor=tk.NW,
#                            fill='white')
#
#     run_thread(handle_threads, mode, ip)
#
#
# def run_thread(target, *args):
#     Thread(target=target, daemon=True, args=(*args,)).start()
#
#
# def audio_receiver(audio, sock):
#     stream = audio.open(format=FORMAT,
#                         channels=CHANNELS,
#                         rate=RATE,
#                         output=True,
#                         frames_per_buffer=CHUNK)
#     while True:
#         stream.write(sock.recv(CHUNK))
#
#         # packet, addr = sock.recvfrom(CHUNK)
#         # if addr == real_addr:
#         #     stream.write(packet)
#
#
# def audio_sender(audio, sock):
#     def callback(in_data, frame_count, time_info, status):
#         sock.send(in_data)
#         # sock.sendto(in_data, addr)
#         return None, pyaudio.paContinue
#
#     recording_stream = audio.open(format=FORMAT,
#                                   channels=CHANNELS,
#                                   rate=RATE,
#                                   input=True,
#                                   frames_per_buffer=CHUNK,
#                                   stream_callback=callback)
#
#
# def image_sender(sock, vid, addr):
#     """The function grabs a new frame of the camera and sends it to the other client.
#     :param sock - socket connection
#     :param addr - address to send the image. (a tuple with ipv4 address and a port number)"""
#
#     while vid.isOpened():
#         if not camera_switch:
#             my_image_container.turn_off_image()
#         else:
#             read_successfully, frame = vid.read()
#             if read_successfully:
#                 # saves a reference to the image
#                 my_image_container.img = frame
#                 # resizing the image
#                 # frame = imutils.resize(frame, width=400)
#                 # compress image data formats in order to make network transfer easier
#
#                 my_image_container.img = frame
#
#         for quality in range(80, -1, -20):
#             try:
#                 message = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]
#                 # send the photo to the other client
#                 sock.sendto(message, addr)
#             except OSError:
#                 pass
#             else:
#                 break
#
#
# def image_receiver(sock: socket.socket, addr):
#     """The function receives an image from the other client.
#     :param sock - socket connection
#     :addr - the other client address"""
#
#     while True:
#         # receives a packet
#         packet, received_addr = sock.recvfrom(BUFF_SIZE)
#         # if the packet received from the other client IP address and port
#         if addr == received_addr:
#             # if packet == b'no image':
#             #     other_image_container.turn_off_image()
#
#             # else:
#             other_image_container.turn_on_image()
#             # converts the received bytes to a numpy array
#             npdata = np.frombuffer(packet, dtype=np.uint8)
#             # converts the numpy array to an image
#             frame = cv2.imdecode(npdata, cv2.IMREAD_COLOR)
#             # saves a reference to the image
#             other_image_container.img = frame
#
#
# def update_photos():
#     """The function updates the photos on the screen to create a video illusion"""
#
#     # update the photos on the image containers
#     my_image_container.update()
#     other_image_container.update()
#
#     # displaying the changes to the screen
#     # if my_image_container.switch:
#     my_image = canvas.create_image(500, 700, image=my_image_container.img)
#     # if other_image_container.switch:
#     other_image = canvas.create_image(1500, 700, image=other_image_container.img)
#
#     # calling this function again after 10 milliseconds to update the screen again
#     canvas.after(10, update_photos)
#
#
# def tcp_connection(*, mode=None, ip=None, port):
#     if mode == 'join':
#         tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         address = (ip, port)
#         tcp.connect(address)
#         return tcp
#     else:
#         tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         address = ('0.0.0.0', port)
#         tcp.bind(address)
#         tcp.listen(0)
#         conn, addr = tcp.accept()
#         return conn
#
#
# class ImageContainer:
#     """This class is used to save a reference to the images in order to display them on the screen.
#     without saving a reference, the garbage-collector will delete the images,
#     witch results blinking images on the screen."""
#
#     no_image = ImageTk.PhotoImage(image=Image.open(r"../images/no_photo.png"))
#     # no_image = tk.PhotoImage(file=r"../images/no_photo.png")
#
#     def __init__(self):
#         """Initializing the object.
#         self._received is used to save a reference to a new image.
#         self._displayed is used to save a reference to the TK image displayed on the canvas."""
#         self._received = None
#         self._displayed = self.no_image
#         self.switch = False
#
#     @property
#     def img(self):
#         """Getter method. returns the TK image displayed on the canvas."""
#         return self._displayed
#
#     @img.setter
#     def img(self, val):
#         """Setter method. sets a new image to contain"""
#         self._received = val
#
#     def update(self):
#         """This methods updates the displayed image to the newest image."""
#         if self._received is not None:
#             # converts to BGR because PhotoImage works with BGR format only.
#             self._displayed = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self._received, cv2.COLOR_RGB2BGR)))
#
#     def turn_off_image(self):
#         self.switch = False
#         self._received = None
#         self._displayed = self.no_image
#
#     def turn_on_image(self):
#         self.switch = True
#
#
# # creating the containers
# my_image_container = ImageContainer()
# other_image_container = ImageContainer()
import time

from template import *
from PIL import Image, ImageTk
import numpy as np
import cv2
# import imutils
import socket
from threading import Thread
import pyaudio

BUFF_SIZE = 65536
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

camera_switch = False




def image_connection(mode, ip=None):
    image_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    image_udp.settimeout(3)
    if mode == 'join':
        server_addr = (ip, 9999)
        while True:
            image_udp.sendto(b'hello client', server_addr)
            print("sending 'hello client'")
            try:
                packet, addr = image_udp.recvfrom(12)
            except socket.timeout:
                print('waiting for response...')
            else:
                if addr == server_addr and packet == b'hello client':
                    break

    else:
        my_addr = ('0.0.0.0', 9999)
        image_udp.bind(my_addr)
        # print('Listening at:', socket_address)
        while True:
            try:
                packet, addr = image_udp.recvfrom(12)
            except socket.timeout:
                print('waiting for client...')
            else:
                if packet == b'hello client':
                    image_udp.sendto(b'hello client', addr)
                    break

    return image_udp, addr


def handle_threads(mode, ip):
    def on_off_camera():
        global camera_switch
        # nonlocal vid

        if camera_switch:
            camera_switch = False
            my_image_container.turn_off_image()
            # vid.release()
        else:
            camera_switch = True
            # my_image_container
            # vid = cv2.VideoCapture(0)


    msg = canvas.create_text(200, y // 2 - 10, text="",
                             font=('Cascadia Mono', 40, 'bold'), anchor=tk.NW,
                             fill='white')
    if mode == 'host':
        canvas.itemconfig(msg, text='Waiting fo another user to join...')
    general = tcp_connection(mode=mode, ip=ip, port=9997)
    print('general connection established')
    img_sock, user_address = image_connection(mode, ip)
    print('img_sock connection established')
    audio_sock = tcp_connection(mode=mode, ip=ip, port=9998)
    canvas.delete(msg)
    vid = cv2.VideoCapture(0)
    run_thread(image_sender, img_sock, vid, user_address)
    run_thread(image_receiver, img_sock, user_address)

    image_button = tk.Button(canvas, text="Turn on/off\nmy camera", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=on_off_camera)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=image_button)

    audio = pyaudio.PyAudio()
    run_thread(audio_receiver, audio, audio_sock)
    audio_sender(audio, audio_sock)

    update_photos()


def run_meeting_page(*, mode, ip=None, meeting_id=None):
    assert mode == 'join' or mode == 'host', f'Unsupported mode. {mode = }.'
    canvas.delete('all')
    exit_button = tk.Button(canvas, image=exit_button_img, command=close_window, bd=0)
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=NE)
    canvas.create_text(20, 20, text="Cyberous - Meeting", font=('Cascadia Mono', 60, 'bold'), anchor=tk.NW,
                       fill='white')
    if mode == 'host':
        canvas.create_text(20, 150, text=f"ID: {meeting_id}", font=('Cascadia Mono', 30, 'bold'), anchor=tk.NW,
                           fill='white')

    run_thread(handle_threads, mode, ip)


def run_thread(target, *args):
    Thread(target=target, daemon=True, args=args).start()


def audio_receiver(audio, sock):
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
    while True:
        stream.write(sock.recv(CHUNK))


def audio_sender(audio, sock):
    def callback(in_data, frame_count, time_info, status):
        sock.send(in_data)
        return None, pyaudio.paContinue

    recording_stream = audio.open(format=FORMAT,
                                  channels=CHANNELS,
                                  rate=RATE,
                                  input=True,
                                  frames_per_buffer=CHUNK,
                                  stream_callback=callback)


def image_sender(sock, vid, addr):
    """The function grabs a new frame of the camera and sends it to the other client.
    :param sock - socket connection
    :param addr - address to send the image. (a tuple with ipv4 address and a port number)"""

    while vid.isOpened():
        read_successfully, frame = vid.read()
        if not camera_switch:
            time.sleep(1)
        elif read_successfully:
            # saves a reference to the image
            my_image_container.img = frame
            my_image_container.turned_off1 = my_image_container.turned_off2 = False
            # resizing the image
            # frame = imutils.resize(frame, width=400)
            # compress image data formats in order to make network transfer easier
            for quality in range(80, -1, -20):
                try:
                    message = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]
                    # send the photo to the other client
                    sock.sendto(message, addr)
                except OSError:
                    pass
                else:
                    break



def image_receiver(sock: socket.socket, addr):
    """The function receives an image from the other client.
    :param sock - socket connection
    :addr - the other client address"""

    while True:
        try:
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
        except socket.timeout:
            other_image_container.turn_off_image()



def update_photos():
    """The function updates the photos on the screen to create a video illusion"""

    # update the photos on the image containers
    my_image_container.update()
    other_image_container.update()

    # displaying the changes to the screen
    if my_image_container.turned_off1 and not my_image_container.turned_off2:
        canvas.create_image(500, 700, image=my_image_container.img)
        my_image_container.turned_off2 = True

    if other_image_container.turned_off1 and not other_image_container.turned_off2:
        canvas.create_image(500, 700, image=other_image_container.img)
        other_image_container.turned_off2 = True

    # calling this function again after 10 milliseconds to update the screen again
    canvas.after(10, update_photos)


def tcp_connection(*, mode=None, ip=None, port):
    if mode == 'join':
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = (ip, port)
        tcp.connect(address)
        return tcp
    else:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        address = ('0.0.0.0', port)
        tcp.bind(address)
        tcp.listen(0)
        conn, addr = tcp.accept()
        return conn


class ImageContainer:
    """This class is used to save a reference to the images in order to display them on the screen.
    without saving a reference, the garbage-collector will delete the images,
    witch results blinking images on the screen."""

    # no_image = np.zeros((640, 480, 3), dtype=np.uint8)
    no_image = tk.PhotoImage(file=r"../images/no_photo.png")

    def __init__(self):
        """Initializing the object.
        self._received is used to save a reference to a new image.
        self._displayed is used to save a reference to the TK image displayed on the canvas."""
        self._received = None
        self._displayed = self.no_image
        self.turned_off1 = True
        self.turned_off2 = False

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

    def turn_off_image(self):
        self._displayed = self.no_image
        self._received = None
        self.turned_off1 = True


# creating the containers
my_image_container = ImageContainer()
other_image_container = ImageContainer()

my_image_container.turn_off_image()
other_image_container.turn_off_image()
