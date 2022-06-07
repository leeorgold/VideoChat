from template import *
from data_checker import DataChecker as dc


def run_login_page():
    from home_page import run_home_page
    # from flipages.lobby import run_lobby
    # from flipages.home_page import run_home_page
    from register_page import run_register_page

    canvas.delete('all')
    exit_button = tk.Button(canvas, image=exit_button_img, command=root.destroy, bd=0)
    # exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)

    # canvas.create_image(x - 50, 20, image=logo, anchor=tk.NE)

    def check_data():
        username = login_username_entry.get()
        password = login_password_entry.get()

        if dc.username(username) and dc.password(password):
            print('valid data')
            # TODO: send data to server

    login_button = tk.Button(canvas, text="Login", font=(MAIN_FONT, 32, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=check_data)
    # login_button.pack()
    forgot_password_button = tk.Button(canvas, text="forgot\npassword?", font=(MAIN_FONT, 25, 'bold italic'),
                                       bg='#15478F',
                                       activebackground='#2060BD', fg='white',
                                       activeforeground='white', bd=3)
    # forgot_password_button.pack()
    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_home_page)
    # back_button.pack()
    register_button = tk.Button(canvas, text="Register", font=(MAIN_FONT, 35, 'bold italic'),
                                bg='#15478F',
                                activebackground='#2060BD', fg='white',
                                activeforeground='white', bd=3, command=run_register_page)
    # register_button.pack()

    login_username_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white',
                                    insertbackground='white')
    login_password_entry = tk.Entry(root, font=(MAIN_FONT, 20, 'italic bold'), bd=3, bg='#15478F', fg='white', show='*',
                                    insertbackground='white')

    canvas.create_text(20, 20, text="Cyberous - Login Page", font=(MAIN_FONT, 60, 'bold italic'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(x // 2, 300, text="Login", font=(MAIN_FONT, 100, 'italic bold'), fill='white')

    canvas.create_text(x // 2 - 10, y // 2 - 50, text="Username:", font=(MAIN_FONT, 45, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 - 50, window=login_username_entry, anchor=tk.W, height=50, width=300)

    canvas.create_text(x // 2 - 10, y // 2 + 50, text="Password:", font=(MAIN_FONT, 45, 'bold italic'), anchor=tk.E,
                       fill='white')
    canvas.create_window(x // 2 + 10, y // 2 + 50, window=login_password_entry, anchor=tk.W, height=50, width=300)

    canvas.create_window(x // 2, y // 2 + 180, window=login_button)
    canvas.create_window(x // 2, y - 180, window=forgot_password_button, height=100, width=230)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    canvas.create_window(2, y - 180, window=register_button, anchor=tk.W)


if __name__ == "__main__":
    run_login_page()
