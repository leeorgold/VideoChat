import sqlite3
import random
from hashlib import sha256

FILE_NAME = 'videochat.db'


class Users:
    """Creates database with users table includes:
       create query
       insert query
       select query
    """

    __tableName = "users"
    __password = "password"
    __username = "username"
    __phoneNumber = "phoneNumber"
    __email = "email"
    __salt = "salt"
    __PAPER = "JdLO5ZCsHor7^TLH"

    conn = sqlite3.connect(FILE_NAME)
    print("Opened database successfully:)")
    query_str = f"CREATE TABLE IF NOT EXISTS {__tableName} ({__username} TEXT    NOT NULL    PRIMARY KEY    UNIQUE, " \
                f"{__password} TEXT    NOT NULL , " \
                f"{__salt} TEXT    NOT NULL , " \
                f"{__phoneNumber} TEXT   NOT NULL    UNIQUE , " \
                f"{__email} TEXT    NOT NULL    UNIQUE);"

    conn.execute(query_str)
    print("Table created successfully")
    conn.commit()
    conn.close()

    def __init__(self):
        raise Exception("DON'T CREATE INSTANCES YOU MORON")

    @classmethod
    def get_table_name(cls):
        return cls.__tableName

    @classmethod
    def insert_user(cls, username, password, phone_number, email):
        """Gets a new user's data and adds it to the database."""

        conn = sqlite3.connect(FILE_NAME)
        insert_query = f"INSERT INTO {cls.__tableName} ({cls.__username}, {cls.__password},{cls.__salt}," \
                       f" {cls.__phoneNumber}, {cls.__email}) VALUES (?, ?, ?, ?, ?); "
        print(insert_query)
        password, salt = cls.encrypt_password(password)
        values = (username, password, salt, phone_number, email)
        conn.execute(insert_query, values)
        conn.commit()
        conn.close()
        print("Record created successfully")

    @classmethod
    def update_user_password_by_username(cls, username, password=None):
        """Gets user's id and new password. The function updates the user's password.
        *NOTE: If the user id is not in the database, or if the password is None, the function does nothing."""

        if password is not None:
            conn = sqlite3.connect(FILE_NAME)
            delete_query = f"UPDATE {cls.__tableName} SET {cls.__password} = ? WHERE {cls.__username} = ?;"
            print(delete_query)
            conn.execute(delete_query, (password, username))
            conn.commit()
            conn.close()
            print("password updated successfully")
        else:
            print("password did not changed. password must not be None.")

    @classmethod
    def encrypt_password(cls, password: str, salt=None):
        if not salt:
            salt = random_salt()
        password += salt + cls.__PAPER
        password = sha256(password.encode()).hexdigest()
        return password, salt


def random_salt():
    all_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ123456789!@#$%^&*()?'
    st = ''
    for c in range(random.randint(8, 16)):
        st += random.choice(all_chars)
    return st


def main():
    Users.insert_user('user2', 'pass2', '0511234567', 'email2@gmail.com')


if __name__ == '__main__':
    main()
