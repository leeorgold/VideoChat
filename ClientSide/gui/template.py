import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()
root.title('cyberous')
root.attributes('-fullscreen', True)

# Screen
x = 1920
y = 1080
root.geometry(f"{x}x{y}")

default_bg = tk.PhotoImage(file='images/background.png')

logo = tk.PhotoImage(file='images/logo.png')

exit_button_img = tk.PhotoImage(file=r"images/exit_button.png")

canvas = tk.Canvas(root, height=y, width=x)
canvas.pack()
MAIN_FONT = 'Cascadia Mono'

def font_size(size=35):
    return 'Cascadia Mono', size, 'bold'


def foo():
    pass