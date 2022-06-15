from template import *
from ClientSide.gui.data_checker import DataChecker as dc

from tkinter.messagebox import showinfo


def run_meeting_password_page():
    from meeting_page import run_meeting_page
    from user_page import run_user_page
    from register_page import run_register_page

    clear_window()

    def check_data():
        password = pass_entry.get()

        if dc.password(password):
            client_socket.send(msg_builder.start_meeting(password).encode())
            msg = client_socket.recv()
            worked, details = msg_builder.handle_message('start_meeting', msg)
            if not worked:
                showinfo('Failure', details)
            else:
                run_meeting_page(mode='host', meeting_id=details)

    pass_button = tk.Button(canvas, text="choose password", font=(MAIN_FONT, 32, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=check_data)

    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_user_page)

    pass_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white',
                          insertbackground='white', show='*')

    canvas.create_text(250, 20, text="Cyberous - Start Meeting Page", font=(MAIN_FONT, 60, 'bold italic'), anchor=tk.NW,
                       fill='white')
    # canvas.create_text(x // 2, 300, text="Login", font=(MAIN_FONT, 100, 'italic bold'), fill='white')

    canvas.create_text(x // 2 - 10, y // 2 - 50, text="Meeting password:", font=(MAIN_FONT, 45, 'bold italic'),
                       anchor=tk.E, fill='white')
    canvas.create_window(x // 2 + 10, y // 2 - 50, window=pass_entry, anchor=tk.W, height=50, width=300)

    canvas.create_window(x // 2, y // 2 + 180, window=pass_button)
    # canvas.create_window(x // 2, y - 180, window=forgot_password_button, height=100, width=230)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    # canvas.create_window(2, y - 180, window=register_button, anchor=tk.W)


if __name__ == "__main__":
    run_meeting_password_page()
