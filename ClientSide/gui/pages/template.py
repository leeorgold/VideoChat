import tkinter as tk
# from PIL import Image, ImageTk
import socket
from ClientSide.message_builder import MessageBuilder

root = tk.Tk()
root.title('cyberous')
root.attributes('-fullscreen', True)

# Screen
x = 1920
y = 1080
root.geometry(f"{x}x{y}")

default_bg = tk.PhotoImage(file='../images/background.png')

logo = tk.PhotoImage(file='../images/logo.png')

exit_button_img = tk.PhotoImage(file=r"../images/exit_button.png")

canvas = tk.Canvas(root, height=y, width=x)
canvas.pack()
MAIN_FONT = 'Cascadia Mono'

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host_ip = '192.168.0.109'
# host_ip = '172.19.250.78'
port = 10000

client_socket.connect((host_ip, port))  # a tuple

msg_builder = MessageBuilder()
my_username = ['']


def close_window():
    try:
        client_socket.send(msg_builder.logout().encode())
    except ConnectionError:
        pass
    root.destroy()


root.protocol('WM_DELETE_WINDOW', close_window)


def foo():
    pass
