import json


class MessageBuilder:

    def __init__(self):
        self._REQUEST = 'request'
        self._PARAMETERS = 'parameters'
        # self._SESSION = 'session'
        # self.__session = None

    def _format(self):
        return {
            self._REQUEST: None,
            # self._SESSION: self.__session,
            self._PARAMETERS: None
        }

    def set_session(self, session):
        self.__session = session

    def register(self, *, username, password, phone, email):
        msg = self._format()
        msg[self._REQUEST] = 'register'
        msg[self._PARAMETERS] = {
            'username': username,
            'password': password,
            'phone': phone,
            'email': email
        }
        msg = json.dumps(msg)
        return f'{len(msg)}'.zfill(8) + msg

    def login(self, *, username, password):
        msg = self._format()
        msg[self._REQUEST] = 'login'
        msg[self._PARAMETERS] = {
            'username': username,
            'password': password
        }
        msg = json.dumps(msg)
        return f'{len(msg)}'.zfill(8) + msg

# print(MessageBuilder().register(username='user1', password='pass1', phone='0501234567', email='email@gmail.com'))

