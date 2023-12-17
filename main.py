from tkinter import *
from tkinter import messagebox
from tkinter import ttk as t
import tkinter.ttk as ttk
import classes
from hashing import hashIt
import sqlSetUp
import logInSystem
import registerSystem
import graphs


class main(classes.window):
    def __init__(self, win):
        self.win = win
        self.colourMode = 'light'
        self.oppositeColourMode = classes.oppositeColourMode('light')

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, False)
        self.win.title('Main Menu')
        self.win.protocol('WM_DELETE_WINDOW', self.quitProgram)
        self.win.configure(bg=classes.colours[self.colourMode][0])

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            400,
            75,
            text='Maths Practice',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.button1.config(
            text='Log In',
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1],
            command=lambda: self.logInWindow(None),
            width=20,
            font=('Arial', 18)
        )
        self.button1.bind('<Return>', self.logInWindow)
        self.button1.place(x=260, y=150)

        self.button2.config(
            text='Register',
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1],
            command=lambda: self.registerWindow(None),
            width=20,
            font=('Arial', 18)
        )
        self.button2.bind('<Return>', self.registerWindow)
        self.button2.place(x=260, y=220)

        self.sideMenu = classes.sideMenu(
            self.win,
            self.quitProgram,
            '',
            '',
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )
        self.button1.focus()

        self.database = sqlSetUp.Database()
        self.database.createTables()
        #self.database.insertValues()

        try:
            self.database.insertValues()
        except:
            pass

        self.toggleColoursButton = Button(
            self.win,
            text='Dark Mode',
            command=self.toggleColours,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.toggleColoursButton.place(x=720, y=110)

        self.widgets = [
            self.button1,
            self.button2,
            self.toggleColoursButton
        ]

    def logInWindow(self, event):
        openWindow = Toplevel(self.win)
        logInWin(
            openWindow,
            self.database,
            self,
            self.colourMode
        )
        self.win.withdraw()

    def registerWindow(self, event):
        openWindow = Toplevel(self.win)
        registerWin(
            openWindow,
            self.database,
            self,
            self.colourMode
        )
        self.win.withdraw()

    def toggleColours(self):
        self.topCanvas.itemconfig(
            self.welcomeLabel,
            fill=classes.colours[self.colourMode][1]
        )
        for widget in self.widgets:
            widget.config(fg=classes.colours[self.colourMode][1])
        if self.colourMode == 'light':
            self.colourMode = 'dark'
            self.oppositeColourMode = 'light'
            self.toggleColoursButton.config(text='Light Mode')
        else:
            self.colourMode = 'light'
            self.oppositeColourMode = 'dark'
            self.toggleColoursButton.config(text='Dark Mode')

        self.topCanvas.config(bg=classes.colours[self.colourMode][1])
        for widget in self.widgets:
            widget.config(bg=classes.colours[self.colourMode][1])
        self.win.configure(bg=classes.colours[self.colourMode][0])
        self.sideMenu.changeColours(
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

    def quitProgram(self):
        getExit = messagebox.askyesno(
            title='Quit',
            message='Are you sure you want to quit?',
            parent=self._newWindow
        )
        if getExit > 0:
            self._newWindow.destroy()
        return


class logInWin(classes.window):
    def __init__(self, win, database, parent, colourMode):
        self.win = win
        self.database = database
        self.parent = parent
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)
        self.loggedIn = False
        self.userLoggedIn = ''

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Log In')
        self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.win.configure(bg=classes.colours[self.colourMode][0])

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            400,
            75,
            text='Log In',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.sideMenu = classes.sideMenu(
            self.win,
            self.closeWindow,
            '',
            '',
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

        self.usernameLabel = Label(
            self.win,
            text='Username:',
            font=('Arial', 14, 'bold'),
            bg=classes.colours[self.colourMode][0],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.usernameEntry = classes.entrybox(
            self.win,
            'username',
            1,
            classes.colours[self.oppositeColourMode][1],
            classes.colours[self.colourMode][1]
        )
        self.usernameEntry. entryBox.config(
            bg=classes.colours[self.colourMode][1]
        )
        self.usernameEntry.entryBox.place(x=360, y=140)
        self.usernameLabel.place(x=235, y=140)
        self.usernameEntry.entryBox.focus()

        self.passwordLabel = Label(
            self.win,
            text='Password:',
            font=('Arial', 14, 'bold'),
            bg=classes.colours[self.colourMode][0],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.passwordEntry = classes.entrybox(
            self.win,
            'password',
            0,
            classes.colours[self.oppositeColourMode][1],
            classes.colours[self.colourMode][1]
        )
        self.passwordEntry.entryBox.config(
            bg=classes.colours[self.colourMode][1]
        )
        self.passwordEntry.entryBox.place(x=360, y=180)
        self.passwordLabel.place(x=235, y=180)

        self.submitButton = Button(
            self.win,
            text='Submit',
            font=('Arial', 20),
            command=self.logIn
        )
        self.submitButton.place(x=350, y=240)

        self.usernameErrorMsg = 'Username not found'
        self.passwordErrorMsg = 'Password incorrect'
        self.errorLabel = Label(
            self.win,
            font=('Arial', 20),
            bg=classes.colours[self.colourMode][0],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.errorLabel.place(x=280, y=340)

        self.showPasswordButton = classes.eyeButton(self.win)
        self.showPasswordButton.setDown(self.updatedShowPassword)
        #self.showPasswordButton.setUp(self.hidePassword)
        self.showPasswordButton.eyeButton.place(x=650, y=180)

    def showPassword(self, event):
        self.passwordEntry.entryBox.config(show='')

    def hidePassword(self, event):
        if self.passwordEntry.entryBox.get() != 'Enter password':
            self.passwordEntry.entryBox.config(show='•')

    def updatedShowPassword(self, event):
        show = self.passwordEntry.entryBox['show']
        entry = self.passwordEntry.entryBox.get()
        if show == '':
            if entry != 'Enter password':
                self.passwordEntry.entryBox.config(show='•')
        else:
            self.passwordEntry.entryBox.config(show='')

    def logIn(self):
        checkUsername = self.usernameEntry.entryBox.get()
        checkPassword = hashIt(self.passwordEntry.entryBox.get())
        # print(f'entered password: {checkPassword}')
        username = logInSystem.UsernameInput(checkUsername)
        password = username.getPassword()
        # print(f'password from database: {password}')
        if password == '':
            self.usernameEntry.entryBox.delete(0, 'end')
            self.passwordEntry.entryBox.delete(0, 'end')
            self.usernameEntry.entryBox.config(
                highlightbackground='red',
                highlightthickness=2,
                highlightcolor='red'
            )
            self.passwordEntry.entryBox.config(
                show='',
                fg='dark grey',
                highlightbackground='red',
                highlightthickness=2,
                highlightcolor='red'
            )
            self.passwordEntry.entryBox.insert(0, 'Enter password')
            self.usernameEntry.entryBox.focus()
            self.errorLabel.config(text=self.usernameErrorMsg)
            return

        if password != checkPassword:
            self.passwordEntry.entryBox.delete(0, 'end')
            self.passwordEntry.entryBox.config(
                show='',
                fg='dark grey',
                highlightbackground='red',
                highlightthickness=2,
                highlightcolor='red'
            )
            self.passwordEntry.entryBox.insert(0, 'Enter password')
            self.usernameEntry.entryBox.focus()
            self.errorLabel.config(text=self.passwordErrorMsg)
            return

        self.userLoggedIn = self.database.getUser(checkUsername)
        #print(self.userLoggedIn)
        self.win.withdraw()
        openWindow = Toplevel(self.win)
        if self.userLoggedIn[-1] == 1:
            mainApp = studentMathsProgram(
                openWindow,
                self.database,
                self.userLoggedIn,
                self
            )
        elif self.userLoggedIn[-1] == 2:
            mainApp = teacherMathsProgram(
                openWindow,
                self.database,
                self.userLoggedIn,
                self
            )
        elif self.userLoggedIn[-1] == 3:
            mainApp = adminMathsProgram(
                openWindow,
                self.database,
                self.userLoggedIn,
                self
            )
        self.loggedIn = True
        # self.closeWindow()

    def getUserLoggedIn(self):
        return self.userLoggedIn

    def closeWindow(self):
        if not self.loggedIn:
            try:
                self.parent.registered = False
            except:
                pass
            self.parent.windowDimensions(800, 600, self)
            self.parent.win.deiconify()
        self._newWindow.destroy()


class registerWin(classes.window):
    def __init__(self, win, database, parent, colourMode):
        self.win = win
        self.database = database
        self.parent = parent
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)
        self.var = StringVar(self.win, '1')
        self.registered = False

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Register Account')
        self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.win.configure(bg=classes.colours[self.colourMode][0])

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            400,
            75,
            text='Register',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.entryBoxes = [
            [
                'usernameLabel', 'usernameEntry',
                'username', 235, 180, 1
            ],
            [
                'passwordLabel', 'passwordEntry',
                'password', 235, 220, 0
            ],
            [
                'confirmPasswordLabel', 'confirmPasswordEntry',
                'confirm password', 158, 260, 0
            ],
            [
                'firstNameLabel', 'firstNameEntry',
                'first name', 230, 300, 1
            ],
            [
                'lastNameLabel', 'lastNameEntry',
                'last name', 230, 340, 1
            ],
            [
                'emailLabel', 'emailEntry',
                'email', 280, 380, 1
            ]
        ]
        self.studentRadioButton = Radiobutton(
            self.win,
            text='Student',
            value='student',
            variable=self.var,
            font=('Arial', 14),
            bg=classes.colours[self.colourMode][0],
            fg=classes.colours[self.oppositeColourMode][1],
            selectcolor=classes.colours[self.colourMode][0]
        )
        self.teacherRadioButton = Radiobutton(
            self.win,
            text='Teacher',
            value='teacher',
            variable=self.var,
            font=('Arial', 14),
            bg=classes.colours[self.colourMode][0],
            fg=classes.colours[self.oppositeColourMode][1],
            selectcolor=classes.colours[self.colourMode][0]
        )
        self.studentRadioButton.place(x=250, y=140)
        self.teacherRadioButton.place(x=500, y=140)
        self.studentRadioButton.select()

        self.entries = []
        for box in self.entryBoxes:
            box[0] = Label(
                self.win,
                text=f'{box[2].title()}:',
                font=('Arial', 14, 'bold'),
                bg=classes.colours[self.colourMode][0],
                fg=classes.colours[self.oppositeColourMode][1]
            )
            box[1] = classes.entrybox(
                self.win,
                box[2],
                box[5],
                classes.colours[self.oppositeColourMode][1],
                classes.colours[self.colourMode][1]
            )
            box[0].place(x=box[3], y=box[4])
            box[1].entryBox.place(x=360, y=box[4])
            self.entries.append(box[1])
        self.entries[0].entryBox.focus()

        self.showPasswordButton = classes.eyeButton(self.win)
        self.showPasswordButton.setDown(self.showPassword)
        self.showPasswordButton.setUp(self.hidePassword)
        self.showPasswordButton.eyeButton.place(x=650, y=220)

        self.submitButton = Button(
            self.win,
            text='Submit',
            font=('Arial', 20),
            command=self.getValues
        )
        self.submitButton.place(x=350, y=420)

        self.title = ttk.Combobox(
            self.win,
            width=5,
            font=('Arial', 14),
            values=['Mr', 'Ms', 'Mrs', 'Dr', 'Prof'],
            state='readonly'
        )
        self.title.place(x=650, y=300)

        self.sideMenu = classes.sideMenu(
            self.win,
            self.closeWindow,
            '',
            '',
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

    def showPassword(self, event):
        for item in [self.entries[1], self.entries[2]]:
            item.entryBox.config(show='')

    def hidePassword(self, event):
        for item in [self.entries[1], self.entries[2]]:
            if item.entryBox.get() != f'Enter {item.getText()}':
                item.entryBox.config(show='•')

    def getValues(self):
        record = registerSystem.registerRecord(
            self.entries[0].entryBox.get(),
            self.entries[1].entryBox.get(),
            self.entries[2].entryBox.get(),
            self.title.get(),
            self.entries[3].entryBox.get(),
            self.entries[4].entryBox.get(),
            self.entries[5].entryBox.get(),
            self.var.get()
        )
        registered = record.addRecord(
            self.database,
            self.resetEntry
        )

        for item in self.entries:
            item.entryBox.delete(0, 'end')
            if item != self.entries[0]:
                item.entryBox.config(show='', fg='dark grey')
            item.entryBox.insert(0, f'Enter {item.getText()}')
        self.entries[0].entryBox.delete(0, 'end')
        self.entries[0].entryBox.focus()

        if registered:
            getLogIn = messagebox.askyesno(
                title='Log In',
                message='Registered account. Do you want to log in?',
                parent=self._newWindow
            )
            if getLogIn > 0:
                self.win.withdraw()
                openWindow = Toplevel(self.win)
                logInWin(
                    openWindow,
                    self.database,
                    self,
                    self.colourMode
                )
                self.registered = True

    def resetEntry(self, value):
        self.entries[value].entryBox.delete(0, 'end')
        self.entries[value].entryBox.config(
            highlightbackground='red',
            highlightthickness=2,
            highlightcolor='red'
        )

    def closeWindow(self):
        if not self.registered:
            self.parent.windowDimensions(800, 600, self)
            self.parent.win.deiconify()
        self._newWindow.destroy()


class studentMathsProgram(classes.window):
    def __init__(self, win, database, user, parent):
        self.win = win
        self.database = database
        self.userLoggedIn = user
        self.parent = parent
        colour, opposite = self.database.getColourMode(
            self.userLoggedIn[0]
        )
        self.colourMode = colour
        self.oppositeColourMode = opposite
        self.questionSet = []
        self.values = self.database.getNumberOfQuestions()
        self.currentTest = None

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Maths Revision App: Student')
        self.win.protocol(
            'WM_DELETE_WINDOW',
            lambda: self.closeWindow(True)
        )
        self.win.configure(
            bg=classes.colours[self.colourMode][0]
        )

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)

        self.welcomeLabel = self.topCanvas.create_text(
            400,
            75,
            text=f'Welcome, {self.userLoggedIn[4].title()}',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.testButton = Button(
            self.win,
            text='Generate Test',
            command=self.testGeneration,
            font=('Arial', 18),
            width=16,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.testButton.place(x=275, y=150)
        self.spinbox = Spinbox(
            self.win,
            font=('Arial', 18),
            width=5,
            from_=10,
            to=30,
            state='readonly'
        )
        self.spinbox.place(x=515, y=158)

        self.viewTestsButton = Button(
            self.win,
            text='View Previous Tests',
            command=self.viewTests,
            font=('Arial', 18),
            width=16,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.viewTestsButton.place(x=275, y=210)

        self.checkAssignmentsButton = Button(
            self.win,
            text='Check Assignments',
            command=self.checkAssignments,
            font=('Arial', 18),
            width=16,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.checkAssignmentsButton.place(x=275, y=270)

        self.toggleColoursButton = Button(
            self.win,
            text='Dark Mode',
            command=self.toggleColours,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.toggleColoursButton.place(x=720, y=110)

        self.widgets = [
            self.testButton,
            self.viewTestsButton,
            self.checkAssignmentsButton,
            self.toggleColoursButton
        ]

        self.sideMenu = classes.sideMenu(
            self.win,
            lambda: self.closeWindow(True),
            '',
            '',
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

    def testGeneration(self):
        self.currentTest = sqlSetUp.Test(
            int(self.spinbox.get()),
            self.database
        )
        self.questionSet = self.currentTest.selectQuestions()
        self.win.withdraw()
        openWindow = Toplevel(self.win)
        testWin = testWindow(
            openWindow,
            self.questionSet,
            int(self.spinbox.get()),
            self.database,
            self,
            self.userLoggedIn,
            self.currentTest,
            'random',
            self.colourMode
        )
        # self.closeWindow(False)

    def viewTests(self):
        self.win.withdraw()
        openWindow = Toplevel(self.win)
        viewTests = viewTestsWindow(
            openWindow,
            self.database,
            self.userLoggedIn,
            self,
            self.colourMode
        )
        # self.closeWindow(False)

    def checkAssignments(self):
        self.win.withdraw()
        openWindow = Toplevel(self.win)
        checkAssignments = checkAssignmentsWindow(
            openWindow,
            self.database,
            self.userLoggedIn,
            self,
            self.colourMode
        )
        # self.closeWindow(False)

    def toggleColours(self):
        self.topCanvas.itemconfig(
            self.welcomeLabel,
            fill=classes.colours[self.colourMode][1]
        )
        for widget in self.widgets:
            widget.config(fg=classes.colours[self.colourMode][1])
        if self.colourMode == 'light':
            self.colourMode = 'dark'
            self.oppositeColourMode = 'light'
            self.toggleColoursButton.config(text='Light Mode')
        else:
            self.colourMode = 'light'
            self.oppositeColourMode = 'dark'
            self.toggleColoursButton.config(text='Dark Mode')

        self.topCanvas.config(bg=classes.colours[self.colourMode][1])
        for widget in self.widgets:
            widget.config(bg=classes.colours[self.colourMode][1])
        self.win.configure(bg=classes.colours[self.colourMode][0])
        self.database.updateColourMode(
            self.userLoggedIn[0],
            self.colourMode
        )
        self.sideMenu.changeColours(
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )


    def closeWindow(self, enable):
        if enable:
            app.windowDimensions(800, 600, self)
            app.win.deiconify()
        self._newWindow.destroy()


class testWindow(classes.window):
    def __init__(self, win, questions, lastQuestion, database,
                 parent, user, test, state, colourMode):
        self.win = win
        self.questionSet = questions
        self.lastQuestion = lastQuestion
        self.database = database
        self.parent = parent
        self.user = user
        self.currentTest = test
        self.state = state
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)
        self.testComplete = False
        self.score = 0

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Test')
        self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.win.configure(bg=classes.colours[colourMode][0])

        container = Frame(
            self.win,
            bg=classes.colours[colourMode][0]
        )
        container.pack(
            side='top',
            fill='both',
            expand=True
        )
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = []
        self.questionNum = 0
        for question in self.questionSet:
            self.questionNum += 1
            frame = classes.questionFrame(
                container,
                self,
                self.questionNum,
                self.questionSet,
                self.lastQuestion,
                classes.colours[self.colourMode],
                classes.colours[self.oppositeColourMode]
            )
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky='nsew')

        frame = classes.endFrame(
            container,
            self,
            self.questionSet,
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )
        frame.grid(row=0, column=0, sticky='nsew')
        self.frames.append(frame)
        self.showFrame(0)

        self.frames[-1].submitButton.config(
            command=self.submitButtonCommand
        )

    def showFrame(self, index):
        frame = self.frames[index]
        if index == 0:
            frame.disableButton('previous')
        if index == -1:
            completeQuestions = self.setBoxes()
            if completeQuestions < len(self.frames) - 1:
                self.frames[-1].submitButton.config(state='disabled')
            else:
                self.frames[-1].submitButton.config(state='active')
        frame.tkraise()

    def setBoxes(self):
        answers = []
        for i in range(len(self.frames) - 1):
            frame = self.frames[i].getAnswer()
            answers.append(frame)
        index = 0
        numberOfCompleteQuestions = 0
        for answer in answers:
            if answer is None:
                self.frames[-1].questionButtons[index].config(bg='yellow')
            else:
                self.frames[-1].questionButtons[index].config(bg='green')
                numberOfCompleteQuestions += 1
            index += 1
        return numberOfCompleteQuestions

    def calculateScore(self):
        self.score = 0
        for i in range(len(self.frames) - 1):
            if self.frames[i].getAnswer():
                self.score += 1
        return self.score

    def getQuestionAnswersAsArray(self):
        array = []
        for i in range(len(self.frames) - 1):
            array.append(
                [self.frames[i].getQuestionID(),
                 self.frames[i].getAnswer()]
            )
        return array

    def finalButtonCommand(self):
        for i in range(len(self.frames) - 2):
            self.frames[i].button2.config(
                text='Review answers',
                command=lambda: self.showFrame(-1)
            )
        self.showFrame(-1)

    def submitButtonCommand(self):
        score = self.calculateScore()
        if score > 5:
            message = f'Congratulations! You scored {score}, ' \
                      f'do you want to submit this test?'
        else:
            message = f'Nice try! You scored {score}, ' \
                      f'do you want to submit this test?'
        submitTest = messagebox.askyesno(
            title='Submit Test?',
            message=message,
            parent=self.win
        )
        if submitTest:
            # adds test into test table
            # data held: testID, #Questions

            #if self.currentTest.testID is None:
            if self.state == 'random':
                self.database.addTest(
                    self.currentTest.getNumberOfQuestions()
                )
                self.currentTest.setTestID(
                    self.database.getLatestTestID()
                )
                self.currentTest.insertIntoDatabase(
                    self.questionSet
                )
            self.database.addAnswers(
                self.getQuestionAnswersAsArray(),
                self.currentTest.testID,
                self.user
            )
            self.database.addStudentPerformance(
                self.user,
                self.currentTest.testID,
                score
            )
            #try:
            if self.state == 'assignment':
                self.database.setCompleteAssignmentsTrue(
                    self.currentTest.testID,
                    self.user[0]
                )
                self.parent.setTree(self.user)
            elif self.state == 'retake':
                self.parent.resetValues()

            #except:
            #    pass
            #try:
            #    self.parent.resetValues()
            #except:
            #    pass
            self.closeWindow()

    def closeWindow(self):
        self.parent.windowDimensions(800, 600, self)
        self.parent.win.deiconify()
        self._newWindow.destroy()
        # openWindow = Toplevel(self.win)
        # studentMathsProgram(openWindow, self.database, self.user, self)


class viewTestsWindow(classes.window):
    def __init__(self, win, database, user, parent, colourMode):
        self.win = win
        self.database = database
        self.user = user
        self.parent = parent
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)
        self.testData = None

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('View tests')
        self.win.protocol(
            'WM_DELETE_WINDOW',
            lambda: self.closeWindow(True)
        )
        self.win.configure(
            bg=classes.colours[self.colourMode][0]
        )

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)

        self.welcomeLabel = self.topCanvas.create_text(
            225,
            75,
            text=f'Previous Tests',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.testTreeFrame = Frame(self.win)
        self.testTreeFrame.place(x=50, y=110)

        self.testTreeScroll = Scrollbar(self.testTreeFrame)
        self.testTreeScroll.pack(side=RIGHT, fill=Y)

        self.style = t.Style()
        self.style.theme_use('default')
        self.style.configure(
            'Treeview',
            background=classes.colours[self.colourMode][1],
            foreground=classes.colours[self.oppositeColourMode][0],
            rowheight=20,
            fieldbackground=classes.colours[self.colourMode][1]
        )
        self.style.map(
            'Treeview',
            background=[
                (
                    'selected',
                    classes.colours[self.colourMode][2]
                )
            ],
            foreground=[
                (
                    'selected',
                    classes.colours[self.oppositeColourMode][1]
                )
            ]
        )

        self.testTree = t.Treeview(
            self.testTreeFrame,
            columns=('testID', 'Percentage'),
            selectmode=BROWSE,
            yscrollcommand=self.testTreeScroll.set
        )
        self.testTree.pack()

        self.testTreeScroll.config(
            command=self.testTree.yview
        )

        self.testTree.column(
            '#0',
            width=120,
            minwidth=25
        )
        self.testTree.column(
            'testID',
            width=110,
            minwidth=25,
            anchor=CENTER
        )
        self.testTree.column(
            'Percentage',
            width=120,
            minwidth=25,
            anchor=CENTER
        )

        self.testTree.heading(
            '#0',
            text='Attempt Number',
            anchor=CENTER
        )
        self.testTree.heading(
            'testID',
            text='Test Number',
            anchor=CENTER
        )
        self.testTree.heading(
            'Percentage',
            text='Percentage',
            anchor=CENTER
        )

        # Create striped row tags
        self.testTree.tag_configure(
            'odd',
            background=classes.colours[self.colourMode][1]
        )
        self.testTree.tag_configure(
            'even',
            background=classes.colours[self.colourMode][0]
        )

        # new treeView showing each test question/answer
        self.questionTreeFrame = Frame(self.win)
        self.questionTreeFrame.place(x=275, y=340)

        self.questionTreeScroll = Scrollbar(self.questionTreeFrame)
        self.questionTreeScroll.pack(side=RIGHT, fill=Y)

        self.questionTree = t.Treeview(
            self.questionTreeFrame,
            columns=('Question', 'Correct'),
            selectmode=BROWSE,
            yscrollcommand=self.questionTreeScroll.set
        )
        self.questionTree.pack()

        self.questionTreeScroll.config(
            command=self.questionTree.yview
        )

        self.questionTree.column(
            '#0',
            width=0,
            stretch=NO
        )
        self.questionTree.column(
            'Question',
            width=400,
            minwidth=25,
            anchor=W
        )
        self.questionTree.column(
            'Correct',
            width=80,
            minwidth=25,
            anchor=CENTER
        )

        self.questionTree.heading(
            'Question',
            text='Question',
            anchor=CENTER
        )
        self.questionTree.heading(
            'Correct',
            text='Correct',
            anchor=CENTER
        )

        # Create striped row tags
        self.questionTree.tag_configure(
            'odd',
            background=classes.colours[self.colourMode][1]
        )
        self.questionTree.tag_configure(
            'even',
            background=classes.colours[self.colourMode][0]
        )

        self.questionTreeLabel = Label(
            self.win,
            font=('Arial', 18),
            bg=classes.colours[self.colourMode][0],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.questionTreeLabel.place(x=50, y=340)

        self.retakeButton = Button(
            self.win,
            text="Retake Test",
            font=("Arial", 14),
            command=self.retakeTest,
            state='disabled',
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )

        self.resetValues()

    def resetValues(self):
        for record in self.testTree.get_children():
            self.testTree.delete(record)

        # Select previous tests from database
        self.testData = self.database.getTreeViewData(self.user[0])
        parentTests = []
        count = 0
        for test in self.testData:
            if count % 2 == 0:
                tag = ('even', )
            else:
                tag = ('odd', )

            # test[0] = userPracticeID
            # test[1] = score
            # test[2] = attemptNumber
            # test[3] = questions/answers
            # test[4] = testID
            # print(test)
            percentage = (test[1] / len(test[3])) * 100
            percentage = f'{percentage}%'
            if test[2] == 1:
                self.testTree.insert(
                    parent='',
                    index='end',
                    iid=test[0],
                    text='Attempt 1',
                    values=(test[4], percentage),
                    tags=tag
                )
                parentTests.append(test)
            else:
                for item in parentTests:
                    if item[4] == test[4]:
                        parent = item
                self.testTree.insert(
                    parent=f'{parent[0]}',
                    index='end',
                    iid=test[0],
                    text=f'Attempt {test[2]}',
                    values=(test[4], percentage),
                    tags=tag
                )
            count += 1

        self.retakeButton.place(x=660, y=150)
        #self.testTree.bind(
        #    '<ButtonRelease-1>',
        #    self.updateQuestionTreeView
        #)
        self.testTree.bind(
            '<<TreeviewSelect>>',
            self.updateQuestionTreeView
        )

    def retakeTest(self):
        # settings up values for the testWindow class
        openWindow = Toplevel(self.win)

        userPracticeID = self.testTree.focus()
        testID, questions = self.database.getRetakeTest(userPracticeID)
        # print(questions)
        currentTest = sqlSetUp.Test(len(questions), self.database)
        currentTest.setTestID(testID)
        # print(testDict)
        # print(testDict['values'])

        # win, questions, lastQuestion, database, parent
        retakeTestWindow = testWindow(
            openWindow,
            questions,
            len(questions),
            self.database,
            self,
            self.user,
            currentTest,
            'retake',
            self.colourMode
        )
        self.win.withdraw()
        # self.newWindow.destroy()

    def updateQuestionTreeView(self, event):
        # try:
        self.resetQuestionTree()
        userPracticeID = self.testTree.focus()
        testDict = self.testTree.item(self.testTree.focus())
        attempt = testDict['text']
        testID = testDict['values'][0]
        self.questionTreeLabel.config(text=f'Test {testID}, {attempt}:')
        questionsAnswers = self.database.getTestQuestions(userPracticeID)

        id = 0
        for item in questionsAnswers:
            if id % 2 == 0:
                tag = ('even', )
            else:
                tag = ('odd', )
            question, answer = item
            self.questionTree.insert(
                parent='',
                index='end',
                iid=id,
                values=(question, answer),
                tags=tag
            )
            id += 1
        self.retakeButton.config(state='normal')
        # except:
        #     if len(self.testTree.get_children()) > 0:
        #         errorBox = messagebox.showerror(
        #             'Error',
        #             'Please select a test',
        #             parent=self.newWindow
        #         )
        #     else:
        #         errorBox = messagebox.showerror(
        #             'Error',
        #             'No tests completed',
        #             parent=self.newWindow
        #         )

    def resetQuestionTree(self):
        for record in self.questionTree.get_children():
            self.questionTree.delete(record)

    def closeWindow(self, show):
        if show:
            self.parent.windowDimensions(800, 600, self)
            self.parent.win.deiconify()
        self._newWindow.destroy()

        # openWindow = Toplevel(self.win)
        # studentMathsProgram(openWindow, self.database, self.user, self)


class checkAssignmentsWindow(classes.window):
    def __init__(self, win, database, user, parent, colourMode):
        self.win = win
        self.database = database
        self.user = user
        self.parent = parent
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Check Classes')
        self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.win.configure(bg=classes.colours[self.colourMode][0])

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)

        self.welcomeLabel = self.topCanvas.create_text(
            225,
            75,
            text=f'Assignments',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.assignmentTreeFrame = Frame(self.win)

        self.assignmentTreeScroll = Scrollbar(self.assignmentTreeFrame)
        self.assignmentTreeScroll.pack(side=RIGHT, fill=Y)

        self.style = t.Style()
        self.style.theme_use('default')
        self.style.configure(
            'Treeview',
            background=classes.colours[self.colourMode][1],
            foreground=classes.colours[self.oppositeColourMode][0],
            rowheight=20,
            fieldbackground=classes.colours[self.colourMode][1]
        )
        self.style.map(
            'Treeview',
            background=[
                (
                    'selected',
                    classes.colours[self.colourMode][2]
                )
            ],
            foreground=[
                (
                    'selected',
                    classes.colours[self.oppositeColourMode][1]
                )
            ]
        )

        self.assignmentTree = t.Treeview(
            self.assignmentTreeFrame,
            columns=('Class', 'AssignmentID', 'Complete'),
            selectmode=BROWSE,
            yscrollcommand=self.assignmentTreeScroll.set
        )
        self.assignmentTree.pack()

        self.assignmentTreeScroll.config(command=self.assignmentTree.yview)

        self.assignmentTree.column(
            '#0',
            width=0,
            stretch=NO
        )
        self.assignmentTree.column(
            'Class',
            width=200,
            minwidth=50,
            anchor=CENTER
        )
        self.assignmentTree.column(
            'AssignmentID',
            width=200,
            minwidth=50,
            anchor=CENTER
        )
        self.assignmentTree.column(
            'Complete',
            width=200,
            minwidth=50,
            anchor=CENTER
        )

        self.assignmentTree.heading(
            'Class',
            text='Class',
            anchor=CENTER
        )
        self.assignmentTree.heading(
            'AssignmentID',
            text='Assignment',
            anchor=CENTER
        )
        self.assignmentTree.heading(
            'Complete',
            text='Complete?',
            anchor=CENTER
        )

        self.assignmentTreeFrame.place(x=50, y=125)

        self.assignmentTree.tag_configure(
            'odd',
            background=classes.colours[self.colourMode][1]
        )
        self.assignmentTree.tag_configure(
            'even',
            background=classes.colours[self.colourMode][0]
        )
        self.assignmentTree.tag_configure(
            'complete',
            background='green'
        )

        self.setTree(user)

        self.completeAssignmentButton = Button(
            self.win,
            text='Complete Assignment',
            command=self.completeAssignment,
            state='disabled',
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1],
            font=('Arial', 18)
        )
        self.completeAssignmentButton.place(x=225, y=375)
        self.assignmentTree.bind(
          '<ButtonRelease-1>',
          self.updateButton
        )

    def completeAssignment(self):
        openWindow = Toplevel(self.win)
        assignmentID = int(self.assignmentTree.item(
            self.assignmentTree.focus())['values'][1][10::]
        )
        # print(assignmentID)
        questions, testID = self.database.getQuestionsAndTestIDFromAssignmentID(assignmentID)
        # print(questions)
        test = sqlSetUp.Test(len(questions), self.database)
        test.setTestID(testID)

        testWin = testWindow(
            openWindow,
            questions,
            len(questions),
            self.database,
            self,
            self.user,
            test,
            'assignment',
            self.colourMode
        )

    def setTree(self, user):
        for record in self.assignmentTree.get_children():
            self.assignmentTree.delete(record)
        assignments = self.database.getStudentAssignments(user[0])
        # print(assignments)
        count = 0
        for assignment in assignments:
            if count % 2 == 0:
                tag = ('even', )
            else:
                tag = ('odd', )

            if assignment[2]:
                assignment[2] = True
                tag = ('complete', )
            else:
                assignment[2] = False

            self.assignmentTree.insert(
                parent='',
                index='end',
                iid=assignment[0],
                values=(
                    assignment[1],
                    f'Assignment {assignment[0]}',
                    assignment[2]
                ),
                tags=tag
            )
            count += 1

    def updateButton(self, event):
        self.completeAssignmentButton.config(state='normal')

    def closeWindow(self):
        self.parent.windowDimensions(800, 600, self)
        self.parent.win.deiconify()
        self._newWindow.destroy()


class teacherMathsProgram(classes.window):
    def __init__(self, win, database, user, parent):
        self.win = win
        self.database = database
        self.user = user
        self.parent = parent
        colour, opposite = self.database.getColourMode(
            self.user[0]
        )
        self.colourMode = colour
        self.oppositeColourMode = opposite

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Maths Revision App: Teacher')
        self.win.protocol(
            'WM_DELETE_WINDOW',
            lambda: self.closeWindow(True)
        )
        self.win.configure(
            bg=classes.colours[self.colourMode][0]
        )

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            400,
            75,
            text=f'Welcome, {self.user[3]}. {self.user[5]}',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.createClassButton = Button(
            self.win,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1],
            text='Create Class',
            command=self.createClass,
            font=('Arial', 18),
            width=16
        )
        self.createClassButton.place(x=275, y=150)

        self.viewClassButton = Button(
            self.win,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1],
            text='View Class',
            command=self.viewClass,
            font=('Arial', 18),
            width=16
        )
        self.viewClassButton.place(x=275, y=210)
        if not self.database.getClassIDs(self.user[0]):
            self.viewClassButton.config(state='disabled')

        self.toggleColoursButton = Button(
            self.win,
            text='Dark Mode',
            command=self.toggleColours,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.toggleColoursButton.place(x=720, y=110)

        self.sideMenu = classes.sideMenu(
            self.win,
            lambda: self.closeWindow(True),
            '',
            '',
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

        self.widgets = [
            self.createClassButton,
            self.viewClassButton,
            self.toggleColoursButton
        ]

    def createClass(self):
        self.win.withdraw()
        openWindow = Toplevel(self.win)
        studentsWin = viewStudents(
            openWindow,
            self.database,
            self.user,
            self,
            self.colourMode
        )

    def viewClass(self):
        self.win.withdraw()
        openWindow = Toplevel(self.win)
        classWindow = viewClasses(
            openWindow,
            self.database,
            self.user,
            self,
            self.colourMode
        )

    def toggleColours(self):
        self.topCanvas.itemconfig(
            self.welcomeLabel,
            fill=classes.colours[self.colourMode][1]
        )
        for widget in self.widgets:
            widget.config(fg=classes.colours[self.colourMode][1])
        if self.colourMode == 'light':
            self.colourMode = 'dark'
            self.oppositeColourMode = 'light'
            self.toggleColoursButton.config(text='Light Mode')
        else:
            self.colourMode = 'light'
            self.oppositeColourMode = 'dark'
            self.toggleColoursButton.config(text='Dark Mode')

        self.topCanvas.config(bg=classes.colours[self.colourMode][1])
        for widget in self.widgets:
            widget.config(bg=classes.colours[self.colourMode][1])
        self.win.configure(bg=classes.colours[self.colourMode][0])
        self.sideMenu.changeColours(
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )
        self.database.updateColourMode(
            self.user[0],
            self.colourMode
        )

    def closeWindow(self, enable):
        if enable:
            app.windowDimensions(800, 600, self)
            app.win.deiconify()
        self._newWindow.destroy()


class viewStudents(classes.window):
    def __init__(self, win, database, teacher, parent, colourMode):
        self.win = win
        self.database = database
        self.teacher = teacher
        self.parent = parent
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Add Students To New Class')
        self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.win.configure(bg=classes.colours[self.colourMode][0])

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            275,
            75,
            text=f'Add Students to Class',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.studentTreeFrame = Frame(self.win)

        self.studentTreeScroll = Scrollbar(self.studentTreeFrame)
        self.studentTreeScroll.pack(side=RIGHT, fill=Y)

        self.style = t.Style()
        self.style.theme_use('default')
        self.style.configure(
            'Treeview',
            background=classes.colours[self.colourMode][1],
            foreground=classes.colours[self.oppositeColourMode][0],
            rowheight=25,
            fieldbackground=classes.colours[self.colourMode][1]
        )
        self.style.map(
            'Treeview',
            background=[
                (
                    'selected',
                    classes.colours[self.colourMode][2]
                )
            ],
            foreground=[
                (
                    'selected',
                    classes.colours[self.oppositeColourMode][1]
                )
            ]
        )

        self.studentTree = t.Treeview(
            self.studentTreeFrame,
            columns=('username', 'fName', 'lName'),
            yscrollcommand=self.studentTreeScroll.set
        )
        self.studentTree.pack()

        self.studentTreeScroll.config(command=self.studentTree.yview)

        self.studentTree.column(
            '#0',
            width=0,
            stretch=NO
        )
        self.studentTree.column(
            'username',
            width=200,
            minwidth=50,
            anchor=CENTER
        )
        self.studentTree.column(
            'fName',
            width=200,
            minwidth=50,
            anchor=CENTER
        )
        self.studentTree.column(
            'lName',
            width=200,
            minwidth=50,
            anchor=CENTER
        )

        self.studentTree.heading(
            'username',
            text='Username',
            anchor=CENTER
        )
        self.studentTree.heading(
            'fName',
            text='First Name',
            anchor=CENTER
        )
        self.studentTree.heading(
            'lName',
            text='Last Name',
            anchor=CENTER
        )

        self.studentTree.tag_configure(
            'odd',
            background=classes.colours[self.colourMode][1]
        )
        self.studentTree.tag_configure(
            'even',
            background=classes.colours[self.colourMode][0]
        )

        self.getStudentsButton = Button(
            self.win,
            text='Get Students',
            command=self.getStudents,
            font=('Arial', 14),
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][0]
        )
        self.getStudentsButton.place(x=335, y=410)
        students = self.database.getStudents()
        for i in range(len(students)):
            if i % 2 == 0:
                tag = ('even', )
            else:
                tag = ('odd', )
            self.studentTree.insert(
                parent='',
                index='end',
                iid=i,
                values=(
                    students[i][0],
                    students[i][1],
                    students[i][2]
                ),
                tags=tag
            )

        self.studentTreeFrame.place(x=100, y=120)

    def getStudents(self):
        studentIDs = list(self.studentTree.selection())
        if len(studentIDs) != 0:
            self.database.addClass(self.teacher[0])
            classID = self.database.getLatestClassID()
            for studentID in studentIDs:
                studentDetails = self.studentTree.item(studentID)['values']
                self.database.addStudentToClass(classID, studentDetails[0])
                self.studentTree.delete(studentID)
            self.parent.viewClassButton.config(state='normal')
        else:
            messagebox.showerror(
                'Error',
                'No students selected.',
                parent=self._newWindow
            )

    def closeWindow(self):
        self.parent.windowDimensions(800, 600, self)
        self.parent.win.deiconify()
        self._newWindow.destroy()


class viewClasses(classes.window):
    def __init__(self, win, database, teacher, parent, colourMode):
        self.win = win
        self.database = database
        self.teacher = teacher
        self.parent = parent
        self.colourMode = colourMode
        self.oppositeColourMode = classes.oppositeColourMode(colourMode)

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Maths Revision App')
        self.win.protocol('WM_DELETE_WINDOW', self.closeWindow)
        self.win.configure(
            bg=classes.colours[self.colourMode][0]
        )

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            200,
            75,
            text=f'Check Classes',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )

        self.variable = StringVar()
        self.variable.set('Please select a classID')
        # self.classSelector = ttk.Combobox(
        #   self.win,
        #   values=self.database.getClassIDs(teacher[0]),
        #   state='readonly'
        # )
        # self.classSelector.insert(
        #   0,
        #   'Please select a classID')
        # self.classSelector.bind(
        #   '<<ComboboxSelected>>',
        #   self.setStudentTree
        # )

        self.classSelector = OptionMenu(
            self.win,
            self.variable,
            *self.database.getClassIDs(teacher[0]),
            command=self.setStudentTree
        )
        self.classSelector.config(
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][0],
            highlightthickness=0
        )
        self.classSelector.place(x=50, y=110)

        self.studentTreeFrame = Frame(
            self.win,
            bg=classes.colours[self.colourMode][0]
        )
        # self.studentTreeFrame.pack(side=LEFT, padx=50)
        self.studentTreeFrame.place(x=50, y=150, height=236, width=700)

        self.studentTreeYScroll = Scrollbar(self.studentTreeFrame)
        self.studentTreeYScroll.pack(side=RIGHT, fill=Y)

        self.studentTreeXScroll = Scrollbar(
            self.studentTreeFrame,
            orient='horizontal'
        )
        self.studentTreeXScroll.pack(side=BOTTOM, fill=X)

        self.style = t.Style()
        self.style.theme_use('default')
        self.style.configure(
            'Treeview',
            background=classes.colours[self.colourMode][1],
            foreground=classes.colours[self.oppositeColourMode][0],
            rowheight=20,
            fieldbackground=classes.colours[self.colourMode][1]
        )
        self.style.map(
            'Treeview',
            background=[
                (
                    'selected',
                    classes.colours[self.colourMode][2]
                )
            ],
            foreground=[
                (
                    'selected',
                    classes.colours[self.oppositeColourMode][1]
                )
            ]
        )

        self.studentTree = t.Treeview(
            self.studentTreeFrame,
            yscrollcommand=self.studentTreeYScroll.set,
            xscrollcommand=self.studentTreeXScroll.set,
            selectmode=BROWSE
        )

        self.studentTree.column(
            '#0',
            width=680,
            minwidth=50,
            anchor=CENTER
        )

        # self.studentTree.bind(
        #   '<ButtonRelease-1>',
        #   self.updateGraphButton
        # )
        self.studentTree.bind(
            '<<TreeviewSelect>>',
            self.updateGraphButton
        )

        self.studentTreeYScroll.config(
            command=self.studentTree.yview
        )
        self.studentTreeXScroll.config(
            command=self.studentTree.xview
        )

        self.studentTree.pack()

        self.studentTree.tag_configure(
            'odd',
            background=classes.colours[self.colourMode][1]
        )
        self.studentTree.tag_configure(
            'even',
            background=classes.colours[self.colourMode][0]
        )
        self.studentTree.tag_configure(
            'complete',
            background='green'
        )

        self.assignTestButton = Button(
            self.win,
            text='Assign Test',
            command=self.assignTest,
            font=('Arial', 16),
            state='disabled',
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][0]
        )
        self.assignTestButton.place(x=100, y=400)

        self.spinbox = Spinbox(
            self.win,
            font=('Arial', 18),
            width=5,
            from_=10,
            to=30,
            state='disabled'
        )
        self.spinbox.place(x=250, y=405)

        self.graphButton = Button(
            self.win,
            font=('Arial', 16),
            text='Display Graph',
            command=self.graph,
            state='disabled',
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][0]
        )
        self.graphButton.place(x=550, y=400)

    def setStudentTree(self, event):
        for record in self.studentTree.get_children():
            self.studentTree.delete(record)

        students = self.getStudentsInClass()
        columns = []
        for student in students:
            columns.append(student[0])

        self.studentTree['columns'] = columns
        self.studentTree.column(
            '#0',
            width=100,
            minwidth=50,
            anchor=CENTER
        )
        self.studentTree.heading(
            '#0',
            text='Assignment',
            anchor=CENTER
        )

        # print(self.studentTree['columns'])
        for student in students:
            # print(student)
            self.studentTree.column(
                student[0],
                width=200,
                minwidth=50,
                anchor=CENTER
            )
            self.studentTree.heading(
                student[0],
                text=student[3],
                anchor=CENTER
            )

        assignments = self.database.\
            getAssignmentDetails(self.variable.get())
        #print(assignments)

        for i in range(len(assignments) // len(students)):  # this gives the number of total assignments there are.
            values = []
            if i % 2 == 0:
                tag = ('even', )
            else:
                tag = ('odd', )
            #print('new assignment')
            for j in range(len(students)):
                #print(students[j])
                #print(assignments[(i * len(students)) + j])
                if assignments[(i * len(students)) + j][2] == 1:
                    #print('complete')
                    values.append(True)
                else:
                    #print('incomplete')
                    values.append(False)

            complete = True
            for value in values:
                if value == False:
                    complete = False
            if complete:
                tag = ('complete', )
            self.studentTree.insert(
                parent='',
                index='end',
                iid=i,
                text=f'Assignment {i + 1}',
                values=values,
                tags=tag
            )

        self.assignTestButton.config(state='normal')
        self.spinbox.config(state='readonly')

    def assignTest(self):
        test = sqlSetUp.Test(int(self.spinbox.get()), self.database)
        questionSet = test.selectQuestions()

        self.database.addTest(test.getNumberOfQuestions())
        testID = self.database.getLatestTestID()
        test.setTestID(testID)
        test.insertIntoDatabase(questionSet)
        #print(questionSet)

        self.database.addAssignment(
            self.variable.get(),
            testID,
            self.getStudentsInClass()
        )
        integer = len(list(self.studentTree.get_children())) + 1
        if integer % 2 == 0:
            tag = ('odd', )
        else:
            tag = ('even', )

        values = []
        students = self.getStudentsInClass()
        for i in range(len(students)):
            values.append(False)
        self.studentTree.insert(
            parent='',
            index='end',
            iid=integer,
            text=f'Assignment {integer}',
            values=tuple(values),
            tags=tag
        )

        messagebox.showinfo(
            title='Assignment added',
            message=f'Test {testID} added, '
                    f'with {self.spinbox.get()} questions',
            parent=self.win
        )

    def getStudentsInClass(self):
        students = self.database.getStudentsInClass(self.variable.get())
        for i in range(len(students)):
            students[i] = self.database.getUser(students[i])

        students = sqlSetUp.stripRecord(students)
        return students

    def graph(self):
        self.win.withdraw()
        assignmentID = int(list(self.studentTree.selection())[0]) + 1
        openWindow = Toplevel()
        graphs.graph(
            openWindow,
            self.database,
            self.parent,
            assignmentID,
            int(self.variable.get()),
            self.colourMode
        )

    def updateGraphButton(self, event):
        assignmentDone = False
        completeAssignments = self.studentTree.item(
            self.studentTree.selection()
        )['values']
        for complete in completeAssignments:
            if complete == 'True':
                assignmentDone = True
        if assignmentDone:
            self.graphButton.config(state='normal')
        else:
            self.graphButton.config(state='disabled')

    def closeWindow(self):
        self.parent.windowDimensions(800, 600, self)
        self.parent.win.deiconify()
        self._newWindow.destroy()


class adminMathsProgram(classes.window):
    def __init__(self, win, database, user, parent):
        self.win = win
        self.database = database
        self.userLoggedIn = user
        self.parent = parent
        colour, opposite = self.database.getColourMode(
            self.userLoggedIn[0]
        )
        self.colourMode = colour
        self.oppositeColourMode = opposite
        # print(self.colourMode, self.oppositeColourMode)
        # print(classes.colours[self.colourMode],
        #       classes.colours[self.oppositeColourMode])

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Maths Revision App: Admin')
        self.win.protocol(
            'WM_DELETE_WINDOW',
            lambda: self.closeWindow(True)
        )
        # print(classes.colours[colourMode][0])
        self.win.configure(
            bg=classes.colours[self.colourMode][0]
        )

        self.topCanvas = Canvas(
            self.win,
            bg=classes.colours[self.colourMode][1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        self.topCanvas.place(x=0, y=0)
        self.welcomeLabel = self.topCanvas.create_text(
            400,
            75,
            text=f'Welcome, admin',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.oppositeColourMode][1]
        )
        self.resetDatabaseButton = Button(
            self.win,
            text='Reset Database',
            font=('Arial', 18, 'bold'),
            command=self.resetButtonCommand,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.resetDatabaseButton.place(x=300, y=160)
        self.resetDatabaseLabel = Label(
            self.win,
            text='Database has been reset',
            font=('Arial', 18),
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )

        self.toggleColoursButton = Button(
            self.win,
            text='Dark Mode',
            command=self.toggleColours,
            bg=classes.colours[self.colourMode][1],
            fg=classes.colours[self.oppositeColourMode][1]
        )
        self.toggleColoursButton.place(x=720, y=110)

        self.widgets = [
            self.resetDatabaseButton,
            self.toggleColoursButton
        ]

        self.sideMenu = classes.sideMenu(
            self.win,
            self.closeWindow,
            '',
            '',
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

    def resetButtonCommand(self):
        self.database.resetTables()
        self.resetDatabaseButton.config(state='disabled')
        self.resetDatabaseLabel.place(x=265, y=220)

    def toggleColours(self):
        self.topCanvas.itemconfig(
            self.welcomeLabel,
            fill=classes.colours[self.colourMode][1]
        )
        for widget in self.widgets:
            widget.config(fg=classes.colours[self.colourMode][1])
        self.resetDatabaseLabel.config(
            fg=classes.colours[self.colourMode][1]
        )
        if self.colourMode == 'light':
            self.colourMode = 'dark'
            self.oppositeColourMode = 'light'
        else:
            self.colourMode = 'light'
            self.oppositeColourMode = 'dark'

        self.topCanvas.config(bg=classes.colours[self.colourMode][1])
        for widget in self.widgets:
            widget.config(bg=classes.colours[self.colourMode][1])
        self.win.configure(bg=classes.colours[self.colourMode][0])
        self.resetDatabaseLabel.config(
            bg=classes.colours[self.colourMode][0]
        )
        self.database.updateColourMode(
            self.userLoggedIn[0],
            self.colourMode
        )
        self.sideMenu.changeColours(
            classes.colours[self.colourMode],
            classes.colours[self.oppositeColourMode]
        )

    def closeWindow(self, enable):
        if enable:
            app.windowDimensions(800, 600, self)
            app.win.deiconify()
        self._newWindow.destroy()


if __name__ == '__main__':
    root = Tk()
    app = main(root)
    root.mainloop()
