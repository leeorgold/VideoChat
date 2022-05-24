from ClientSide.gui.template import *


def run_welcome_page():
    from ClientSide.gui.meeting import run_meeting

    exit_button = Button(canvas, image=exit_button_img, command=root.destroy, bd=0)
    exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=NE)

    continue_button = Button(canvas, text="Continue", font=('Cascadia Mono', 35, 'bold'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_meeting)
    continue_button.pack()
    canvas.create_text(x // 2, 300, text="Welcome to\nCyberous...", font=('Cascadia Mono', 90, 'bold'), fill='white')
    canvas.create_window(x // 2, y // 2 + 200, window=continue_button)


if __name__ == "__main__":
    run_welcome_page()

mainloop()
