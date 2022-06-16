from template import *
from ClientSide.gui.data_checker import DataChecker as dc

from tkinter.messagebox import showinfo


def run_reset_password_page():
    from user_page import run_user_page
    from authentication_page import run_auth_page

    clear_window()

    def check_data():
        """The function checks the user input."""
        pass1 = pass1_entry.get()
        pass2 = pass2_entry.get()

        if dc.password(pass1, pass2):
            client_socket.send(msg_builder.reset_password(password=pass1).encode())
            msg = client_socket.recv()
            worked, details = msg_builder.handle_response('get_token', msg)
            if not worked:
                showinfo('Failure', details)
            else:
                run_auth_page('reset_password')

    continue_button = tk.Button(canvas, text="continue", font=(MAIN_FONT, 32, 'bold italic'), bg='#15478F',
                                activebackground='#2060BD', fg='white',
                                activeforeground='white', bd=3, command=check_data)

    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_user_page)

    pass1_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white', show='*',
                           insertbackground='white')
    pass2_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white', show='*',
                           insertbackground='white')

    canvas.create_text(250, 20, text="Cyberous - Reset Password", font=(MAIN_FONT, 60, 'bold italic'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(x // 2, 300, text="Choose your new password", font=(MAIN_FONT, 70, 'italic bold'), fill='white')

    canvas.create_text(x // 2 - 10, y // 2 - 50, text="New Password:", font=(MAIN_FONT, 45, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 - 50, window=pass1_entry, anchor=tk.W, height=50, width=300)

    canvas.create_text(x // 2 - 10, y // 2 + 50, text="Confirm Password:", font=(MAIN_FONT, 30, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 + 50, window=pass2_entry, anchor=tk.W, height=50, width=300)

    canvas.create_window(x // 2, y // 2 + 180, window=continue_button)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)


if __name__ == "__main__":
    run_reset_password_page()
