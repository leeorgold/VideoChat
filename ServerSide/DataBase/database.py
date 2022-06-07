import sqlite3
import random
from hashlib import sha256

# this makes sure that 'videochat.db' is created in this directory.
FILE_PATH = __file__ + '\\..\\videochat.db'


class Users:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    __tableName = "users"
    __password = "password"
    __username = "username"
    __phone_number = "phoneNumber"
    __email = "email"
    __salt = "salt"
    __session = 'session'
    __PEPPER = "J9L^O5ZCsxQr7T4H"

    conn = sqlite3.connect(FILE_PATH)
    # print("Opened database successfully:)")
    query_str = f"CREATE TABLE IF NOT EXISTS {__tableName} ({__username} TEXT NOT NULL PRIMARY KEY UNIQUE, " \
                f"{__password} TEXT NOT NULL, " \
                f"{__salt} TEXT NOT NULL, " \
                f"{__phone_number} TEXT NOT NULL UNIQUE, " \
                f"{__email} TEXT NOT NULL UNIQUE," \
                f"{__session} TEXT UNIQUE);"

    conn.execute(query_str)
    # print("Table created successfully")
    conn.commit()
    conn.close()

    @classmethod
    def get_table_name(cls):
        return cls.__tableName

    @classmethod
    def insert_user(cls, username, password, phone_number, email):
        """Gets a new user's data and adds it to the database."""

        conn = sqlite3.connect(FILE_PATH)

        session = cls.get_new_session()
        insert_query = f"INSERT INTO {cls.__tableName} ({cls.__username}, {cls.__password},{cls.__salt}," \
                       f" {cls.__phone_number}, {cls.__email}, {cls.__session}) VALUES (?, ?, ?, ?, ?, ?);"
        password, salt = cls.encrypt_password(password)
        values = (username, password, salt, phone_number, email, session)
        try:
            conn.execute(insert_query, values)
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            if cls.get_info(username=username):
                return False, 'username already taken'
            if cls.get_info(phone_number=phone_number):
                return False, 'phone number already taken'
            if cls.get_info(email=email):
                return False, 'email already taken'
        else:
            return True, session

    @classmethod
    def update_user_password_by_username(cls, username, password):
        """Gets user's id and new password. The function updates the user's password.
        *NOTE: If the user id is not in the database, or if the password is None, the function does nothing."""

        if password is not None:
            hashed, salt = cls.encrypt_password(password)
            conn = sqlite3.connect(FILE_PATH)
            query = f"UPDATE {cls.__tableName} SET {cls.__password} = ?, {cls.__salt} = ? WHERE {cls.__username} = ?;"
            conn.execute(query, (hashed, salt, username))
            conn.commit()
            conn.close()
            # print("password updated successfully")
        else:
            print("password did not changed. password must not be None.")

    @classmethod
    def encrypt_password(cls, password: str, salt=None):
        """The function is used to get the hash value of a password+salt+pepper.
        :param password - the original password
        :param salt - optional. If given, the function will calculate its value using this salt.
        if not given, the function will create a new random salt.

        :return a tuple with the hashed value and the used salt."""

        # if not given, create a new random salt.
        if not salt:
            salt = random_string(8, 16)

        # calculate the hash value
        password += salt + cls.__PEPPER
        password = sha256(password.encode()).hexdigest()

        # return the hashed value and the used salt
        return password, salt

    @classmethod
    def get_info(cls, *, username=None, phone_number=None, email=None, session=None):
        conn = sqlite3.connect(FILE_PATH)

        query, values = cls.get_search_query(username=username, phone_number=phone_number, email=email, session=session)

        data = conn.execute(query, values).fetchone()
        conn.commit()
        conn.close()
        return data

    @classmethod
    def get_search_query(cls, **kwargs):
        kwargs = {k: v for k, v in kwargs.items() if v is not None}
        assert bool(kwargs), "No data was given"
        # column_names = {'username': cls.__username,
        #                 'password': cls.__password,
        #                 'phone_number': cls.__phoneNumber,
        #                 'email': cls.__email,
        #                 'session': cls.__session}

        query = f"SELECT * FROM {cls.__tableName} WHERE "
        values = []
        for k, v in kwargs.items():
            # visualization for k = 'phone_number'
            # cls.__dict__[f'_{cls.__name__}__{k}'] ->
            # cls.__dict__[_Users__phone_number] -> cls.__phone_number -> phoneNumber
            query += f"{cls.__dict__[f'_{cls.__name__}__{k}']} = ? AND "
            values.append(v)
        query = query[:-5] + ';'
        return query, values

    @classmethod
    def try_login(cls, username, password):
        if (data := cls.get_info(username=username)) is None:
            return False, 'username doesnt exists'
        real_hashed, real_salt = data[1:3]
        hashed_input = cls.encrypt_password(password, salt=real_salt)[0]

        if real_hashed == hashed_input:
            return True, cls.set_session(username)
        return False, 'wrong password'

    @classmethod
    def set_session(cls, username, clear=False):
        conn = sqlite3.connect(FILE_PATH)
        query = f"UPDATE {cls.__tableName} SET {cls.__session} = ? WHERE {cls.__username} = ?;"
        session = None if clear else cls.get_new_session()
        conn.execute(query, (session, username))
        conn.commit()
        conn.close()
        return session

    @classmethod
    def get_new_session(cls):
        session = random_string(16, 16)
        conn = sqlite3.connect(FILE_PATH)
        query = f"SELECT * FROM {cls.__tableName} WHERE {cls.__session} = ?;"
        while conn.execute(query, (session,)).fetchone():
            session = random_string(16, 16)
        return session


def random_string(a, b):
    all_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()?'
    st = ''.join([random.choice(all_chars) for c in range(random.randint(a, b))])
    return st


def main():
    # print(Users.insert_user('user1', 'pass1', '0551234567', 'email12@gmail.com'))
    # print(Users.get_info(username='user1'))
    # print(Users.try_login('user1', 'pass1'))
    # Users.update_user_password_by_username('user1', 'pass1')
    # print(Users.get_info(phone_number='user1'))
    # print(Users.try_login('user1', 'pass1'))
    # print(Users.try_login('user3', 'pass3'))
    # print(Users.get_search_query(username='user', phone_number='email'))
    Users.set_session('user1', True)


if __name__ == '__main__':
    main()
