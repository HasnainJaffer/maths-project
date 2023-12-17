import sqlite3
from random import randint
import hashing


def stripRecord(record):
    for item in range(len(record)):
        record[item] = [
            record[item][0],
            record[item][2],
            record[item][3],
            record[item][4]
        ]
    return record


class Database:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()

    def createTables(self):
        self.c.executescript(
            '''CREATE TABLE IF NOT EXISTS roles
            ([roleID]           INTEGER         PRIMARY KEY AUTOINCREMENT,
            [description]       VARCHAR(16)     NOT NULL);
            
            CREATE TABLE IF NOT EXISTS users
            ([userID]           INTEGER         PRIMARY KEY AUTOINCREMENT,
            [username]          VARCHAR(16)     UNIQUE NOT NULL,
            [password]          VARCHAR(128)    NOT NULL,
            [title]             VARCHAR(4),
            [firstName]         VARCHAR(20),
            [lastName]          VARCHAR(20),
            [email]             VARCHAR(50),
            [roleID]            INTEGER         NOT NULL,
            FOREIGN KEY (roleID) REFERENCES      roles(roleID));
            
            CREATE TABLE IF NOT EXISTS questions
            ([questionID]       INTEGER         PRIMARY KEY AUTOINCREMENT,
            [question]          VARCHAR(128)    NOT NULL,
            [choice1]           VARCHAR(32)     NOT NULL,
            [choice2]           VARCHAR(32)     NOT NULL,
            [choice3]           VARCHAR(32)     NOT NULL,
            [answer]            INTEGER         NOT NULL,
            [topic]             VARCHAR(16)     NOT NULL);
            
            CREATE TABLE IF NOT EXISTS tests
            ([testID]           INTEGER         PRIMARY KEY AUTOINCREMENT,
            [NOQuestions]       INTEGER         NOT NULL);
            
            CREATE TABLE IF NOT EXISTS studentPractice
            ([userPracticeID]   INTEGER         PRIMARY KEY AUTOINCREMENT,
            [userID]            INTEGER         NOT NULL,
            [testID]            INTEGER         NOT NULL,
            FOREIGN KEY(userID) REFERENCES      users(userID),
            FOREIGN KEY(testID) REFERENCES      tests(testID));
            
            CREATE TABLE IF NOT EXISTS userAnswer
            ([userPracticeID]   INTEGER         NOT NULL,
            [questionID]        INTEGER         NOT NULL,
            [correct]           BOOLEAN         NOT NULL,
            FOREIGN KEY(userPracticeID) REFERENCES      studentPractice(userPracticeID),
            FOREIGN KEY(questionID)     REFERENCES      questions(questionID));
            
            CREATE TABLE IF NOT EXISTS studentPerformance
            ([userPracticeID]   INTEGER         NOT NULL,
            [attemptNumber]     INTEGER         NOT NULL,
            [score]             INTEGER         NOT NULL,
            FOREIGN KEY(userPracticeID) REFERENCES      studentPractice(userPracticeID));
            
            CREATE TABLE IF NOT EXISTS testDetails
            ([testID]           INTEGER         NOT NULL,
            [questionID]        INTEGER         NOT NULL,
            FOREIGN KEY(testID)     REFERENCES      studentPractice(testID),
            FOREIGN KEY(questionID) REFERENCES      questions(questionID));
            
            CREATE TABLE IF NOT EXISTS classes
            ([classID]          INTEGER         PRIMARY KEY AUTOINCREMENT,
            [userID]            VARCHAR(16)     NOT NULL,
            FOREIGN KEY(userID) REFERENCES      users(userID));
            
            CREATE TABLE IF NOT EXISTS classComposition
            ([classID]          INTEGER         NOT NULL,
            [userID]            VARCHAR(16)     NOT NULL,
            FOREIGN KEY(userID)  REFERENCES      users(userID),
            FOREIGN KEY(classID) REFERENCES      classes(classID));
            
            CREATE TABLE IF NOT EXISTS setAssignments
            ([assignmentID]     INTEGER         PRIMARY KEY AUTOINCREMENT,
            [classID]           INTEGER         NOT NULL,
            [testID]            INTEGER         NOT NULL,
            FOREIGN KEY(classID) REFERENCES      classes(classID),
            FOREIGN KEY(testID)  REFERENCES      tests(testID));
            
            CREATE TABLE IF NOT EXISTS completeAssignments
            ([userID]           INTEGER         NOT NULL,
            [assignmentID]      INTEGER         NOT NULL,
            [complete]          BOOLEAN         NOT NULL,
            FOREIGN KEY(userID)       REFERENCES      users(userID),
            FOREIGN KEY(assignmentID) REFERENCES      setAssignments(assignmentID));
            
            CREATE TABLE IF NOT EXISTS settings
            ([userID]           INTEGER         NOT NULL,
            [darkMode]          BOOLEAN         DEFAULT 0 NOT NULL,
            FOREIGN KEY(userID) REFERENCES      users(userID));
            '''
        )

    def insertValues(self):
        # insert values for roles
        self.c.execute(
            '''INSERT INTO roles (description)
            VALUES ('student'),
                   ('teacher'),
                   ('admin')
            '''
        )

        # insert values for users
        self.c.executemany(
            '''INSERT INTO users 
            (username, password, title, 
            firstName, lastName, email, roleID)
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            users
        )

        for user in users:
            userID = self.getUser(user[0])[0]
            self.c.execute(
                '''INSERT INTO settings(userID)
                VALUES (?)''',
                (userID, )
            )

        # insert values for questions
        self.c.executemany(
            '''INSERT INTO questions 
            (question, choice1, choice2, 
            choice3, answer, topic)
            VALUES (?, ?, ?, ?, ?, ?)''',
            questions
        )
        self.conn.commit()

    def resetTables(self):
        self.c.executescript(
            '''DROP TABLE IF EXISTS roles;
            DROP TABLE IF EXISTS users;
            DROP TABLE IF EXISTS questions;
            DROP TABLE IF EXISTS tests;
            DROP TABLE IF EXISTS studentPractice;
            DROP TABLE IF EXISTS userAnswer;
            DROP TABLE IF EXISTS studentPerformance;
            DROP TABLE IF EXISTS testsDetails;
            DROP TABLE IF EXISTS classes;
            DROP TABLE IF EXISTS classComposition;
            DROP TABLE IF EXISTS setAssignments;
            DROP TABLE IF EXISTS completeAssignments;'''
        )
        self.createTables()
        self.insertValues()

    def addUser(self, username, password, title,
                firstname, lastname, email, roleID):
        self.c.execute(
            '''INSERT INTO users 
            (username, password, title, 
            firstName, lastName, email, roleID) 
            VALUES (?, ?, ?, ?, ?, ?, ?)''',
            (username, password, title, firstname,
             lastname, email, roleID)
        )
        userID = self.getUser(username)[0]
        self.c.execute(
            '''INSERT INTO settings (userID)
            VALUES (?)''',
            (userID, )
        )
        self.conn.commit()

    def addTest(self, numberOfQuestions):
        self.c.execute(
            '''INSERT INTO tests 
            (NOQuestions) 
            VALUES (?)''',
            (numberOfQuestions, )
        )
        self.conn.commit()

    def addAnswers(self, answers, testID, user):
        self.c.execute(
            '''INSERT INTO studentPractice 
            (userID, testID)
            VALUES (?, ?)''',
            (user[0], testID)
        )
        userPracID = self.getUserPracticeID(user[0], testID)
        for i in answers:
            self.c.execute(
                '''INSERT INTO userAnswer 
                (userPracticeID, questionID, correct)
                VALUES (?, ?, ?)''',
                (userPracID, i[0], i[1])
            )
        self.conn.commit()

    # userPracticeID, attempt, score addition to studentPerformance table
    def addStudentPerformance(self, user, testID, score):
        self.c.execute(
            '''SELECT COUNT(*)
            FROM studentPractice
            WHERE testID = ?''',
            (testID, )
        )
        results = self.c.fetchall()
        # print("count(*) from studentPrac:", results)
        attemptNum = int(str(results[0])[1:-2])

        userPracticeID = self.getUserPracticeID(user[0], testID)
        self.c.execute(
            '''INSERT INTO studentPerformance 
            (userPracticeID, attemptNumber, score)
            VALUES (?, ?, ?)''',
            (userPracticeID, attemptNum, score)
        )
        self.conn.commit()

    def addClass(self, userID):
        self.c.execute(
            '''INSERT INTO classes (userID)
            VALUES (?)''',
            (userID, )
        )
        self.conn.commit()

    def addStudentToClass(self, classID, userID):
        self.c.execute(
            '''INSERT INTO classComposition (classID, userID)
            VALUES (?, ?)''',
            (classID, userID)
        )
        self.conn.commit()

    def addAssignment(self, classID, testID, students):
        self.c.execute(
            '''INSERT INTO setAssignments(classID, testID)
            VALUES (?, ?)''',
            (classID, testID)
        )
        assignmentID = self.getLatestAssignmentID()
        for student in students:
            self.updateCompleteAssignmentsTable(
                student,
                assignmentID
            )

        self.conn.commit()

    def getLatestAssignmentID(self):
        self.c.execute(
            '''SELECT assignmentID
            FROM setAssignments
            ORDER BY assignmentID DESC'''
        )
        assignmentID = self.c.fetchall()
        assignmentID = int(str(assignmentID[0])[1:-2])
        return assignmentID

    def updateCompleteAssignmentsTable(self, student, assignmentID):
        self.c.execute(
            '''INSERT INTO completeAssignments
            (userID, assignmentID, complete)
            VALUES (?,?,?)''',
            (student[0], assignmentID, 0)
        )
        self.conn.commit()

    def setCompleteAssignmentsTrue(self, testID, userID):
        self.c.execute(
            '''SELECT assignmentID
            FROM setAssignments
            WHERE testID = ?''',
            (testID, )
        )
        assignmentID = list(self.c.fetchall()[0])[0]
        self.c.execute(
            '''UPDATE completeAssignments
            SET complete = 1
            WHERE assignmentID = ?
            AND userID = ?''',
            (assignmentID, userID)
        )
        self.conn.commit()

    def updateColourMode(self, userID, newMode):
        if newMode == 'light':
            newMode = 0
        else:
            newMode = 1
        self.c.execute(
            '''UPDATE settings
            SET darkMode = ?
            WHERE userID = ?''',
            (newMode, userID)
        )
        self.conn.commit()

    def getAssignmentDetails(self, classID):
        self.c.execute(
            '''SELECT completeAssignments.assignmentID, userID, complete
            FROM completeAssignments LEFT JOIN setAssignments 
            ON setAssignments.assignmentID = completeAssignments.assignmentID
            WHERE classID = ?''',
            (classID, )
        )
        data = self.c.fetchall()
        for i in range(len(data)):
            data[i] = list(data[i])
        return data

    def getStudentAssignments(self, userID):
        self.c.execute(
            '''SELECT completeAssignments.assignmentID, classID, complete
            FROM completeAssignments LEFT JOIN setAssignments
            ON setAssignments.assignmentID = completeAssignments.assignmentID
            WHERE userID = ?''',
            (userID, )
        )
        data = self.c.fetchall()
        for i in range(len(data)):
            data[i] = list(data[i])
        return data

    def getStudents(self):
        self.c.execute(
            '''SELECT username, firstName, lastName
            FROM users
            WHERE roleID = 1'''
        )
        result = self.c.fetchall()
        for i in range(len(result)):
            result[i] = list(result[i])
        return result

    def getLatestTestID(self):
        self.c.execute(
            '''SELECT testID
            FROM tests
            ORDER BY testID DESC'''
        )
        data = self.c.fetchall()
        return int(str(data[0])[1:-2])

    def getLatestClassID(self):
        self.c.execute(
            '''SELECT classID
            FROM classes
            ORDER BY classID DESC'''
        )
        data = self.c.fetchall()
        return int(str(data[0])[1:-2])

    def getUserPracticeID(self, userID, testID):
        self.c.execute(
            '''SELECT userPracticeID
            FROM studentPractice
            WHERE userID = ?
            AND testID = ?''',
            (userID, testID)
        )
        data = self.c.fetchall()
        # print("getUserPractice:", data)
        return int(str(data[len(data) - 1])[1:-2])

    def getNumberOfQuestions(self):
        self.c.execute(
            '''SELECT COUNT(*) 
            FROM questions'''
        )
        num = self.c.fetchall()
        return int(str(num[0])[1:-2])

    def getUser(self, username):
        global record
        self.c.execute(
            '''SELECT * 
            FROM users 
            WHERE username = ?''',
            (username, )
        )
        rawRecord = self.c.fetchall()
        if rawRecord:
            record = list(rawRecord[0])
        else:
            print('user doesnt exist')
        return record

    def getQuestion(self, ID):
        index = [0, 1, 3, 5, 7, 8, 9]
        self.c.execute(
            '''SELECT * 
            FROM questions 
            WHERE questionID = ?''',
            (ID, )
        )
        rawQuestion = self.c.fetchall()
        rawQuestion = str(rawQuestion)
        rawQuestion = rawQuestion.split("'")
        questionRecord = ['', '', '', '', '', '', '']
        for x in index:
            questionRecord[index.index(x)] = rawQuestion[x]
        questionRecord[0] = questionRecord[0][2:-2]
        questionRecord[5] = questionRecord[5][2:-2]
        return questionRecord

    def getTreeViewData(self, userID):
        self.c.execute(
            '''SELECT userPracticeID
            FROM studentPractice
            WHERE userID = ?''',
            (userID, )
        )
        tests = self.c.fetchall()
        # print(tests)
        # this gets all the userPracticeIDs of the tests the user has done

        for item in tests:
            tests[tests.index(item)] = int(str(item)[1:-2])
        # print(tests)
        # the test array has all the right userPracticeIDs as integers not tuples

        testPos = 0
        for userPracticeID in tests:
            self.c.execute(
                '''SELECT questionID, correct
                FROM userAnswer
                WHERE userPracticeID = ?''',
                (userPracticeID,)
            )
            questionAnswer = self.c.fetchall()
            # this gets the questions and answers for a specific test

            score = 0
            for questionAnswerItem in questionAnswer:
                tempArray = str(questionAnswerItem).split(',')
                for item in tempArray:
                    if tempArray.index(item) == 0:
                        tempArray[0] = int(str(tempArray[0])[1:])
                    elif tempArray.index(item) == 1:
                        tempArray[1] = int(str(tempArray[1])[:-1])
                # print(tempArray)

                if tempArray[1]:
                    score += 1
                questionAnswer[questionAnswer.index(questionAnswerItem)] = tempArray
            # this for loop sets changes every tuple into an array and places it back into the questionAnswer array
            attemptNum = self.getAttemptNumber(userPracticeID)

            self.c.execute(
                '''SELECT testID
                FROM studentPractice
                WHERE userPracticeID = ?''',
                (userPracticeID, )
            )
            testID = int(str(self.c.fetchone())[1:-2])
            tests[testPos] = [
                tests[testPos],
                score,
                attemptNum,
                questionAnswer,
                testID
            ]
            testPos += 1
        # print(tests)
        return tests
        # each item in the tests array is a different test
        # index 0: userPracticeID
        # index 1: score
        # index 2: attemptNumber
        # index 3: questionsArray
        # index 4: testID

    def getAttemptNumber(self, userPracticeID):
        self.c.execute(
            '''SELECT attemptNumber
            FROM studentPerformance
            WHERE userPracticeID = ?''',
            (userPracticeID, )
        )
        result = self.c.fetchone()
        result = int(str(result)[1:-2])
        return result

    def getClassIDs(self, userID):
        self.c.execute(
            '''SELECT classID
            FROM classes
            WHERE userID = ?''',
            (userID, )
        )
        data = self.c.fetchall()
        for i in range(len(data)):
            data[i] = str(list(data[i])[0])
        return data

    def getScores(self, classID, assignmentID):
        scores = []
        self.c.execute(
            '''SELECT userPracticeID
            FROM setAssignments LEFT JOIN studentPractice
            ON studentPractice.testID = setAssignments.testID
            WHERE classID = ?''',
            (classID, )
        )
        userPracticeIDs = self.c.fetchall()
        for i in range(len(userPracticeIDs)):
            userPracticeIDs[i] = list(userPracticeIDs[i])[0]
        # print(f'userpracticeIDs: {userPracticeIDs}')
        numberOfAttempts = 0
        for attempt in userPracticeIDs:
            if attempt:
                numberOfAttempts += 1
        for userPracticeID in userPracticeIDs:
            self.c.execute(
                '''SELECT questionID, correct
                FROM userAnswer
                WHERE userPracticeID = ?''',
                (userPracticeID, )
            )
            answers = self.c.fetchall()
            for i in range(len(answers)):
                answers[i] = list(answers[i])

            scores.append(answers)
        return scores, numberOfAttempts



    def getStudentsInClass(self, classID):
        self.c.execute(
            '''SELECT userID
            FROM classComposition
            WHERE classID = ?''',
            (classID, )
        )
        data = self.c.fetchall()
        for i in range(len(data)):
            data[i] = list(data[i])[0]
        return data

    def getRetakeTest(self, userPracticeID):
        # this method needs to return all the questions from the given userPracticeID
        self.c.execute(
            ''' SELECT testID
            FROM studentPractice
            WHERE userPracticeID = ?''',
            (userPracticeID, )
        )
        testID = int(str(self.c.fetchone())[1:-2])
        # print(testID)
        self.c.execute(
            '''SELECT questionID
            FROM tests LEFT JOIN testDetails
            ON tests.testID = testDetails.testID
            WHERE tests.testID = ?''',
            (testID, )
        )
        # the SQL statement above performs a left join on the tests table with the testDetails table
        # this joins the testDetails table to the tests table where ever possible
        # selecting the questionIDs from the tests table now will return the questionIDs in the correct order
        questionIDs = self.c.fetchall()

        for item in questionIDs:
            questionID = int(str(item)[1:-2])
            questionData = self.getQuestion(questionID)
            question = Question(questionData)
            questionIDs[questionIDs.index(item)] = question
        return testID, questionIDs
        # this for loop formats the array from a list of tuples into a list of integers
        # in this form i can use this to create instances of the Question class and return that as questionSet

    def getTestQuestions(self, userPracticeID):
        self.c.execute(
            '''SELECT question, correct
            FROM userAnswer LEFT JOIN questions
            ON userAnswer.questionID = questions.questionID
            WHERE userPracticeID = ?''',
            (userPracticeID, )
        )
        return self.c.fetchall()

    def getQuestionsAndTestIDFromAssignmentID(self, assignmentID):
        self.c.execute(
            '''SELECT testID
            FROM setAssignments
            WHERE assignmentID = ?''',
            (assignmentID, )
        )
        testID = self.c.fetchone()
        testID = list(testID)[0]
        self.c.execute(
            '''SELECT questions.questionID, question, choice1, choice2, choice3, answer, topic
            FROM testDetails LEFT JOIN questions
            ON testDetails.questionID = questions.questionID
            WHERE testDetails.testID = ?''',
            (testID, )
        )
        questionSet = self.c.fetchall()
        # print(questionSet)
        testQuestions = []
        for item in questionSet:
            question = Question(item)
            testQuestions.append(question)
        return testQuestions, testID

    def getColourMode(self, userID):
        self.c.execute(
            '''SELECT darkMode
            FROM settings
            WHERE userID = ?''',
            (userID, )
        )
        colourMode = list(self.c.fetchone())[0]
        if colourMode == 0:
            colourMode = 'light'
            oppositeMode = 'dark'
        else:
            colourMode = 'dark'
            oppositeMode = 'light'
        return colourMode, oppositeMode


class Test:
    def __init__(self, numberOfQuestions, database):
        self.numberOfQuestions = numberOfQuestions
        self.database = database
        self.conn = sqlite3.connect('database.db')
        self.c = self.conn.cursor()
        self.testID = None

    def selectQuestions(self):
        self.c.execute(
            'SELECT COUNT(*) FROM questions'
        )
        count = self.c.fetchall()
        questionsInDB = int(str(count)[2:-3])
        selectedQuestions = []
        questionIDs = []
        dupeQuestion = False
        for i in range(self.numberOfQuestions):
            randomQuestionID = randint(1, questionsInDB)
            if randomQuestionID in questionIDs:
                dupeQuestion = True
            while dupeQuestion:
                randomQuestionID = randint(1, questionsInDB)
                if randomQuestionID not in questionIDs:
                    dupeQuestion = False
            question = self.database.getQuestion(randomQuestionID)
            questionIDs.append(int(question[0]))
            questionClass = Question(question)
            selectedQuestions.append(questionClass)
        return selectedQuestions

    def insertIntoDatabase(self, testQuestions):
        for question in testQuestions:
            questionID = question.getID()
            self.c.execute(
                '''INSERT INTO testDetails (testID, questionID)
                VALUES (?,?)''', (self.testID, questionID)
            )
        self.conn.commit()

    def setTestID(self, testID):
        self.testID = testID

    def getNumberOfQuestions(self):
        return self.numberOfQuestions


class Question:
    def __init__(self, questionData):
        self.questionID = questionData[0]
        self.question = questionData[1]
        self.choices = [
            questionData[2],
            questionData[3],
            questionData[4]
        ]
        self.answerIndex = str(int(questionData[5]) - 1)
        self.topic = questionData[6]

    def getData(self):
        return [
            self.questionID,
            self.question,
            self.choices,
            self.answerIndex,
            self.topic
        ]

    def getID(self):
        return self.questionID


# password = hashing.hashIt('test')


users = [
    (
        'hasnain', hashing.hashIt('test'), 'Mr', 'Hasnain',
        'Jaffer', '2016hjaffer01@beauchamp.org.uk', 1
    ),
    (
        '2016rbains', hashing.hashIt('hello'), 'Mr', 'Runveer',
        'Bains', '2016rbains@beauchamp.org.uk', 1
    ),
    (
        '2016hshields', hashing.hashIt('test1234'), 'Mr', 'Harry',
        'Shields', '2016hshields@beauchamp.org.uk', 1
    ),
    (
        '2016kpatel', hashing.hashIt('yes'), 'Mr', 'Kapish',
        'Patel', '2016kpatel@beauchamp.org.uk', 1
    ),
    (
        '2016jkey', hashing.hashIt('yes'), 'Mr', 'Jamie',
        'Key', '2016jkey@beauchamp.org.uk', 1
    ),
    (
        'edward.olszewski', hashing.hashIt('Password1'), 'Mr', 'Edward',
        'Olszewski', 'edward.olszewski@beauchamp.org.uk', 2
    ),
    (
        'teacher', hashing.hashIt('test1'), 'Mr', 'Hasnain',
        'Jaffer', 'teacher@email.com', 2
    ),
    (
        'admin', hashing.hashIt('admin'), '', '',
        '', '', 3
    ),
    (
        'sraigatt0', hashing.hashIt('test'), 'Ms', 'Saunders',
        'Raigatt', 'sraigatt0@gov.uk', 1
    ),
    (
        'blovel1', hashing.hashIt('test'), 'Ms', 'Burl',
        'Lovel', 'blovel1@tumblr.com', 1
    ),
    (
        'smorgue2', hashing.hashIt('test'), 'Ms', 'Morgue',
        'Sandye', 'smorgue2@unblog.fr', 1
    ),
    (
        'lbriand3', hashing.hashIt('test'), 'Ms', 'Letitia',
        'Briand', 'lbriand3@prweb.com', 1
    ),
    (
        'tbumphries4', hashing.hashIt('test'), 'Mr', 'Tadio',
        'Bumphries', 'tbumphries4@squidoo.com', 1
    ),
    (
        'tvane5', hashing.hashIt('test'), 'Mr', 'Tomaso',
        'Vane', 'tvane5@ihg.com', 1
    ),
    (
        'lamanger6', hashing.hashIt('test'), 'Mr', 'Lemmy',
        'aManger', 'lamanger6@fc2.com', 1
    ),
    (
        'aollis7', hashing.hashIt('test'), 'Ms', 'Anett',
        'Ollis', 'aollis7@blogger.com', 1
    ),
    (
        'tweson8 ', hashing.hashIt('test'), 'Mr', 'Tyson',
        'Weson', 'tweson8@npr.org', 1
    ),
    (
        'jwhitcomb9', hashing.hashIt('test'), 'Mr', 'Jamima',
        'Whitcomb', 'jwhitcomb9@networksolutions.com', 1
    ),
    (
        'cchetwina', hashing.hashIt('test'), 'Mr', 'Crawford',
        'Chetwin', 'cchetwina@a8.net', 1
    ),
    (
        'pbinesteadb', hashing.hashIt('test'), 'Ms', 'Pepi',
        'Binestead', 'pbinesteadb@mozilla.com', 1
    ),
    (
        'iandorc', hashing.hashIt('test'), 'Mrs', 'Ingra',
        'Andor', 'iandorc@army.mil', 2
    ),
    (
        'erowantreed', hashing.hashIt('test'), 'Mr', 'Eamon',
        'Rowantree', 'erowantreed@bandcamp.com', 1
    ),
    (
        'econgrevee', hashing.hashIt('test'), 'Mr', 'Egor',
        'Congreve', 'econgrevee@shareasale.com', 1
    )
]

questions = [
    (
        '4 × 3 ÷ 2 × 3',
        '18', '2',
        '12', 1, 'Arithmetic'
    ),
    (
        'Write 8 × 10^2 as an ordinary number',
        '80.0', '8000',
        '800', 3, 'Standard Form'
    ),
    (
        'Write 7.35 × 10^-1 as an ordinary number',
        '73.5', '0.0735',
        '0.735', 3, 'Standard Form'
    ),
    (
        'Write 4.36 × 10^4 as an ordinary number',
        '43600', '4360',
        '43.60', 2, 'Standard Form'
    ),
    (
        'Write 5 × 10^5 as an ordinary number',
        '500000', '5000',
        '500', 1, 'Standard Form'
    ),
    (
        'Write 1 × 10^-4 as an ordinary number',
        '100', '0.01',
        '0.0001', 3, 'Standard Form'
    ),
    (
        'Write 1.64 × 10^2 as an ordinary number',
        '0.0164', '164',
        '16.4', 2, 'Standard Form'
    ),
    (
        'Write 6.345 × 10^6 as an ordinary number',
        '634500', '6345000',
        '0.06345', 2, 'Standard Form'
    ),
    (
        'Write 8 × 10^4 as an ordinary number',
        '0.008', '800',
        '80000', 3, 'Standard Form'
    ),
    (
        'Write 7.53 × 10^-4 as an ordinary number',
        '753', '0.000753',
        '0.0754', 2, 'Standard Form'
    ),
    (
        'Write 0.64153 as a number in standard form',
        '6.4153 × 10^-1', '6.414 × 10^-3',
        '6.4153 × 10^2', 1, 'Standard Form'
    ),
    (
        'Write 56472.63 as a number in standard form',
        '5.647263 × 10^-4', '5.64 × 10^3',
        '5.647263 × 10^4', 3, 'Standard Form'
    ),
    (
        'Write 0.00046235 as a number in standard form',
        '4.623 × 10^-3', '4.6235 × 10^-4',
        '4.6235 × 10^4', 2, 'Standard Form'
    ),
    (
        'Write 34.742 as a number in standard form',
        '347.42', '3.4742 × 10',
        '3.4742 × 10^3', 2, 'Standard Form'
    ),
    (
        'Write 6475.324 as a number in standard form',
        '6.475324 × 10^1', '6.475324 × 10^3',
        '6.475324 × 10^-4', 2, 'Standard Form'
    ),
    (
        'Write 0.00345 as a number in standard form',
        '3.45 × 10^3', '3.45 × 10^-2',
        '3.45 × 10^-3', 3, 'Standard Form'
    ),
    (
        'Write 1.5435 as a number in standard form',
        '1.5435 × 10^-2', '1.5435 × 10^0',
        '154.35 × 10^1', 2, 'Standard Form'
    ),
    (
        'Write 1353.63 as a number in standard form',
        '1.35363 × 10^3', '1.35363 × 10^-2',
        '1.35363 × 10^1', 1, 'Standard Form'
    ),
    (
        'Write 26.464 as a number in standard form',
        '2.6464 × 10^1', '2.6464 × 10^3',
        '2.6464 × 10^-2', 1, 'Standard Form'
    ),
    (
        'Find the mean of 4, 9, 5',
        '12', '9', '6', 3, 'Averages'
    ),
    (
        'Find the range of 2, 10, 6',
        '6', '8', '10', 2, 'Averages'
    ),
    (
        'Find the nth term rule for the sequence: 1, 4, 9, 16',
        '3n-2', '3n+1', '3n', 1, 'Sequences'
    ),
    (
        'Solve: x + 4 ≤ 8',
        'x ≤ 4', '4 ≤ x',
        'x ≤ 12', 1, 'Algebra'
    ),
    (
        'Solve: 4x + 3 = 11',
        'x = 3', 'x = 2',
        'x = 3.5', 2, 'Algebra'
    ),
    (
        '8 × 15 = 10 × ?',
        '13', '12',
        '13.5', 2, 'Algebra'
    ),
    (
        '8.223 + 2.914',
        '11.137', '11.264',
        '12.564', 1, 'Arithmetic'
    ),
    (
        '0.0912 ÷ 0.12',
        '0.64', '0.76',
        '0.68', 2, 'Arithmetic'
    ),
    (
        '133 × 1.21',
        '174.71', '170.55',
        '160.93', 3, 'Arithmetic'
    ),
    (
        '92.69 − 58.69',
        '34', '34.6',
        '33', 1, 'Arithmetic'
    ),
    (
        'Find the median of 11, 18, 10, 26, 10, 21, 21, 31',
        '20.5', '20', '19.5', 3, 'Averages'
    ),
    (
        'Find the median of 13, 15, 17, 3, 1, 12, 35, 22',
        '12', '14', '13', 2, 'Averages'
    ),
    (
        'Find the median of 23, 2, 13, 34, 2, 8, 25, 32',
        '18', '20', '21', 1, 'Averages'
    ),
    (
        'Find the median of 11, 27, 2, 32, 7, 3, 30, 34, 25',
        '25', '23', '20', 1, 'Averages'
    ),
    (
        'Find the median of 35, 13, 16,  8, 28, 11, 7 ,7',
        '12.5', '14', '12', 3, 'Averages'
    ),
    (
        'Find the nth term rule for the sequence: 1, 6, 11, 16, ...',
        '5n - 4', '5n + 1', '5n', 1, 'Sequences'
    ),
    (
        'Find the nth term rule for the sequence: 2, 3, 4, 5, ...',
        'n', 'n + 1', 'n - 1', 2, 'Sequences'
    ),
    (
        'Find the nth term rule for the sequence: 2 ,7, 12, 17, ...',
        '5n - 2', '5n + 2', '5n - 3', 3, 'Sequences'
    ),
    (
        'Find the nth term rule for the sequence: 5, 6, 7, 8, ...',
        'n + 4', 'n + 5', '5n', 1, 'Sequences'
    ),
    (
        'Find the nth term rule for the sequence: 7, 9, 11, 13, ...',
        '2n + 7', '2n + 5', '2n + 8', 2, 'Sequences'
    ),
    (
        'In the ratio 2 : 6 : 9. The largest share was 36. What was the total?',
        '70', '68', '72', 2, 'Ratios'
    ),
    (
        'Share 144 in the ratio 7 : 3 : 2',
        '84 : 36 : 24', '84 : 34 : 26',
        '80 : 40 : 24', 1, 'Ratios'
    ),
    (
        'Share 176 in the ratio 7 : 6 : 9',
        '51 : 49 : 70', '52 : 48 : 68',
        '56 : 48 : 72', 3, 'Ratios'
    ),
    (
        'Share 147 in the ratio 6 : 9 : 6',
        '40 : 67 : 40', '42 : 63 : 42',
        '40 : 63 : 44', 2, 'Ratios'
    ),
    (
        'Share 45 in the ratio 8 : 2 : 5',
        '24 : 6 : 15', '20 : 10 : 15',
        '22 : 8 : 17', 1, 'Ratios'
    ),
    (
        'Share 70 in the ratio 2 : 1 : 7',
        '7 : 14 : 49', '14 : 7 : 49',
        '49 : 7 : 14', 2, 'Ratios'
    ),
    (
        'Share 48 in the ratio 8 : 2 : 6',
        '24 : 6 : 18', '20 : 10 : 18',
        '16 : 14 : 18', 1, 'Ratios'
    ),
    (
        'Solve: -6x + 23 = -3x + 2',
        'x = 8', 'x = 7', 'x = 5', 2, 'Algebra'
    ),
    (
        'Solve: -5x + 11 = -3x + 7',
        'x = 3', 'x = 5', 'x = 2', 3, 'Algebra'
    ),
    (
        'Solve: -2x + 45 = 4x - 3',
        'x = 8', 'x = 4', 'x = 7', 1, 'Averages'
    ),
    (
        'Solve: 70 - 7x = x - 2',
        'x = 9', 'x = 5', 'x = 11', 1, 'Algebra'
    ),
    (
        'Solve: 1 - 6x = 17 - 8x',
        'x = 11', 'x = 8', 'x = 12', 2, 'Algebra'
    ),
    (
        'Solve: x - 1 = 11 - 3x',
        'x = 7', 'x = 2', 'x = 3', 3, 'Algebra'
    ),
    (
        'Solve: 38 + 6x = -2 + 14x',
        'x = 7', 'x = 5', 'x = 3', 2, 'Algebra'
    ),
    (
        'Solve: -4x + 67 = 2x + 7',
        'x = 9', 'x = 7', 'x = 10', 3, 'Algebra'
    ),
    (
        'Solve: 7x + 23 = 15x + 7',
        'x = 1', 'x = 3', 'x = 2', 3, 'Algebra'
    ),
    (
        'Solve: 5x + 30 = -6 + 11x',
        'x = 3', 'x = 6', 'x = 4', 2, 'Averages'
    ),
    (
        'What is the probability of rolling a 6 on a dice?',
        '1/6', '1/3', '1/2', 1, 'Probability'
    ),
    (
        'What is the probability of rolling a 1 on a dice?',
        '1/1', '1/6', '6/1', 2, 'Probability'
    ),
    (
        'What is the probability of rolling an even number on a dice?',
        '1/2', '1/6', '1/3', 1, 'Probability'
    ),
    (
        'What is the probability of rolling an odd number on a dice?',
        '1/6', '1/2', '1/4', 2, 'Probability'
    ),
    (
        'HCF of 32, 52 and 28',
        '4', '12', '2', 1, 'Highest Common Factor'
    ),
    (
        'HCF of 153, 170 and 34',
        '7', '17', '13', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 70, 30 and 75',
        '8', '10', '5', 3, 'Highest Common Factor'
    ),
    (
        'HCF of 108, 66 and 36',
        '3', '6', '12', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 75, 240 and 45',
        '5', '15', '45', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 54, 27 and 90',
        '27', '3', '9', 3, 'Highest Common Factor'
    ),
    (
        'HCF of 80, 256 and 128',
        '24', '16', '32', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 44, 77 and 110',
        '11', '3', '7', 1, 'Highest Common Factor'
    ),
    (
        'HCF of 255, 289 and 68',
        '13', '17', '15', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 288, 18 and 198',
        '18', '6', '9', 1, 'Highest Common Factor'
    ),
    (
        'HCF of 44, 12 and 24',
        '6', '4', '12', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 13, 143 and 104',
        '6', '7', '13', 3, 'Highest Common Factor'
    ),
    (
        'HCF of 10, 40 and 180',
        '5', '10', '20', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 48, 18 and 15',
        '3', '6', '4', 1, 'Highest Common Factor'
    ),
    (
        'HCF of 84, 144 and 36',
        '12', '18', '3', 1, 'Highest Common Factor'
    ),
    (
        'HCF of 196, 140 and 84',
        '20', '28', '14', 2, 'Highest Common Factor'
    ),
    (
        'HCF of 10, 36 and 30',
        '3', '6', '2', 3, 'Highest Common Factor'
    ),
    (
        'HCF of 24, 8 and 16',
        '4', '8', '12', 2, 'Highest Common Factor'
    ),
    (
        'Find the equation of the circle (-18, -32), radius 13.',
        '(x - 18)^2 + (y - 32)^2 = 13*2', '(x + 18)^2 + (y + 32)^2 = 13*2',
        '(x + 18)^2 + (y + 32)^2 = 13^2', 3, 'Equations Of Circles'
    ),
    (
        'Find the equation of the circle (-15, -19), radius 26.',
        '(x + 19)^2 + (y + 15)^2 = 26^2', '(x + 15)^2 + (y + 19)^2 = 26^2',
        '(x - 19)^2 + (y - 15)^2 = 26^2', 2, 'Equations Of Circles'
    ),
    (
        'Find the equation of the circle (-28, -23), radius 24.',
        '(x + 28)^2 + (y + 23)^2 = 12^2', '(x - 28)^2 + (y - 23)^2 = 12^2',
        '(x + 28)^2 + (y + 23)^2 = 24^2', 3, 'Equations Of Circles'
    ),
    (
        'Find the equation of the circle (20, -23), radius 5.',
        '(x - 20)^2 + (y + 23)^2 = 5^2', '(x + 20)^2 + (y - 23)^2 = 10^2',
        '(x - 20)^2 + (y - 23)^2 = 5^2', 1, 'Equations Of Circles'
    ),
    (
        'Find the equation of the circle (1.2, 5), radius 22.',
        '(x - 1.2)^2 + (y - 5)^2 = 22^2', '(x + 5)^2 + (y - 1.2)^2 = 11^2',
        '(x - 5)^2 + (y + 1.2)^2 = 11^2', 1, 'Equations Of Circles'
    ),
    (
        'Find the equation of the circle (-6.4, -24), radius 12.',
        '(x - 6.4)^2 + (y + 24)^2 = 12*2', '(x + 6.4)^2 + (y - 24)^2 = 24',
        '(x + 6.4)^2 + (y + 24)^2 = 12^2', 3, 'Equations Of Circles'
    ),
    (
        'Find the equation of the circle at the origin, radius 13.',
        'x^2 - y^2 = 144', 'x^2 + y^2 = 13^2',
        '(x + 1)^2 - (y + 1)^2 = 13^2', 2, 'Equations Of Circles'
    ),
    (
        'Factorise: 2x^2 - 24x + 70',
        '(2x - 10)(x - 7)', '(2x + 10)(x - 7)',
        '(x - 10)(2x - 7)', 1, 'Factorisation'
    ),
    (
        'Factorise: 3x^2 - 32x + 20',
        '(3x + 10)(x + 2)', '(3x - 10)(x - 2)',
        '(3x - 2)(x - 10)', 3, 'Factorisation'
    ),
    (
        'Factorise: 3x^2 - 34x + 63',
        '(3x + 7)(x - 9)', '(3x + 5)(x - 12)',
        '(3x - 7)(x - 9)', 3, 'Factorisation'
    ),
    (
        'Factorise: -x^2 + 3x + 10',
        '-(x - 2)(-x - 4)', '-(x + 2)(x - 5)',
        '-(-x - 2)(x - 5)', 2, 'Factorisation'
    ),
    (
        'Factorise: x^2 - 10x + 24',
        '(x - 4)(x - 6)', '(x + 4)(x + 6)',
        '(x - 24)(x - 1)', 1, 'Factorisation'
    ),
    (
        'Factorise: -x^2 + 2x + 80',
        '-(x - 8)(x + 10)', '-(x + 8)(x - 10)',
        '(x + 8)(x - 10)', 2, 'Factorisation'
    ),
    (
        'Factorise: -2x^2 + 6x + 8',
        '-2(x + 1)(x - 4)', '-(x + 1)(2x + 4)',
        '(x - 1)(2x - 4)', 1, 'Factorisation'
    )
]
