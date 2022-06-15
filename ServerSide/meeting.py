from client import Client
# from os import urandom
import random





def id_generator():
    abc = 'abcdefghijklmnopqrstuvwxyz'
    st = ''.join([random.choice(abc) for c in range(8)])
    while st in meetings.keys():
        st = ''.join([random.choice(abc) for c in range(8)])
    return st


class Meeting:
    def __init__(self, host: Client, password: str):
        self.host = host
        self.ip = host.ip
        self.joiner = None
        # self.id = id_generator()
        self.id = 'aaaaaaaa'
        self.password = password
        meetings[self.id] = self

    def can_add_user(self):
        return self.joiner is None

    def add_user(self, user: Client):
        assert self.can_add_user(), "Meeting is full"
        self.joiner = user


meetings: dict[str, Meeting] = {}
