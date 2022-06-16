from template import *
from ClientSide.gui.data_checker import DataChecker as dc


from tkinter.messagebox import showinfo

def run_register_page():
    from home_page import run_home_page
    from login_page import run_login_page
    from authentication_page import run_auth_page

    clear_window()

    register_username_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'bold'), bd=3, bg='#15478F', fg='white',
                                       insertbackground='white')
    register_password_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'bold'), bd=3, bg='#15478F', fg='white', show='*',
                                       insertbackground='white')
    register_confirm_password_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'bold'), bd=3, bg='#15478F', fg='white',
                                               show='*', insertbackground='white')
    register_phone_number_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'bold'), bd=3, bg='#15478F', fg='white',
                                           insertbackground='white')
    register_email_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'bold'), bd=3, bg='#15478F', fg='white',
                                    insertbackground='white')

    def check_data():
        """The function checks the user input."""
        username = register_username_entry.get()
        password = register_password_entry.get()
        confirm_password = register_confirm_password_entry.get()
        phone_number = register_phone_number_entry.get()
        email = register_email_entry.get()

        if dc.username(username) and dc.password(password, confirm_password) and dc.phone(phone_number) and dc.email(
                email):
            client_socket.send(msg_builder.register(
                username=username, password=password, phone=phone_number, email=email).encode())
            msg = client_socket.recv()
            worked, details = msg_builder.handle_response('get_token', msg)
            if not worked:
                showinfo('Failure', details)
            else:
                my_username[0] = username
                run_auth_page('register')


    register_button = tk.Button(canvas, text="Register", font=(MAIN_FONT, 32, 'bold italic'), bg='#15478F',
                                activebackground='#2060BD', fg='white',
                                activeforeground='white', bd=3, command=check_data)
    login_button = tk.Button(canvas, text="Login", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_login_page)
    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 23, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_home_page)

    canvas.create_text(250, 20, text="Cyberous - Register Page", font=(MAIN_FONT, 60, 'bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(x // 2 + 50, 230, text="Register", font=(MAIN_FONT, 85, 'bold'), fill='white')

    canvas.create_text(x // 2 - 280, y // 2 - 170, text="Username:", font=(MAIN_FONT, 40, 'bold'), anchor=tk.W,
                       fill='white')
    canvas.create_window(x // 2 + 25, y // 2 - 170, window=register_username_entry, anchor=tk.W, height=50, width=300)
    canvas.create_text(x // 2 - 280, y // 2 - 70, text="Password:", font=(MAIN_FONT, 40, 'bold'), anchor=tk.W,
                       fill='white')
    canvas.create_window(x // 2 + 25, y // 2 - 70, window=register_password_entry, anchor=tk.W, height=50, width=300)
    canvas.create_text(x // 2 - 280, y // 2 + 30, text="Confirm Password:", font=(MAIN_FONT, 22, 'bold'),
                       anchor=tk.W,
                       fill='white')
    canvas.create_window(x // 2 + 25, y // 2 + 30, window=register_confirm_password_entry, anchor=tk.W, height=50,
                         width=300)
    canvas.create_text(x // 2 - 280, y // 2 + 130, text="Phone Number:", font=(MAIN_FONT, 27, 'bold'), anchor=tk.W,
                       fill='white')
    canvas.create_window(x // 2 + 15, y // 2 + 130, window=register_phone_number_entry, anchor=tk.W, height=50,
                         width=300)
    canvas.create_text(x // 2 - 280, y // 2 + 230, text="Email:", font=(MAIN_FONT, 40, 'bold'), anchor=tk.W,
                       fill='white')
    canvas.create_window(x // 2 - 80, y // 2 + 230, window=register_email_entry, anchor=tk.W, height=50, width=405)

    canvas.create_window(x // 2, y - 180, window=register_button)
    canvas.create_window(2, y - 180, anchor=tk.W, window=login_button)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)


if __name__ == "__main__":
    run_register_page()
