import tkinter as tk
# from PIL import Image, ImageTk
import socket
from ClientSide.message_builder import MessageBuilder
from ClientSide.encryption_manger import EncryptionManger

root = tk.Tk()
root.title('cyberous')
root.attributes('-fullscreen', True)

# Screen
x = 1920
y = 1080
root.geometry(f"{x}x{y}")

default_bg = tk.PhotoImage(file='../images/background.png')

logo = tk.PhotoImage(file='../images/new-small-logo.png')

exit_button_img = tk.PhotoImage(file=r"../images/exit_button.png")

canvas = tk.Canvas(root, height=y, width=x)
canvas.pack()
MAIN_FONT = 'Cascadia Mono'

# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_ip = '172.19.250.79'
# server_ip = '192.168.0.109'
port = 10000

#
# client_socket.connect((host_ip, port))  # a tuple
client_socket = EncryptionManger(ip=server_ip, port=port)


# reset_encryption_manager()

msg_builder = MessageBuilder()
my_username = ['']


def clear_window():
    canvas.delete('all')

    exit_button = tk.Button(canvas, image=exit_button_img, command=close_window, bd=0)
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    canvas.create_image(50, 20, image=logo, anchor=tk.NW)


def close_window():
    try:
        client_socket.send(msg_builder.logout().encode())
    except ConnectionError:
        pass
    root.destroy()


root.protocol('WM_DELETE_WINDOW', close_window)


def foo():
    pass
