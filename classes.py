from tkinter import *
from PIL import Image, ImageTk


def oppositeColourMode(colourMode):
    if colourMode == 'light':
        oppositeColourMode = 'dark'
    else:
        oppositeColourMode = 'light'
    return oppositeColourMode


colours = {
    'light': ['#FAF7F0',
              '#CDFCF6',
              '#BCCEF8',
              '#98A8F8'],

    'dark':  ['#000000',
              '#150050',
              '#3F0071',
              '#610094']
}


class window:
    def __init__(self, newWindow):
        self._newWindow = newWindow
        self._newWindow.resizable(0, 0)
        self.__screenwidth = self._newWindow.winfo_screenwidth()
        self.__screenheight = self._newWindow.winfo_screenheight()
        self.label1 = Label(newWindow)
        self.label2 = Label(newWindow)
        self.button1 = Button(newWindow)
        self.button2 = Button(newWindow)

    def windowDimensions(self, width, height, parent):
        if not parent:
            x = (self.__screenwidth - width) / 2
            y = (self.__screenheight - height) / 2
        else:
            x = parent.win.winfo_x()
            y = parent.win.winfo_y()
        self._newWindow.geometry(
            '%dx%d+%d+%d' % (
                width,
                height,
                x,
                y
            )
        )


class entrybox:
    def __init__(self, win, text, show, colour, opposite):
        self.__win = win
        self._text = text
        self.__show = show
        self.__colour = colour
        self.__opposite = opposite
        self.entryBox = Entry(
            self.__win,
            text='',
            width=25,
            borderwidth=3,
            font=('Arial', 14),
            fg='dark grey',
            bg=self.__opposite
        )
        self.entryBox.bind('<FocusIn>', self._delTempText)
        self.entryBox.insert(0, f'Enter {self._text}')
        self.entryBox.bind('<FocusOut>', self._insTempText)

    def _delTempText(self, event):
        if self.entryBox.get() == f'Enter {self._text}':
            self.entryBox.delete(0, 'end')
            self.entryBox.config(
                fg=self.__colour,
                highlightbackground='white',
                highlightthickness=0,
                highlightcolor='white'
            )
            if self.__show == 0:
                self.entryBox.config(show='•')

    def _insTempText(self, event):
        if self.entryBox.get() == '':
            self.entryBox.insert(0, f'Enter {self._text}')
            self.entryBox.config(
                fg='dark grey',
                highlightbackground='white',
                highlightthickness=0,
                highlightcolor='white'
            )
            if self.__show == 0:
                self.entryBox.config(show='')

    def getText(self):
        return self._text


class sideMenu:
    def __init__(self, root, command1, command2,
                 command3, colour, opposite):
        self.__root = root
        self.__command1 = command1
        self.__command2 = command2
        self.__command3 = command3
        self.__colour = colour
        self.__opposite = opposite
        self.__buttonY = 0
        self.__buttons = []
        self.__frame = Frame(
            self.__root,
            bg=self.__colour[2],
            width=50,
            height=50
        )
        self.__frame.place(x=15, y=15)
        self.__frame.bind('<Enter>', lambda e: self.expand())
        self.__frame.bind('<Leave>', lambda e: self.contract())
        self._minWidth = 50
        self._maxWidth = 200
        self._minHeight = 50
        self._maxHeight = 800
        self._minPos = 15
        self._maxPos = 0
        self._currentPos = self._minPos
        self._currentHeight = self._minHeight
        self._currentWidth = self._minWidth
        self._expanded = False

        self.backArrow = ImageTk.PhotoImage(
            Image.open('backArrow.png').resize((43, 43))
        )
        self.settings = ImageTk.PhotoImage(
            Image.open('settings.png').resize((43, 43))
        )
        self.signOut = ImageTk.PhotoImage(
            Image.open('signOut.png').resize((43, 43))
        )

        self.backButton = Button(
            self.__frame,
            image=self.backArrow,
            bg=self.__colour[2],
            fg=self.__opposite[1],
            relief='flat',
            command=self.__command1
        )
        self.backButton.place(x=0, y=self.__buttonY)
        self.__buttonY += 90
        self.__buttons.append([self.backButton, 'Back'])

        if self.__command2 != '':
            self.settingsButton = Button(
                self.__frame,
                image=self.settings,
                bg=self.__colour[2],
                fg=self.__opposite[1],
                relief='flat',
                command=self.__command2
            )
            self.settingsButton.place(x=0, y=self.__buttonY)
            self.__buttonY += 90
            self.__buttons.append([self.settingsButton, 'Settings'])

        if self.__command3 != '':
            self.signOutButton = Button(
                self.__frame,
                image=self.signOut,
                bg=self.__colour[2],
                fg=self.__opposite[1],
                relief='flat',
                command=self.__command3
            )
            self.signOutButton.place(x=0, y=self.__buttonY)
            self.__buttons.append([self.signOutButton, 'Sign Out'])

        self.__frame.grid_propagate(False)

    def expand(self):
        self._currentWidth += 10
        self._currentHeight += 50
        self._currentPos -= 1
        rep = self.__root.after(10, self.expand)
        self.__frame.config(
            width=self._currentWidth,
            height=self._currentHeight
        )
        self.__frame.place(x=self._currentPos, y=self._currentPos)
        if self._currentWidth >= self._maxWidth and \
                self._currentHeight >= self._maxHeight:
            self._expanded = True
            self.__root.after_cancel(rep)
            self.fill()

    def contract(self):
        self._currentWidth -= 10
        self._currentHeight -= 50
        self._currentPos += 1
        rep = self.__root.after(5, self.contract)
        self.__frame.config(
            width=self._currentWidth,
            height=self._currentHeight
        )
        self.__frame.place(x=self._currentPos, y=self._currentPos)
        if self._currentWidth <= self._minWidth and \
                self._currentHeight <= self._minHeight:
            self._expanded = False
            self.__root.after_cancel(rep)
            self.fill()

    def fill(self):
        if self._expanded:
            for button in self.__buttons:
                button[0].config(
                    text=button[1],
                    compound=LEFT,
                    font=('Arial', 20)
                )
        else:
            for button in self.__buttons:
                button[0].config(text='')

    def changeColours(self, colour, opposite):
        self.__frame.config(bg=colour[2])
        try:
            self.backButton.config(
                bg=colour[2],
                fg=opposite[1]
            )
            self.settingsButton.config(
                bg=colour[2],
                fg=opposite[1]
            )
            self.signOutButton.config(
                bg=colour[2],
                fg=opposite[1]
            )
        except:
            pass


class eyeButton:
    def __init__(self, win):
        self.__win = win
        self.__eye = ImageTk.PhotoImage(
            Image.open('eye.png').resize((20, 20))
        )
        self.eyeButton = Button(
            self.__win,
            image=self.__eye
        )

    def setDown(self, fn):
        self.eyeButton.bind('<Button-1>', fn)

    def setUp(self, fn):
        self.eyeButton.bind('<ButtonRelease-1>', fn)


class questionFrame(Frame):
    def __init__(self, parent, controller, question,
                 questionSet, lastQuestion, colour, opposite):
        self.questionNum = question
        self.questionSet = questionSet
        self.questionDetails = self.questionSet[self.questionNum - 1].getData()
        self.lastQuestion = lastQuestion
        self.colour = colour
        self.opposite = opposite

        Frame.__init__(self, parent, bg=self.colour[0])
        canvas = Canvas(
            self,
            bg=self.colour[1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        canvas.place(x=0, y=0)
        self.headerLabel = canvas.create_text(
            200,
            75,
            text=f'Question {self.questionNum}',
            font=('Arial', 30, 'bold'),
            fill=self.opposite[1]
        )

        self.answerInput = StringVar(self, 'None')

        self.questionLabel = Label(
            self,
            text=self.questionDetails[1],
            font=('Arial', 18),
            bg=self.colour[0],
            fg=self.opposite[1]
        )
        self.questionLabel.place(x=100, y=120)
        self.radio1 = Radiobutton(
            self,
            text=self.questionDetails[2][0],
            value=self.questionDetails[2][0],
            font=('Arial', 18),
            variable=self.answerInput,
            bg=self.colour[0],
            fg=self.opposite[1],
            selectcolor=self.colour[0]
        )
        self.radio1.place(x=100, y=180)
        self.radio2 = Radiobutton(
            self,
            text=self.questionDetails[2][1],
            value=self.questionDetails[2][1],
            font=('Arial', 18),
            variable=self.answerInput,
            bg=self.colour[0],
            fg=self.opposite[1],
            selectcolor=self.colour[0]
        )
        self.radio2.place(x=100, y=240)
        self.radio3 = Radiobutton(
            self,
            text=self.questionDetails[2][2],
            value=self.questionDetails[2][2],
            font=('Arial', 18),
            variable=self.answerInput,
            bg=self.colour[0],
            fg=self.opposite[1],
            selectcolor=self.colour[0]
        )
        self.radio3.place(x=100, y=300)
        self.radiobuttons = [
            self.radio1,
            self.radio2,
            self.radio3
        ]

        self.button1 = Button(
            self,
            text='Previous question',
            font=('Arial', 20, 'bold'),
            width=15,
            command=lambda: controller.showFrame(self.questionNum - 2),
            bg=self.colour[1],
            fg=self.opposite[1]
        )
        self.button2 = Button(
            self,
            text='Next question',
            font=('Arial', 20, 'bold'),
            width=15,
            command=lambda: controller.showFrame(self.questionNum),
            bg=self.colour[1],
            fg=self.opposite[1]
        )
        self.button1.place(x=40, y=500)
        self.button2.place(x=520, y=500)

        if self.questionNum == self.lastQuestion:
            self.button2.config(
                text='Review answers',
                command=controller.finalButtonCommand
            )

    def getAnswer(self):
        answer = self.questionDetails[2][int(self.questionDetails[3])]
        if self.answerInput.get() == answer:
            return True
        elif self.answerInput.get() == 'None':
            return None
        else:
            return False

    def getQuestionNumber(self):
        return self.questionNum

    def getQuestionID(self):
        return self.questionDetails[0]

    def disableButton(self, button):
        if button == 'previous':
            self.button1.config(
                state='disabled',
                font=('Arial', 20, 'normal')
            )
        elif button == 'next':
            self.button2.config(
                state='disabled',
                font=('Arial', 20, 'normal')
            )


class endFrame(Frame):
    def __init__(self, parent, controller,
                 questions, colour, opposite):
        self.parent = parent
        self.controller = controller
        self.questions = questions
        self.colour = colour
        self.opposite = opposite
        Frame.__init__(
            self,
            self.parent,
            bg=self.colour[0]
        )
        canvas = Canvas(
            self,
            bg=self.colour[1],
            width=800,
            height=100,
            borderwidth=0,
            highlightthickness=0
        )
        canvas.place(x=0, y=0)
        self.headerLabel = canvas.create_text(
            400,
            75,
            text='Review Answers',
            font=('Arial', 30, 'bold'),
            fill=self.opposite[1]
        )

        self.container = Frame(self, bg=self.colour[0])
        self.container.place(x=180, y=150)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.questionButtons = []
        row = 0
        column = 0
        for i in range(len(questions)):
            self.questionButtons.append('')
            self.questionButtons[i] = Button(
                self.container,
                text=(
                    'Question',
                    str(i + 1)
                )
            )
            self.configButton(i)
            if i % 5 == 0:
                row += 1
                column = 0
            else:
                column += 1
            self.questionButtons[i].grid(
                row=row,
                column=column,
                padx=10,
                pady=10
            )

        self.submitButton = Button(
            self.container,
            text='Submit',
            font=('Arial', 18, 'bold'),
            bg=self.colour[1],
            fg=self.opposite[1]
        )
        self.submitButton.grid(row=row + 1, column=2, pady=50)

    def configButton(self, index):
        self.questionButtons[index].config(
            command=lambda: self.controller.showFrame(index)
        )
