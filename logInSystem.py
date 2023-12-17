import sqlite3


class UsernameInput:
    def __init__(self, username):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.username = username
        self.password = ''

    def getPassword(self):
        self.c.execute(
            '''SELECT password
            FROM users
            WHERE username=?''',
            (self.username,)
        )
        password = self.c.fetchall()
        if password:
            self.password = list(password[0])[0]
        return self.password

    def getUsername(self):
        return self.username
