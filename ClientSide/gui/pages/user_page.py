from template import *
from welcome_page import run_welcome_page


def logout():
    client_socket.send(msg_builder.logout().encode())
    msg_builder.set_session(None)
    my_username[0] = ''
    run_welcome_page()


def run_user_page():
    from start_meeting_page import run_meeting_password_page
    from join_meeting_page import run_join_meeting_page
    from reset_password import run_reset_password_page

    clear_window()

    change_password_button = tk.Button(canvas, text="Change password", font=(MAIN_FONT, 45, 'bold italic'),
                                       bg='#15478F',
                                       activebackground='#2060BD', fg='white',
                                       activeforeground='white', bd=3, command=run_reset_password_page)
    host_meeting_button = tk.Button(canvas, text="Start meeting", font=(MAIN_FONT, 40, 'italic bold'), bg='#15478F',
                                    activebackground='#2060BD', fg='white',
                                    activeforeground='white', bd=3, command=run_meeting_password_page)
    join_meeting_button = tk.Button(canvas, text="Join meeting", font=(MAIN_FONT, 45, 'italic bold'), bg='#15478F',
                                    activebackground='#2060BD', fg='white',
                                    activeforeground='white', bd=3, command=run_join_meeting_page)
    logout_button = tk.Button(canvas, text="Logout", font=(MAIN_FONT, 35, 'italic bold'), bg='#15478F',
                              activebackground='#2060BD', fg='white',
                              activeforeground='white', bd=3, command=logout)

    canvas.create_text(250, 20, text="Cyberous - User Page", font=(MAIN_FONT, 60, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(30, 150, text=f"Hello {my_username[0]}", font=(MAIN_FONT, 45, 'italic bold'), anchor=tk.NW,
                       fill='white')
    canvas.create_window(x - 2, y - 550, anchor=tk.E, window=host_meeting_button)
    canvas.create_window(x - 2, y - 400, anchor=tk.E, window=join_meeting_button)
    canvas.create_window(x - 2, y - 250, anchor=tk.E, window=change_password_button)
    canvas.create_window(2, y - 180, anchor=tk.W, window=logout_button)


if __name__ == "__main__":
    run_user_page()
