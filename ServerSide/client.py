class Client:
    def __init__(self, username, email, ip):
        self.username = username
        self.email = email
        self.ip = ip
        self.hosting = None


logged_users: dict[str, Client] = {}
