import sqlite3
import hashing


class registerRecord:
    def __init__(self, username, password, confirmedPassword,
                 title, firstName, lastName, email, authority):
        self.username = Username(username)
        self.password = Password(password, confirmedPassword)
        self.title = title
        self.names = Names(firstName, lastName)
        self.email = Email(email)
        self.authority = authority
        self.validArray = [
            [self.username.checkUnique(), 0],
            [self.password.getStrong(), 1],
            [self.password.getConfirmed(), 2],
            [self.names.checkValidity()[0], 3],
            [self.names.checkValidity()[1], 4],
            [self.email.checkValid(), 5],
        ]

    def addRecord(self, database, fn):
        registered = False
        if any(i[0] is False for i in self.validArray):
            for i in self.validArray:
                if i[0] is False:
                    fn(i[1])
        else:
            if self.authority == 'student':
                database.addUser(
                    self.username.getUsername(),
                    hashing.hashIt(self.password.getPassword()),
                    self.title,
                    self.names.getNames()[0],
                    self.names.getNames()[1],
                    self.email.getEmail(),
                    1
                )

            elif self.authority == 'teacher':
                database.addUser(
                    self.username.getUsername(),
                    hashing.hashIt(self.password.getPassword()),
                    self.title,
                    self.names.getNames()[0],
                    self.names.getNames()[1],
                    self.email.getEmail(),
                    2
                )
            registered = True
        # print(f'plaintext password: {self.password.getPassword()}')
        # print(f'hashed password: {hashing.hashIt(self.password.getPassword())}')
        return registered


class Username:
    def __init__(self, username):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.username = username
        self.unique = True

    def checkUnique(self):
        self.c.execute(
            '''SELECT username 
            FROM users 
            WHERE username=?''',
            (self.username,)
        )
        rows = self.c.fetchall()
        if rows:
            self.unique = False
        return self.unique

    def getUsername(self):
        return self.username


class Password:
    def __init__(self, password, confirmedPassword):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.password = password
        self.confirmedPassword = confirmedPassword
        self.confirmed = False
        self.strong = True

    def checkStrength(self):
        if not any('a' <= c <= 'z' for c in self.password):
            # print("lowercase")
            self.strong = False
        if not any('A' <= c <= 'Z' for c in self.password):
            # print("uppercase")
            self.strong = False
        if not any(c.isdigit() for c in self.password):
            # print("number")
            self.strong = False
        if not 8 <= len(self.password) <= 20:
            # print("length")
            self.strong = False
        if self.password == self.confirmedPassword:
            # print("password confirmed")
            self.confirmed = True

    def getStrong(self):
        self.checkStrength()
        return self.strong

    def getConfirmed(self):
        self.checkStrength()
        return self.confirmed

    def getPassword(self):
        return self.password


class Names:
    def __init__(self, first, last):
        self.fName = first
        self.lName = last
        self.fValid = True
        self.lValid = True

    def checkValidity(self):
        if any(c.isdigit() for c in self.fName):
            # print("first")
            self.fValid = False
        if any(c.isdigit() for c in self.lName):
            # print("last")
            self.lValid = False
        if self.fValid is False or self.lValid is False:
            return self.fValid, self.lValid
        else:
            self.fName = self.fName.title()
            self.lName = self.lName.title()
            # print(self.fName, self.lName)
            return self.fValid, self.lValid

    def getNames(self):
        return self.fName, self.lName


class Email:
    def __init__(self, email):
        self.email = email
        self.unique = True
        self.valid = True

    def checkValid(self):
        pos1 = 0
        pos2 = 0
        if any(c == '@' for c in self.email):
            for character in self.email:
                if character == '@':
                    break
                pos1 += 1
        else:
            self.valid = False

        if any(c == '.' for c in self.email):
            for character in self.email:
                if character == '.':
                    break
                pos2 += 1
            if pos1 > pos2:
                self.valid = False
        else:
            self.valid = False
        return self.valid

    def getEmail(self):
        return self.email
