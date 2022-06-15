from template import *
from ClientSide.gui.data_checker import DataChecker as dc

from tkinter.messagebox import showinfo


def run_forgot_password_page():
    from home_page import run_home_page
    from authentication_page import run_auth_page
    from register_page import run_register_page
    from login_page import run_login_page

    clear_window()

    def check_data():
        username = username_entry.get()
        email = email_entry.get()

        if dc.username(username) and dc.email(email):
            client_socket.send(msg_builder.forgot_password(username=username, email=email).encode())
            msg = client_socket.recv()
            worked, details = msg_builder.handle_message('get_token', msg)
            if not worked:
                showinfo('Failure', details)
            else:
                my_username[0] = username
                run_auth_page('forgot_password')

    login_button = tk.Button(canvas, text="login", font=(MAIN_FONT, 32, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=check_data)

    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_home_page)

    register_button = tk.Button(canvas, text="Register", font=(MAIN_FONT, 35, 'bold italic'),
                                bg='#15478F',
                                activebackground='#2060BD', fg='white',
                                activeforeground='white', bd=3, command=run_register_page)

    got_a_password_button = tk.Button(canvas, text="Got a\npassword?", font=(MAIN_FONT, 25, 'bold italic'),
                                       bg='#15478F',
                                       activebackground='#2060BD', fg='white',
                                       activeforeground='white', bd=3, command=run_login_page)

    username_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white',
                              insertbackground='white')
    email_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white',
                           insertbackground='white')

    canvas.create_text(250, 20, text="Cyberous - Login Page", font=(MAIN_FONT, 60, 'bold italic'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(x // 2, 300, text="Login", font=(MAIN_FONT, 100, 'italic bold'), fill='white')

    canvas.create_text(x // 2 - 10, y // 2 - 50, text="Username:", font=(MAIN_FONT, 45, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 - 50, window=username_entry, anchor=tk.W, height=50, width=300)

    canvas.create_text(x // 2 - 10, y // 2 + 50, text="Email:", font=(MAIN_FONT, 45, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 + 50, window=email_entry, anchor=tk.W, height=50, width=300)

    canvas.create_window(x // 2, y // 2 + 180, window=login_button)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    canvas.create_window(2, y - 180, window=register_button, anchor=tk.W)
    canvas.create_window(x // 2, y - 180, window=got_a_password_button, height=100, width=230)


if __name__ == "__main__":
    from welcome_page import run_welcome_page
    run_welcome_page()
