

class Client:
    def __init__(self, username, email, ip):
        self.username = username
        self.email = email
        self.ip = ip
        self.hosting = None

    def __eq__(self, other):
        return self.username == other.username


# class UsersDict(dict):
#     def __init__(self, *args, **kwargs):
#         super().__init__()
#         self.update(*args, **kwargs)
#
#     def __setitem__(self, key, value):
#         for client in self.values():
#             if client == value:
#
#         super().__setitem__(key, value)
#
#     def update(self, *args, **kwargs):
#         if args:
#             if len(args) > 1:
#                 raise TypeError("update expected at most 1 arguments, "
#                                 "got %d" % len(args))
#             other = dict(args[0])
#             for key in other:
#                 self[key] = other[key]
#         for key in kwargs:
#             self[key] = kwargs[key]
#
#     def setdefault(self, key, value=None):
#         if key not in self:
#             self[key] = value
#         return self[key]


logged_users : dict[str, Client] = {}