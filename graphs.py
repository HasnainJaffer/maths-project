from tkinter import *
import classes
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
matplotlib.use('TkAgg')


class graph(classes.window):
    def __init__(self, win, database, parent, assignmentID, classID, colourMode):
        self.win = win
        self.database = database
        self.parent = parent
        self.assignmentID = assignmentID
        self.classID = classID
        self.colourMode = colourMode
        self.opposite = classes.oppositeColourMode(colourMode)

        classes.window.__init__(self, self.win)
        self.windowDimensions(800, 600, self.parent)
        self.win.title('Maths Revision App')
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
            text='Data Graph',
            font=('Arial', 30, 'bold'),
            fill=classes.colours[self.opposite][1]
        )

        # plot a graph of number of correct answers against question num
        # print(classID)

        scores, numberOfAttempts = self.database.getScores(self.classID, self.assignmentID)
        sortedScores = []
        # print(scores)

        for i in range(len(scores[0])):
            temp = []
            for j in range(numberOfAttempts):
                temp.append(scores[j][i])
            sortedScores.append(temp)

        xValues = []
        yValues = []

        questionNumber = 1

        for question in sortedScores:
            xValues.append(questionNumber)
            total = 0
            for answers in question:
                total += answers[1]
            yValues.append(total)
            questionNumber += 1

        frame = Frame(self.win)
        frame.place(x=0, y=100)

        line, axis = plt.subplots()
        axis.bar(xValues, yValues)
        line.set_facecolor(
            classes.colours[self.colourMode][0]
        )
        axis.set_facecolor(
            classes.colours[self.colourMode][0]
        )
        axis.spines['left'].set_color(
            classes.colours[self.opposite][0]
        )
        axis.spines['bottom'].set_color(
            classes.colours[self.opposite][0]
        )
        axis.spines['right'].set_color(
            classes.colours[self.colourMode][0]
        )
        axis.spines['top'].set_color(
            classes.colours[self.colourMode][0]
        )

        axis.tick_params(
            axis='x',
            colors=classes.colours[self.opposite][0]
        )
        axis.tick_params(
            axis='y',
            colors=classes.colours[self.opposite][0]
        )
        axis.set_xticks(ticks=xValues)
        axis.set_yticks(ticks=np.arange(0, max(yValues) + 1, 1))

        plt.xlabel(
            'Question Number',
            color=classes.colours[self.opposite][0]
        )
        plt.ylabel(
            'Number of Correct Answers',
            color=classes.colours[self.opposite][0]
        )
        plt.title(
            'Number of people that got each question correct',
            color=classes.colours[self.opposite][0]
        )

        canvas = FigureCanvasTkAgg(line, frame)
        canvas.get_tk_widget().pack()
        canvas.get_tk_widget().config(
            bg=classes.colours[self.colourMode][0]
        )

    def closeWindow(self):
        self.parent.win.deiconify()
        self._newWindow.destroy()
