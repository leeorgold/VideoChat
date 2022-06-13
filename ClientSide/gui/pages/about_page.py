from template import *

text = """
Welcome to cyberous, a secured video chat application.
Cyberous provides a solution to the problem of communicating
with a friend, a family member, a job partner, and everyone
else who has a computer.

HOW TO USE CYBEROUS?

In order to use the application for the first time, you will
have to create an account.
Once you have registered, all you need to do in your next visits
is to simply log in.
Once youre logged in, you can start your own personal meeting and
invite another user. In addition you can also join your friends
meetings.

COPYRIGHTS:
All rights reserved to Leeor Goldberg.
"""

def run_about_page():
    from home_page import run_home_page

    canvas.delete('all')
    exit_button = tk.Button(canvas, image=exit_button_img, command=close_window, bd=0)
    canvas.create_window(x - 24, 15, window=exit_button)
    canvas.create_image(0, 0, image=default_bg, anchor=tk.NW)

    # canvas.create_image(x - 50, 20, image=logo, anchor=tk.NE)

    back_button = tk.Button(canvas, text="Back", font=(MAIN_FONT, 35, 'bold italic'), bg='#15478F',
                            activebackground='#2060BD', fg='white',
                            activeforeground='white', bd=3, command=run_home_page)

    canvas.create_text(20, 20, text="Cyberous - About", font=(MAIN_FONT, 60, 'bold italic'), anchor=tk.NW,
                       fill='white')
    canvas.create_text(x // 2 - 120, 600, text=text, font=(MAIN_FONT, 28, 'italic bold'), fill='white')



    # canvas.create_window(x // 2, y - 180, window=forgot_password_button, height=100, width=230)
    canvas.create_window(x - 2, y - 180, anchor=tk.E, window=back_button)
    # canvas.create_window(2, y - 180, window=register_button, anchor=tk.W)


if __name__ == "__main__":
    run_about_page()
