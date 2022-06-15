from template import *


def run_welcome_page():
    # from ClientSide.gui.meeting import run_meeting
    from home_page import run_home_page

    clear_window()

    continue_button = tk.Button(canvas, text="Continue", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                                activebackground='#2060BD', fg='white',
                                activeforeground='white', bd=3, command=run_home_page)
    # continue_button.pack()
    canvas.create_text(x // 2, 300, text="Welcome to\nCyberous...", font=(MAIN_FONT, 90, 'italic bold'), fill='white')
    canvas.create_window(x // 2, y // 2 + 200, window=continue_button)


if __name__ == "__main__":
    run_welcome_page()

    tk.mainloop()
