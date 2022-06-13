import json
import re
from DataBase.database import Users, random_string
from client import Client, logged_users
from smtp import send_code
from meeting import Meeting, meetings

_REQUEST = 'request'
_PARAMETERS = 'parameters'
_SESSION = 'session'
_DETAILS = 'details'

auth_codes = {}
functions = {}


def handle_message(sock, msg):
    try:
        msg = json.loads(msg)
    except json.decoder.JSONDecodeError:
        return build_message(False, {_DETAILS: 'Not a json data'})

    if not (req := msg.get(_REQUEST)):
        return build_message(False, {_DETAILS: 'No request'})

    if req not in _valid_requests:
        return build_message(False, {_DETAILS: 'Not a valid request'})

    if (kwargs := msg.get(_PARAMETERS)) is None:
        return build_message(False, {_DETAILS: 'No parameters'})

    try:
        return _valid_requests[req](sock, **kwargs)
    except Exception as e:
        print(e)
        return build_message(False, {_DETAILS: 'Some error occurred'})


def register(sock, *, username, password, phone, email):
    if not (username_ok(username) and password_ok(password) and phone_ok(phone) and email_ok(email)):
        return build_message(False, {_DETAILS: 'Illegal data'})
    can = Users.can_insert_user(username, password, phone, email)
    if not can[0]:
        return build_message(can[0], {_DETAILS: can[1]})

    token = random_string(16, 16)
    while token in auth_codes.keys():
        token = random_string(16, 16)
    # auth_codes[token] = '123456'
    auth_codes[token] = send_code(email)
    functions[token] = {'func': inserting_user, 'args': (username, password, phone, email)}
    return build_message(True, {'token': token})


def search_logged_user(*, username=None, ip=None):
    if username:
        for session, client in logged_users.items():
            if username == client.username:
                return session
    if ip:
        for session, client in logged_users.items():
            if ip == client.ip:
                return session

    return None


def log_user(session, username, email, sock):
    if search_logged_user(username=username):
        return build_message(False, {_DETAILS: 'User already logged in.'})
    logged_users[session] = Client(username, email, sock.getpeername()[0])
    return build_message(True, {_SESSION: session})


def inserting_user(sock, username, password, phone, email):
    worked, session = Users.insert_user(username, password, phone, email)
    if not worked:
        return build_message(worked, {_DETAILS: session})

    return log_user(session, username, email, sock)


def login(sock, *, username, password):
    if not (username_ok(username) and password_ok(password)):
        return build_message(False, {_DETAILS: 'Illegal data'})
    worked, session = Users.try_login(username, password)
    if not worked:
        return build_message(worked, {_DETAILS: session})
    return log_user(session, username, Users.get_email(username), sock)


def logout(sock, session):
    if user := logged_users.get(session):
        if meet := user.hosting:
            meet.host = None
            del meetings[meet.id]
        del logged_users[session]
    return False


def authenticate(sock, token, code):
    if token not in auth_codes.keys():
        return build_message(False, {_DETAILS: 'Token does not exist'})
    if code != auth_codes.pop(token):
        functions.pop(token)
        return build_message(False, {_DETAILS: 'Wrong code'})
    dic = functions.pop(token)
    return dic['func'](sock, *dic['args'])


def start_meeting(sock, session, password):
    if user := logged_users.get(session):
        meet = Meeting(user, password)
        user.hosting = meet
        return build_message(True, {'meeting_id': meet.id})
    return build_message(False, {_DETAILS: 'Session does not exist'})


def join_meeting(sock, session, meeting_id, password):
    if session not in logged_users.keys():
        return build_message(False, {_DETAILS: 'Session does not exist'})
    if (meet := meetings.get(meeting_id)) is None:
        return build_message(False, {_DETAILS: 'Meeting does not exist'})
    if meet.password != password:
        return build_message(False, {_DETAILS: 'Wrong password'})
    msg = build_message(True, {'ip': meet.ip})
    meetings[meeting_id].host.hosting = None
    del meetings[meeting_id]
    return msg


_valid_requests = {
    'register': register,
    'login': login,
    'logout': logout,
    'authenticate': authenticate,
    'start_meeting': start_meeting,
    'join_meeting': join_meeting
}


def username_ok(username: str):
    return 3 < len(username) < 21 and username.isalnum() and username.isascii() and not username.isdigit()


def password_ok(password: str):
    return 3 < len(
        password) < 31 and password.isalnum() and password.isascii() and not password.isdigit() and not password.isalpha()


def phone_ok(phone: str):
    return re.search(r"^05[0-58]\d{7}$", phone) is not None


def email_ok(email: str):
    return re.search(r"^[\w.]{2,}@([\w-]{2,}\.)+[\w-]{2,4}$", email) is not None


def build_message(status, parameters):
    msg = json.dumps(
        {
            'status': status,
            'parameters': parameters
        }
    )
    return msg

# print(handle_message(
#     '{"request": "register", '
#     '"parameters": {"username": "user1", "password": "pass1", "phone": "0551234567", "email": "email12@gmail.com"}}'
# ))
# print(handle_message(
#     '{"request": "login", '
#     '"parameters": {"username": "user1", "password": "pass1"}}'
# ))
