from tkinter import *
import tkinter.ttk as ttk

class window:
    def __init__(self, newWindow):
        newWindow.resizable(0, 0)
        newWindow.protocol("WM_DELETE_WINDOW", self.closeWindow)
        self.newWindow = newWindow
        self.screenwidth = self.newWindow.winfo_screenwidth()
        self.screenheight = self.newWindow.winfo_screenheight()
        self.label1 = Label(newWindow)
        self.label2 = Label(newWindow)
        self.button1 = ttk.Button(newWindow)
        self.button2 = ttk.Button(newWindow)

    def closeWindow(self):
        self.newWindow.destroy()

    def enableWindows(self):
        self.newWindow.attributes("-disabled", False)

    def windowDimensions(self, width, height):
        x = (self.screenwidth - width) / 2
        y = (self.screenheight - height) / 2
        self.newWindow.geometry('%dx%d+%d+%d' % (width, height, x, y))


class questionFrame(Frame):
    def __init__(self, parent, controller, question, questionSet):
        self.questionNum = question
        self.questionIndex = question - 1
        self.questionSet = questionSet
        self.questionDetails = self.questionSet[self.questionIndex]
        #print(self.questionDetails)
        Frame.__init__(self, parent)
        canvas = Canvas(self, bg="light grey", width=800, height=100)
        canvas.place(x=0, y=0)
        label = Label(self, text=f"Question {self.questionNum}", font=("Arial", 18), bg="light grey")
        label.pack(pady=10, padx=10)

        self.button1 = Button(self, text="Next question", font=("Arial", 20),
                              command=lambda: controller.showFrame(self.questionIndex + 1))
        self.button1.place(x=580, y=500)

        self.button2 = Button(self, text="Previous question", font=("Arial", 20),
                              command=lambda: controller.showFrame(self.questionIndex - 1))
        self.button2.place(x=40, y=500)

    def getQuestionNumber(self):
        return self.questionNum

    def disableButton(self, button):
        if button == "next":
            self.button1.config(state="disabled")
        elif button == "previous":
            self.button2.config(state="disabled")


class testScreen(window):
    def __init__(self, win, questions):
        self.win = win
        self.questionSet = questions

        window.__init__(self, self.win)
        self.windowDimensions(800, 600)

        container = Frame(self.win)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = []
        self.questionNum = 0
        for question in self.questionSet:
            self.questionNum += 1
            frame = questionFrame(container, self, self.questionNum, self.questionSet)
            self.frames.append(frame)
            frame.grid(row=0, column=0, sticky="nsew")
        self.showFrame(0)

    def showFrame(self, index):
        frame = self.frames[index]
        if index == 0:
            frame.disableButton("previous")
        elif index == len(self.frames) - 1:
            frame.disableButton("next")
        frame.tkraise()


questions = [
    ["4 × 3 ÷ 2 × 3",
     "18", "2", "12", 1, "Arithmetic"],

    ["Write 8 × 10^2 as an ordinary number",
     "80.0", "8000", "800", 3, "Standard Form"],

    ["Write 7.35 × 10^-1 as an ordinary number",
     "73.5", "0.0735", "0.735", 3, "Standard Form"],

    ["Write 4.36 × 10^4 as an ordinary number",
     "43600", "4360", "43.60", 2, "Standard Form"],

    ["Write 5 × 10^5 as an ordinary number",
     "500000", "5000", "500", 1, "Standard Form"],

    ["Write 1 × 10^-4 as an ordinary number",
     "100", "0.01", "0.0001", 3, "Standard Form"],

    ["Write 1.64 × 10^2 as an ordinary number",
     "0.0164", "164", "16.4", 2, "Standard Form"],

    ["Write 6.345 × 10^6 as an ordinary number",
     "634500", "6345000", "0.06345", 2, "Standard Form"]
]

if __name__ == '__main__':
    root = Tk()
    app = testScreen(root, questions)
    root.mainloop()
