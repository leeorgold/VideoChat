import tkinter.messagebox as msgbox
import re


class DataChecker:

    @classmethod
    def username(cls, username: str):
        if not username:
            msgbox.showwarning('Empty username', 'You must enter a username')
            return False
        if len(username) < 4:
            msgbox.showwarning('Username too short', 'Username must contain at least 4 characters')
            return False
        if len(username) > 20:
            msgbox.showwarning('Username too long', 'Username must be under 21 characters')
            return False
        if not (username.isalnum() and username.isascii()):
            msgbox.showwarning('Invalid username', 'Username must contain english letters and numbers only')
            return False
        elif username.isdigit():
            msgbox.showwarning('Invalid username', 'Username must contain at least one letter')
            return False
        return True

    @classmethod
    def password(cls, password: str, password2=None):
        if not password:
            msgbox.showwarning('Empty password', 'You must enter a password')
            return False
        if len(password) < 4:
            msgbox.showwarning('Password too short', 'Password must contain at least 4 characters')
            return False
        if len(password) > 30:
            msgbox.showwarning('Password too long', 'Username must be under 31 characters')
            return False
        if not (password.isalnum() and password.isascii()):
            msgbox.showwarning('Invalid password', 'password must contain english letters and numbers only')
            return False
        if password.isalpha():
            msgbox.showwarning('Invalid password', 'For security measures, password must contain at least one number')
            return False
        if password.isdigit():
            msgbox.showwarning('Invalid password', 'For security measures, password must contain at least one letter')
            return False
        if password2 is not None and not password == password2:
            msgbox.showwarning('Wrong confirmation password', 'Password and confirmation password do not match')
            return False
        return True

    @classmethod
    def phone(cls, phone: str):
        if not phone:
            msgbox.showwarning('Empty phone number', 'You must enter a phone number')
            return False
        if not re.search(r"^\d{10}$", phone):
            msgbox.showwarning('Invalid phone number', 'You must enter 10 digit exactly with no special characters')
            return False
        if not re.search(r"^05[0-58]\d{7}$", phone):
            msgbox.showwarning('Invalid phone number', 'You must enter a valid phone number')
            return False
        return True

    @classmethod
    def email(cls, email: str):
        if not email:
            msgbox.showwarning('Empty email address', 'You must enter an email address')
            return False
        if not email.isascii():
            msgbox.showwarning('Invalid email address', 'You must enter valid characters only')
            return False
        if not re.search(r"^[\w.]{2,}@([\w-]{2,}\.)+[\w-]{2,4}$", email):
            msgbox.showwarning('Invalid email address', 'You must enter a valid email address')
            return False
        return True


# print(DataChecker.email('gold.leeor2004@gmail.com'))
# print(DataChecker.email('leeorgo129@amirim.edum.org.il'))
