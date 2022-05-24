from tkinter import *
from PIL import Image, ImageTk

root = Tk()
root.title('cyberous')
root.attributes('-fullscreen', True)

# Screen
x = 1920
y = 1080
root.geometry(f"{x}x{y}")

default_bg = PhotoImage(file='images/background.png')

logo = PhotoImage(file='images/logo.png')

exit_button_img = PhotoImage(file=r"images/exit_button.png")

canvas = Canvas(root, height=y, width=x)
canvas.pack()

images = []


def create_rectangle(x1, y1, x2, y2, **kwargs):
    if 'alpha' in kwargs:
        alpha = int(kwargs.pop('alpha') * 255)
        fill = kwargs.pop('fill')
        fill = root.winfo_rgb(fill) + (alpha,)
        image = Image.new('RGBA', (x2 - x1, y2 - y1), fill)
        images.append(ImageTk.PhotoImage(image))
        canvas.create_image(x1, y1, image=images[-1], anchor='nw')
    rect = canvas.create_rectangle(x1, y1, x2, y2, **kwargs)