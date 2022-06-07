from template import *




def run_home_page():
    from login_page import run_login_page
    from register_page import run_register_page
    # from flipages.rules_page import run_rules_page
    from welcome_page import run_welcome_page
    # from flipages.credits_page import run_credits_page

    canvas.delete('all')

    exit_button = tk.Button(canvas, image=exit_button_img, command=root.destroy, bd=0)
    exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=tk.NE)

    login_button = tk.Button(canvas, text="Login", font=(MAIN_FONT, 45, 'bold italic'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_login_page)
    # login_button.pack()
    register_button = tk.Button(canvas, text="Register", font=(MAIN_FONT, 40, 'italic bold'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_register_page)
    # register_button.pack()
    about_button = tk.Button(canvas, text="About", font=(MAIN_FONT, 45, 'italic bold'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=foo)
    # about_button.pack()
    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=run_welcome_page)
    # back_button.pack()
    credits_button = tk.Button(canvas, text="Credits", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
                             activebackground='#2060BD', fg='white',
                             activeforeground='white', bd=3, command=foo)
    # credits_button.pack()

    canvas.create_text(20, 20, text="Cyberous - Home Page", font=(MAIN_FONT, 60, 'italic bold'), anchor=tk.NW, fill='white')
    canvas.create_window(x - 2, y - 700, anchor=tk.E, window=login_button)
    canvas.create_window(x - 2, y - 550, anchor=tk.E, window=register_button)
    canvas.create_window(x - 2, y - 400, anchor=tk.E, window=about_button)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    canvas.create_window(2, y - 180, anchor=tk.W, window=credits_button)


if __name__ == "__main__":
    run_home_page()
