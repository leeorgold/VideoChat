import json



class MessageBuilder:
    """The class handles the messages formatting according to the protocol."""
    def __init__(self):
        self._REQUEST = 'request'
        self._PARAMETERS = 'parameters'
        self._SESSION = 'session'
        self.__session = None

    def _format(self):
        return {
            self._REQUEST: None,
            self._PARAMETERS: {self._SESSION: self.__session}
        }

    def set_session(self, session):
        self.__session = session


    # These functions will build the messages.


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
        return msg

    def login(self, *, username, password):
        msg = self._format()
        msg[self._REQUEST] = 'login'
        msg[self._PARAMETERS] = {
            'username': username,
            'password': password
        }
        msg = json.dumps(msg)
        return msg

    def logout(self):
        msg = self._format()
        msg[self._REQUEST] = 'logout'
        msg = json.dumps(msg)

        return msg

    def authenticate(self, code):
        msg = self._format()
        msg[self._REQUEST] = 'authenticate'
        msg[self._PARAMETERS] = {'token': self.token}
        del self.token
        msg[self._PARAMETERS]['code'] = code
        msg = json.dumps(msg)
        return msg

    def start_meeting(self, password):
        msg = self._format()
        msg[self._REQUEST] = 'start_meeting'
        msg[self._PARAMETERS]['password'] = password
        msg = json.dumps(msg)
        return msg

    def join_meeting(self, meeting_id, password):
        msg = self._format()
        msg[self._REQUEST] = 'join_meeting'
        msg[self._PARAMETERS]['meeting_id'] = meeting_id
        msg[self._PARAMETERS]['password'] = password
        msg = json.dumps(msg)
        return msg

    def forgot_password(self, username, email):
        msg = self._format()
        msg[self._REQUEST] = 'forgot_password'
        msg[self._PARAMETERS] = {
            'username': username,
            'email': email
        }
        msg = json.dumps(msg)
        return msg

    def reset_password(self, password):
        msg = self._format()
        msg[self._REQUEST] = 'reset_password'
        msg[self._PARAMETERS]['password'] = password
        msg = json.dumps(msg)
        return msg

    def leave_meeting(self):
        msg = self._format()
        msg[self._REQUEST] = 'leave_meeting'
        msg = json.dumps(msg)
        return msg


    def handle_response(self, req, msg):
        """The function will analyse and handle the server responses."""
        try:
            msg = json.loads(msg)
        except json.decoder.JSONDecodeError:
            return False, 'Not a json data'

        if (status := msg.get('status')) is None:
            return False, 'No status'

        if type(status) is not bool:
            return False, 'Not a boolean status'

        if (parm := msg.get('parameters')) is None:
            return False, 'No parameters'

        if req == 'login':
            if status:
                if session := parm.get('session'):
                    self.__session = session
                    return True, ''
                else:
                    return False, 'no session'
            elif (details := parm.get('details')) is not None:
                return False, details

        elif req == 'get_token':
            if status:
                if token := parm.get('token'):
                    self.token = token
                    return True, ''
                return False, 'no token'

            elif (details := parm.get('details')) is not None:
                return False, details

        elif req == 'authenticate':
            if status:
                if session := parm.get('session'):
                    self.__session = session
                return True, ''
            elif (details := parm.get('details')) is not None:
                return False, details

        elif req == 'start_meeting':
            if status:
                if meeting_id := parm.get('meeting_id'):
                    return True, meeting_id
            elif (details := parm.get('details')) is not None:
                return False, details

        elif req == 'join_meeting':
            if status:
                if ip := parm.get('ip'):
                    return True, ip
            elif (details := parm.get('details')) is not None:
                return False, details

        return False, 'Unknown Error'
