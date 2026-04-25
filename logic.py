from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import *
from gui import *
import csv
class Logic(QMainWindow, Ui_MainWindow):
    '''
    Creates a class called Logic that imports QMainWindow and UI_Mainwindow, which are necessary to allow our gui.py
    code to be edited while providing a window Layout with QMainWindow. Now, we can access our GUI widgets directly
    using self.(variablename).
    '''
    def __init__(self) -> None:
        #        #Init function and things below were inspired by the Graphical user interface lecture, page 21

        '''
         Ensures that all our instance varaibles are usable and not lost in the other peices of the code. It also intializes several lists and values that we need
         to do validation checks. Lastly, and most improtantly, it sets up teh UI with super().__init__()) and setup UI so we can actually use it.
        '''
        self.numbers = ['0', '1', '2','3','4', '5', '6', '7', '8', '9']
        self.special_symbols = ['!','@','#','$','%','^','&','*', '-', '(', ')', '+', '=']
        super().__init__()
        self.setupUi(self)
        self.name_list = []
        self.test_list = []
        self.total_scores = []
        self.green = False
        self.red = False
        self.average = 0
        self.total = 0
        self.submit.clicked.connect(self.submit_1)
        self.number_of_scores.returnPressed.connect(self.prevent_error_message)
        self.attempts = 0
        self.load_from_csv()
        self.error = False

    def load_from_csv(self) -> None:
        #    #12, files.pdf Lecture page 16, lab 4. Inspired both load_from_csv and write_to_csv.

        '''
        Loads the csv into both total_scores and name_list so we can keep track of studdent scores and set up a list that allows us to check for duplicate names.
        '''

        with open('student_data.csv', 'r', newline='') as csv_file:
            content = csv.reader(csv_file, delimiter=',')
            for line in content:
                self.total_scores.append(line)
                self.name_list.append(line[0]) #Pycharm AI suggestion

    def submit_1(self)-> None:
        '''
        This makes sure that all our functions run after the button is clicked. We connected the submit button to this function for that reason.
        The way it does this is by doing a bunch of conditional statements with boloean values and then exiting a funciton and coloring the submit button red
        if it doesn't work. This function then runs other functions if everything else is successful. Finally, it determines your input as valid.
        '''
        self.red = False
        self.test_list = []
        name = self.student_name.text().strip()
        if not self.student_name_check(name):
            self.red_button()
            return
        if not self.prevent_error_message():
            self.red_button()
            return
        if not self.grade_validation():
            self.red_button()
            return
        self.green_button()
        self.student_data()
        self.submit_message.setText("All Inputs Valid")


    def student_name_check(self, name: str)-> bool:
        '''
        This function goes through a series of checks on symbols numbers and duplicates in order to make sure the users name input is valid. It then returns a boolean
        value depending on whether it is.
        :param name: User input of their name, this is the parameter.
        :return: the function returns a boolean value depending on if the name input is valid.
        '''
        name = self.student_name.text().strip()
        for prevent_duplicates in self.name_list:
            if name == prevent_duplicates:
                self.submit_message.setText("Duplicate Name")
                self.red = True
                return False

        if name == "":
            self.submit_message.setText("No Name Submitted")
            self.red = True
            return False

        for number_check in name:
            if number_check in self.numbers:
                self.submit_message.setText("No Numbers Allowed")
                self.red = True
                return False

        for symbol_check in name:
            if symbol_check in self.special_symbols:
                self.submit_message.setText("No Symbols Allowed")
                self.red = True
                return False

        if len(name) < 2:
            self.submit_message.setText("Please Enter a Name")
            self.red = True
            return False

        self.name_list.append(name)
        return True


    def score_numbers_check(self)-> bool:
        '''
        Very similar to student_name_check because it also returns a boolean value. Except this time its checking the number of scores
        the student is entering in to make sure they dont enter more than 4 scores, and that the input is 1,2,3, or 4.
        :return: This function returns a boolean that is used later to call the function in submit_1
        '''
        attempts = self.number_of_scores.text()
        if attempts == "":
            self.submit_message.setText("Please Enter a Number")
            self.red = True
            return False
        if not attempts.isdigit():
            self.submit_message.setText("Please Enter a Number")
            self.red = True
            return False
        attempts = int(attempts)
        if attempts < 1 or attempts > 4:
            self.submit_message.setText("Please Enter a Number from 1-4")
            self.red = True
            return False
        self.attempts = attempts
        return True

    def prevent_error_message(self)-> bool:
        '''
        This function prevents a specific error I encountered during the code. That error was that it the submit_message button showed an error
        after the user pressed enter on the score attempts because it thought that the user scores were not entered. But the scores are hidden until they
        click enter.
        :return: This returns a boolean value if the function passes, otherwise it will return a false value, this will determine whether the display button
        is red or green.
        '''
        if not self.score_numbers_check():
            self.error = True
            self.red = True
            return False
        self.display_check()
        self.error = False
        return True

    def display_check(self)-> None:
        '''
        This function hides certain scores or shows them depending on how many scores the user is putting in for the respective student.
        It does this through a set of repetitive, conditional if statements. All of them are if because I want it to run through every option to make sure
        all scores are shown.
        '''
        if self.attempts == 1:
            self.score_1.show()
            self.score1_show.show()
            self.score2_show.hide()
            self.score_2.hide()
            self.score3_show.hide()
            self.score_3.hide()
            self.score4_show.hide()
            self.score_4.hide()
        elif self.attempts == 2:
            self.score_1.show()
            self.score1_show.show()
            self.score2_show.show()
            self.score_2.show()
            self.score3_show.hide()  #.hide() and .show() were derived from this website: https://www.pythonguis.com/faq/show-and-hide-widget/
            self.score_3.hide()
            self.score4_show.hide()
            self.score_4.hide()
        elif self.attempts == 3:
            self.score_1.show()
            self.score1_show.show()
            self.score2_show.show()
            self.score_2.show()
            self.score3_show.show()
            self.score_3.show()
            self.score_4.hide()
            self.score4_show.hide()
        elif self.attempts == 4:
            self.score_1.show()
            self.score1_show.show()
            self.score2_show.show()
            self.score_2.show()
            self.score3_show.show()
            self.score_3.show()
            self.score_4.show()
            self.score4_show.show()

    def grade_validation(self)-> bool:
        '''
        This function makes sure the students grade inputs are between 0-100. After this, it appends each score to two key lists.
        THe first is test_list, which I use later on to determine the average, lowest, and highest scores of the current student.
        The other is total_scores which is put into a csv list to determine all student scores.
        :return: This returns a boolean value that determines whether the function is called or not.
        '''
        self.total_scores = []
        if self.attempts >= 1:
            score_1 = self.score_1.text()
            if score_1 == "":
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            if not score_1.isdigit():
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            score_1 = int(score_1)
            if score_1 < 0 or score_1 > 100:
                self.submit_message.setText("Please Enter a Number from 0-100")
                self.red = True
                return False
            self.total_scores.append(score_1)
            self.test_list.append(score_1)


        if self.attempts >= 2:
            score_2 = self.score_2.text()
            if score_2 == "":
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            if not score_2.isdigit():
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            score_2= int(score_2)
            if score_2 < 0 or score_2 > 100:
                self.submit_message.setText("Please Enter a Number from 0-100")
                self.red = True
                return False
            self.total_scores.append(score_2)
            self.test_list.append(score_2)



        if self.attempts >= 3:
            score_3 = self.score_3.text()
            if score_3 == "":
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            if not score_3.isdigit():
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            score_3 = int(score_3)
            if score_3 < 0 or score_3 > 100:
                self.submit_message.setText("Please Enter a Number from 0-100")
                self.red = True
                return False
            self.total_scores.append(score_3)
            self.test_list.append(score_3)


        if self.attempts == 4:
            score_4 = self.score_4.text()
            if score_4 == "":
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            if not score_4.isdigit():
                self.submit_message.setText("Please Enter a Number")
                self.red = True
                return False
            score_4 = int(score_4)
            if score_4 < 0 or score_4 > 100:
                self.submit_message.setText("Please Enter a Number from 0-100")
                self.red = True
                return False
            self.total_scores.append(score_4)
            self.test_list.append(score_4)

        self.write_to_csv()
        return True
    def write_to_csv(self)-> None:
        '''
        This function writes the candidate profiles to a csv file.
        '''
        #Code structure repurposed from youtube video: https://www.youtube.com/watch?v=MGes28nDERk&t=64s
        with open('student_data.csv', 'a', newline = '') as csv_file:
            writer = csv.writer(csv_file) #FIXME
            writer.writerow([self.student_name.text()] + self.total_scores) # this line was generated with ChatGPT assistance

    def student_data(self) -> None:
        '''
        This function calculates the students highest, lowest, and average score. It uses the data in test_list, which was appended by grade_validation,
        and then it changes the text of the Qlabel depending on what the scores are. To determine the highest score, I set it to 0 and saw which number in the list was
        greater by continously reassining the self.highscore variable. I did the same with lowscore, and for average I used the sum button which I found on a forum.
        '''
        self.highscore = 0
        self.lowscore = 100
        for i in self.test_list:
            if i > self.highscore:
                self.highscore = i
        self.highest_score.setText(str(self.highscore))

        for j in self.test_list:
            if j < self.lowscore:
                self.lowscore= j
        self.lowest_score.setText(str(self.lowscore))

        self.total = sum(self.test_list) #This piece of code was inspired by this forum: https://stackoverflow.com/questions/4362586/sum-a-list-of-numbers-in-python

        if self.attempts == 1:
            self.average = self.total
            self.average_score.setText(str(self.average))

        elif self.attempts == 2:
            self.average = self.total/2
            self.average_score.setText(str(self.average))

        elif self.attempts == 3:
            self.average = self.total/3
            self.average_score.setText(str(self.average))

        elif self.attempts == 4:
            self.average = self.total/4
            self.average_score.setText(str(self.average)) #Str additions to average_score, lowest_score, and highest_score was a solution found by AI debugging

    def red_button(self) -> None:
        '''
        This function changes the submit_message button color depending on if the function has a true or false boolean value, to tell the user an input is invalid.
        '''
        # This function was inspired by the post with 28 upvotes on this website:  https://stackoverflow.com/questions/2749798/qlabel-set-color-of-text-and-background
        self.red = True
        color = QColor("red")
        self.submit_message.setStyleSheet("QLabel {background-color : %s }" % color.name())
        return True
    def green_button(self) -> None:
        '''
        This function is run if the red button function fails or doesn't run , and it just shows the user that their input is valid.
        '''
        # This function was inspired by the post with 28 upvotes on this website:  https://stackoverflow.com/questions/2749798/qlabel-set-color-of-text-and-background
        self.red = False
        color = QColor("green")
        self.submit_message.setStyleSheet("QLabel {background-color : %s }" % color.name())














































