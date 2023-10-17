import sys
import datetime
import json
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint, QSize, QDate
import os
# change dir to read json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class HabitTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.initUI()

    def initUI(self):
        # Create a header row with the days of the month for October
        habit_row = QHBoxLayout()
        day_label = QLabel("Habits:")
        habit_row.addWidget(day_label)
        for i in range(1, 32):
            day_label = QLabel(str(i))
            #day_label = QLabel(str(i) + "(" + QDate(2023, 10, i).toString("ddd")[0] + ")")
            habit_row.addWidget(day_label)

        # Create a grid layout for the habits
        self.grid = QGridLayout()
        self.grid.addLayout(habit_row, 0, 0)
        self.habit_rows = []
        self.load_habits()
        for habit in self.habits:
            self.add_habit_row(habit["name"], habit["squares"])

        # Create a new row for the button and habit input
        button_row = QHBoxLayout()
        self.habit_input = QLineEdit()
        button_row.addWidget(self.habit_input)
        self.new_habit_button = QPushButton("New Habit")
        self.new_habit_button.clicked.connect(self.add_new_habit)
        button_row.addWidget(self.new_habit_button)

        # Add the grid and button to the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.grid)
        main_layout.addLayout(button_row)

        self.setLayout(main_layout)

    def add_habit_row(self, habit_name, squares):
        habit_row = QHBoxLayout()
        day_label = QLabel(habit_name)
        habit_row.addWidget(day_label)

        # For each habit row, create a colored square for each day of the month
        habit_squares = []
        for i in range(1, 32):
            day = QDate(2023, 10, i)
            #print(day.toString("ddd")[0])
            square = Square(day)
            if squares[i-1] == "green":
                square.color = Qt.green
            else:
                if datetime.datetime.today().day == day.day():
                    square.color = Qt.yellow
                elif day.toString("ddd")[0] == 'd' or day.toString("ddd")[0] == 's':
                    square.color = Qt.gray
                else:
                    square.color = Qt.white
            habit_squares.append(square)
            habit_row.addWidget(square)

        self.grid.addLayout(habit_row, len(self.habit_rows)+1, 0)
        self.habit_rows.append((habit_name, habit_squares))

    def add_new_habit(self):
        habit_name = self.habit_input.text()
        if habit_name:
            row = len(self.habit_rows) + 1
            squares = ["white"] * 31
            self.add_habit_row(habit_name, squares)
            self.habit_input.clear()
            self.save_habits()

    def save_habits(self):
        habits = []
        for habit_name, habit_squares in self.habit_rows:
            squares = []
            for square in habit_squares:
                if square.color == Qt.green:
                    squares.append("green")
                else:
                    squares.append("white")
            habits.append({"name": habit_name, "squares": squares})
        with open("habits.json", "w") as f:
            json.dump(habits, f, indent=4)

    def load_habits(self):
        try:
            with open("habits.json", "r") as f:
                self.habits = json.load(f)
        except FileNotFoundError:
            self.habits = []

    def closeEvent(self, event):
        self.save_habits()

class Square(QWidget):
    def __init__(self, day):
        super().__init__()
        self.day = day
        if datetime.datetime.today().day == self.day.day():
            self.color = Qt.yellow
        else:
            self.color = Qt.white
        self.setMinimumSize(QSize(20, 20))
        self.setMaximumSize(QSize(20, 20))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(QRect(QPoint(0, 0), QSize(20, 20)))

    def mousePressEvent(self, event):
        if self.color != Qt.green:
            self.color = Qt.green
        else:
            if datetime.datetime.today().day == self.day.day():
                self.color = Qt.yellow
            elif self.day.toString("ddd")[0] == 'd' or self.day.toString("ddd")[0] == 's':
                self.color = Qt.gray
            else:
                self.color = Qt.white
        self.update()
        self.parent().save_habits()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    habit_tracker = HabitTracker()
    habit_tracker.show()
    sys.exit(app.exec_())
