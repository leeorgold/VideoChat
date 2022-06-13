from template import *
from welcome_page import run_welcome_page


def logout():
    client_socket.send(msg_builder.logout().encode())
    msg_builder.set_session(None)
    my_username[0] = ''
    # reset_encryption_manager()
    run_welcome_page()


def run_user_page():
    from start_meeting_page import run_meeting_password_page
    from join_meeting_page import run_join_meeting_page

    canvas.delete('all')

    exit_button = tk.Button(canvas, image=exit_button_img, command=close_window, bd=0)
    exit_button.pack()
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)
    # canvas.create_image(x - 50, 20, image=logo, anchor=tk.NE)

    change_password_button = tk.Button(canvas, text="Change password", font=(MAIN_FONT, 45, 'bold italic'),
                                       bg='#15478F',
                                       activebackground='#2060BD', fg='white',
                                       activeforeground='white', bd=3, command=foo)
    host_meeting_button = tk.Button(canvas, text="Start meeting", font=(MAIN_FONT, 40, 'italic bold'), bg='#15478F',
                                    activebackground='#2060BD', fg='white',
                                    activeforeground='white', bd=3, command=run_meeting_password_page)
    join_meeting_button = tk.Button(canvas, text="Join meeting", font=(MAIN_FONT, 45, 'italic bold'), bg='#15478F',
                                    activebackground='#2060BD', fg='white',
                                    activeforeground='white', bd=3, command=run_join_meeting_page)
    logout_button = tk.Button(canvas, text="Logout", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
                              activebackground='#2060BD', fg='white',
                              activeforeground='white', bd=3, command=logout)

    canvas.create_text(20, 20, text="Cyberous - User Page", font=(MAIN_FONT, 60, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(30, 150, text=f"Hello {my_username[0]}", font=(MAIN_FONT, 45, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_window(x - 2, y - 550, anchor=tk.E, window=host_meeting_button)
    canvas.create_window(x - 2, y - 400, anchor=tk.E, window=join_meeting_button)
    canvas.create_window(x - 2, y - 250, anchor=tk.E, window=change_password_button)
    canvas.create_window(2, y - 180, anchor=tk.W, window=logout_button)


if __name__ == "__main__":
    run_user_page()
