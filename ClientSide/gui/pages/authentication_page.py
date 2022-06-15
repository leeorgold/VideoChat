from template import *
from ClientSide.gui.data_checker import DataChecker as dc

from tkinter.messagebox import showinfo


def run_auth_page(mode):
    from home_page import run_home_page
    from user_page import run_user_page
    from register_page import run_register_page
    from forgot_password_page import run_forgot_password_page

    clear_window()

    def check_data():
        code = auth_entry.get()

        if dc.auth_code(code):
            client_socket.send(msg_builder.authenticate(code).encode())
            msg = client_socket.recv()
            worked, details = msg_builder.handle_message('authenticate', msg)
            if not worked:
                showinfo('Failure', details)
                my_username[0] = ''
                if mode == 'register':
                    run_register_page()
                elif mode == 'forgot_password':
                    run_forgot_password_page()
                elif mode == 'reset_password':
                    run_forgot_password_page()
            elif mode == 'reset_password':
                showinfo('Success', 'Password changed successfully.')
            run_user_page()

    auth_button = tk.Button(canvas, text="authenticate", font=(MAIN_FONT, 32, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=check_data)

    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_home_page)

    auth_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white',
                          insertbackground='white')

    canvas.create_text(250, 20, text="Cyberous - Authentication Page", font=(MAIN_FONT, 60, 'bold italic'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(x // 2, 300, text="Login", font=(MAIN_FONT, 100, 'italic bold'), fill='white')

    canvas.create_text(x // 2 - 10, y // 2 - 50, text="authentication code:", font=(MAIN_FONT, 45, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 - 50, window=auth_entry, anchor=tk.W, height=50, width=300)

    canvas.create_window(x // 2, y // 2 + 180, window=auth_button)
    # canvas.create_window(x // 2, y - 180, window=forgot_password_button, height=100, width=230)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    # canvas.create_window(2, y - 180, window=register_button, anchor=tk.W)


if __name__ == "__main__":
    run_auth_page()
