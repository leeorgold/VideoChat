from template import *


def run_home_page():
    from login_page import run_login_page
    from register_page import run_register_page
    from welcome_page import run_welcome_page
    from about_page import run_about_page

    clear_window()

    login_button = tk.Button(canvas, text="Login", font=(MAIN_FONT, 45, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_login_page)
    register_button = tk.Button(canvas, text="Register", font=(MAIN_FONT, 40, 'italic bold'), bg='#15478F',
                                activebackground='#2060BD', fg='white',
                                activeforeground='white', bd=3, command=run_register_page)
    about_button = tk.Button(canvas, text="About", font=(MAIN_FONT, 45, 'italic bold'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_about_page)
    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_welcome_page)

    canvas.create_text(250, 20, text="Cyberous - Home Page", font=(MAIN_FONT, 60, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_window(x - 2, y - 600, anchor=tk.E, window=login_button)
    canvas.create_window(x - 2, y - 400, anchor=tk.E, window=register_button)
    canvas.create_window(2, y - 180, anchor=tk.W, window=about_button)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)


if __name__ == "__main__":
    run_home_page()
