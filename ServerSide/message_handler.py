import json
import re
from DataBase.database import Users

_REQUEST = 'request'
_PARAMETERS = 'parameters'
_SESSION = 'session'


def handle_message(msg):
    try:
        msg = json.loads(msg)
    except json.decoder.JSONDecodeError:
        return False, 'Not a json data'

    if not (req := msg.get(_REQUEST)):
        return False, 'No request'

    if req not in _valid_requests:
        return False, 'Not a valid request'

    if (kwargs := msg.get(_PARAMETERS)) is None:
        return False, 'No parameters'

    try:
        return _valid_requests[req](**kwargs)
    except Exception as e:
        print(e)
        return False, 'Some error occurred'


def register(*, username, password, phone, email):
    if username_ok(username) and password_ok(password) and phone_ok(phone) and email_ok(email):
        return Users.insert_user(username, password, phone, email)
    return False, 'Illegal data'


def login(*, username, password):
    if username_ok(username) and password_ok(password):
        return Users.try_login(username, password)
    return False, 'Illegal data'


_valid_requests = {'register': register, 'login': login}


def username_ok(username: str):
    return 3 < len(username) < 21 and username.isalnum() and username.isascii() and not username.isdigit()


def password_ok(password: str):
    return 3 < len(
        password) < 31 and password.isalnum() and password.isascii() and not password.isdigit() and not password.isalpha()


def phone_ok(phone: str):
    return re.search(r"^05[0-58]\d{7}$", phone) is not None


def email_ok(email: str):
    return re.search(r"^[\w.]{2,}@([\w-]{2,}\.)+[\w-]{2,4}$", email) is not None

# print(handle_message(
#     '{"request": "register", '
#     '"parameters": {"username": "user1", "password": "pass1", "phone": "0551234567", "email": "email12@gmail.com"}}'
# ))
# print(handle_message(
#     '{"request": "login", '
#     '"parameters": {"username": "user1", "password": "pass1"}}'
# ))
