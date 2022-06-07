from template import *


def run_user_page():
    from login_page import run_login_page
    from register_page import run_register_page
    # from flipages.rules_page import run_rules_page
    from welcome_page import run_welcome_page
    # from flipages.credits_page import run_credits_page
    from meeting import run_meeting

    canvas.delete('all')

    exit_button = tk.Button(canvas, image=exit_button_img, command=root.destroy, bd=0)
    exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=tk.NE)

    change_password_button = tk.Button(canvas, text="Change password", font=(MAIN_FONT, 45, 'bold italic'),
                                       bg='#15478F',
                                       activebackground='#2060BD', fg='white',
                                       activeforeground='white', bd=3, command=foo)
    # login_button.pack()
    host_meeting_button = tk.Button(canvas, text="Start meeting", font=(MAIN_FONT, 40, 'italic bold'), bg='#15478F',
                                    activebackground='#2060BD', fg='white',
                                    activeforeground='white', bd=3, command=foo)
    # register_button.pack()
    join_meeting_button = tk.Button(canvas, text="Join meeting", font=(MAIN_FONT, 45, 'italic bold'), bg='#15478F',
                                    activebackground='#2060BD', fg='white',
                                    activeforeground='white', bd=3, command=run_meeting)
    # about_button.pack()
    # back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
    #                         activebackground='#2060BD', fg='white',
    #                         activeforeground='white', bd=3, command=run_welcome_page)
    # back_button.pack()
    logout_button = tk.Button(canvas, text="Logout", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
                              activebackground='#2060BD', fg='white',
                              activeforeground='white', bd=3, command=foo)
    # credits_button.pack()

    canvas.create_text(20, 20, text="Cyberous - User Page", font=(MAIN_FONT, 60, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(30, 150, text="Hello leeor123", font=(MAIN_FONT, 45, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_window(x - 2, y - 550, anchor=tk.E, window=host_meeting_button)
    canvas.create_window(x - 2, y - 400, anchor=tk.E, window=join_meeting_button)
    canvas.create_window(x - 2, y - 250, anchor=tk.E, window=change_password_button)
    # canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    canvas.create_window(2, y - 180, anchor=tk.W, window=logout_button)


if __name__ == "__main__":
    run_user_page()
