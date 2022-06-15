import time

from template import *
from PIL import Image, ImageTk
import numpy as np
import cv2
# import imutils
import socket
from threading import Thread
import pyaudio
from tkinter.messagebox import showinfo

from user_page import run_user_page

BUFF_SIZE = 65536
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

camera_switch = False
leaving = False
general = None
recording = False


def reset():
    global camera_switch, leaving, general, recording

    camera_switch = False
    leaving = False
    general = None
    recording = False


mic_on = tk.PhotoImage(file='../images/microphone-on.png')
mic_off = tk.PhotoImage(file='../images/microphone-off.png')
img_on = tk.PhotoImage(file='../images/video-on.png')
img_off = tk.PhotoImage(file='../images/video-off.png')


def image_connection(mode, ip=None):
    image_udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    image_udp.settimeout(3)
    if mode == 'join':
        server_addr = (ip, 9999)
        while not leaving:
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
        while not leaving:
            try:
                packet, addr = image_udp.recvfrom(12)
            except socket.timeout:
                print('waiting for client...')
            else:
                if packet == b'hello client':
                    image_udp.sendto(b'hello client', addr)
                    break

    if not leaving:
        return image_udp, addr
    return None, None


def handle_threads(mode, ip):
    global general

    msg = canvas.create_text(200, y // 2 - 10, text="",
                             font=('Cascadia Mono', 40, 'bold'), anchor=tk.NW,
                             fill='white')
    if mode == 'host':
        canvas.itemconfig(msg, text='Waiting fo another user to join...')
    general = tcp_connection(mode=mode, ip=ip, port=9997)
    if leaving:
        return None
    print('general connection established')
    img_sock, user_address = image_connection(mode, ip)
    if leaving:
        return None
    print('img_sock connection established')
    audio_sock = tcp_connection(mode=mode, ip=ip, port=9998)
    if leaving:
        return None
    canvas.delete(msg)
    vid = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    run_thread(send_status, general)
    run_thread(image_sender, img_sock, vid, user_address)
    run_thread(image_receiver, img_sock, user_address)
    run_thread(listen_for_leaving, general)

    audio = pyaudio.PyAudio()
    run_thread(audio_receiver, audio, audio_sock)
    audio_sender(audio, audio_sock)
    update_photos()


def run_meeting_page(*, mode, ip=None, meeting_id=None):
    global leaving
    leaving = False
    assert mode == 'join' or mode == 'host', f'Unsupported mode. {mode = }.'

    reset()

    def on_off_camera():
        global camera_switch
        if camera_switch:
            image_button.configure(image=img_off)
            camera_switch = False
        else:
            image_button.configure(image=img_on)
            camera_switch = True

    def change_recording():
        global recording
        if recording:
            recording = False
            record_button.configure(image=mic_off)
        else:
            recording = True
            record_button.configure(image=mic_on)

    clear_window()

    canvas.create_text(250, 20, text="Cyberous - Meeting", font=('Cascadia Mono', 60, 'bold'), anchor=tk.NW,
                       fill='white')

    leave_button = tk.Button(canvas, text="Leave Meeting", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=leave)
    canvas.create_window(x - 2, 180, anchor=tk.E, window=leave_button)

    record_button = tk.Button(canvas, bg='#15478F', activebackground='#2060BD', image=mic_off, bd=0,
                              command=change_recording)
    canvas.create_window(x // 2 + 300, y - 140, anchor=tk.W, window=record_button)

    image_button = tk.Button(canvas, bg='#15478F', activebackground='#2060BD', image=img_off, bd=0,
                             command=on_off_camera)
    canvas.create_window(x // 2 - 300, y - 140, anchor=tk.E, window=image_button)

    if mode == 'host':
        canvas.create_text(20, 150, text=f"ID: {meeting_id}", font=('Cascadia Mono', 30, 'bold'), anchor=tk.NW,
                           fill='white')

    run_thread(handle_threads, mode, ip)


def run_thread(target, *args):
    t = Thread(target=target, daemon=True, args=args)
    t.start()
    return t


def audio_receiver(audio, sock):
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        output=True,
                        frames_per_buffer=CHUNK)
    while not leaving:
        try:
            stream.write(sock.recv(CHUNK))
        except ConnectionError:
            stream.close()
            break


def audio_sender(audio, sock):
    def callback(in_data, frame_count, time_info, status):
        if leaving:
            return None, pyaudio.paComplete
        try:
            if recording:
                sock.send(in_data)
        except ConnectionError:
            stream.close()
            return None, pyaudio.paComplete
        else:
            return None, pyaudio.paContinue

    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK,
                        stream_callback=callback)


def image_sender(sock, vid, addr):
    """The function grabs a new frame of the camera and sends it to the other client.
    :param sock - socket connection
    :param addr - address to send the image. (a tuple with ipv4 address and a port number)"""

    while not leaving and vid.isOpened():
        read_successfully, frame = vid.read()
        if not camera_switch:
            my_image_container.img = None
            time.sleep(1)
        elif read_successfully:

            # saves a reference to the image
            my_image_container.img = frame

            # compress image data formats in order to make network transfer easier
            for quality in range(80, -1, -20):
                try:
                    message = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, quality])[1]
                    # send the photo to the other client
                    sock.sendto(message, addr)

                # for big images
                except OSError:
                    pass
                else:
                    break


def image_receiver(sock: socket.socket, addr):
    """The function receives an image from the other client.
    :param sock - socket connection
    :addr - the other client address"""

    while not leaving:

        try:
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
            other_image_container.img = None
        except OSError:
            break


def listen_for_leaving(sock: socket.socket):
    global leaving
    sock.settimeout(5)
    print('listening for leaving')
    while not leaving:
        try:
            sock.recv(5)
        except socket.timeout:
            print('no alive data received in time. exiting')
            break
        except ConnectionError:
            print('client disconnected. exiting')
            break

    try:
        sock.close()
    except Exception:
        pass
    if not leaving:
        showinfo('Client has disconnected', 'Returning to user page.')
        leave()


def update_photos():
    """The function updates the photos on the screen to create a video illusion"""
    if not leaving:
        # update the photos on the image containers
        my_image_container.update()
        other_image_container.update()

        # displaying the changes to the screen

        canvas.create_image(500, 550, image=my_image_container.img)
        canvas.create_image(1400, 550, image=other_image_container.img)

        # calling this function again after 10 milliseconds to update the screen again

        canvas.after(10, update_photos)


def send_status(sock: socket.socket):
    while not leaving:
        try:
            sock.send(b'alive')
            time.sleep(3)
        except OSError:
            pass

    try:
        sock.close()
    except Exception:
        pass


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
        tcp.settimeout(1)
        conn = None
        while not leaving:
            try:
                conn, addr = tcp.accept()
            except socket.timeout:
                pass
            else:
                tcp.settimeout(None)
                break
        return conn


def leave():
    global leaving

    leaving = True
    run_user_page()


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
        if self._received is None:
            self._displayed = None
        else:
            # converts to BGR because PhotoImage works with BGR format only.
            self._displayed = ImageTk.PhotoImage(Image.fromarray(cv2.cvtColor(self._received, cv2.COLOR_RGB2BGR)))


# creating the containers
my_image_container = ImageContainer()
other_image_container = ImageContainer()
