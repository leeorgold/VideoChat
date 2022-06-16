import tkinter as tk
# from PIL import Image, ImageTk
# import socket
from ClientSide.message_builder import MessageBuilder
from ClientSide.encryption_manger import EncryptionManger


# build the application screen
root = tk.Tk()
root.title('cyberous')
root.attributes('-fullscreen', True)

# Screen
x = 1920
y = 1080
root.geometry(f"{x}x{y}")

# build a canvas. on the canvas the gui is drawn.
canvas = tk.Canvas(root, height=y, width=x)
canvas.pack()


# build objects that are in used in the pages
default_bg = tk.PhotoImage(file='../images/background.png')
logo = tk.PhotoImage(file='../images/new-small-logo.png')
exit_button_img = tk.PhotoImage(file=r"../images/exit_button.png")
my_username = ['']

# declae the main font name.
MAIN_FONT = 'Cascadia Mono'

# server_ip = '172.19.250.79'
server_ip = '192.168.0.109'
port = 10000

# create a EncryptionManger object.
client_socket = EncryptionManger(ip=server_ip, port=port)
msg_builder = MessageBuilder()


# define function for different activities on the application

def clear_window():
    """The function deletes all the items from the canvas.
     Once the canvas is cleared, the basic drawing is done.
     Basic drawing contains background image, X button and a logo."""
    canvas.delete('all')

    exit_button = tk.Button(canvas, image=exit_button_img, command=close_window, bd=0)
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    canvas.create_image(50, 20, image=logo, anchor=tk.NW)


def close_window():
    """The function try to inform the server about leaving before destroying the application."""
    try:
        client_socket.send(msg_builder.logout().encode())
    except ConnectionError:
        pass
    root.destroy()


# set the closing window function to the custom close window declared above.
root.protocol('WM_DELETE_WINDOW', close_window)

