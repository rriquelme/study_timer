import sys
import datetime
import json
import calendar
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
        self.hrows = QHBoxLayout()
        #self.setLayout(self.hrows)
        # First will be the header for the habits
        # Create a new row for the button and habit input
        self.create_ui()
        #self.create_ui()
        button_row = QHBoxLayout()
        self.habit_input = QLineEdit()
        button_row.addWidget(self.habit_input)
        self.new_habit_button = QPushButton("New Habit")
        self.new_habit_button.clicked.connect(self.add_new_habit)
        button_row.addWidget(self.new_habit_button)


        # Add the grid and button to the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.hrows)
        main_layout.addLayout(button_row)
        self.setLayout(main_layout)


    def create_ui(self):
        #self.hrows = QHBoxLayout()
        self.load_habits()
        now = datetime.datetime.now()
        len_month = calendar.monthrange(now.year, now.month)[1]
        self.v0 = QVBoxLayout()
        day_label = QLabel("Habits:")
        day_label.setAlignment(Qt.AlignVCenter)
        self.v0.addWidget(day_label)
        for habit in self.habits:
            day_label = QLabel(habit['name'])
            day_label.setAlignment(Qt.AlignVCenter)
            self.v0.addWidget(day_label)
        self.hrows.addLayout(self.v0)
        
        # Then the days of the month
        self.vx = []
        for i in range(1, len_month+1):
            #vx = QVBoxLayout()
            self.vx.append(QVBoxLayout())
            day = QDate(now.year, now.month, i)
            day_label = QLabel(str(i)+"|"+day.toString("ddd")[0])
            self.vx[-1].addWidget(day_label)
            for habit in self.habits:
                self.vx[-1].addWidget(self.to_square(habit['days'][str(i)],i,habit['name']))
            self.hrows.addLayout(self.vx[-1])

    def resize_ui(self,habit_name, days):
        self.v0.addWidget(QLabel(habit_name))
        for x in range(1, len(self.vx)+1):
            #print("---",days[1])
            self.vx[x-1].addWidget(self.to_square(days[x],x,habit_name))

    def to_square(self, color,ndate,habit_name):
        day = QDate(2023, 10, ndate)
        square = Square(day,habit_name)
        if color == "green":
            square.color = Qt.green
        else:
            if datetime.datetime.today().day == day.day():
                square.color = Qt.yellow
            elif day.toString("ddd")[0] == 'd' or day.toString("ddd")[0] == 's':
                square.color = Qt.gray
            else:
                square.color = Qt.white
        return square

    def add_new_habit(self):
        habit_name = self.habit_input.text()
        if habit_name:
            d = {}
            now = datetime.datetime.now()
            len_month = calendar.monthrange(now.year, now.month)[1]
            for x in range(1,len_month+1):
                d[x] = "white"
            self.habits.append({"name": habit_name, "days": d})
            self.habit_input.clear()
            self.save_habits()
        self.resize_ui(self.habits[-1]['name'],self.habits[-1]['days'])

    def save_habits(self):
        with open("habits.json", "w") as f:
            json.dump(self.habits, f, indent=4)

    def load_habits(self):
        try:
            with open("habits.json", "r") as f:
                self.habits = json.load(f)
        except FileNotFoundError:
            self.habits = []

    def closeEvent(self, event):
        self.save_habits()

class Square(QWidget):
    def __init__(self, day,habit_name):
        super().__init__()
        self.day = day
        self.habit_name = habit_name
        #if datetime.datetime.today().day == self.day.day():
        #    self.color = Qt.yellow
        #else:
        #    self.color = Qt.white
        self.setMinimumSize(QSize(20, 20))
        self.setMaximumSize(QSize(20, 20))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(QRect(QPoint(0, 0), QSize(20, 20)))

    def mousePressEvent(self, event):
        if self.color != Qt.green:
            self.color = Qt.green
            for x in self.parent().habits:
                if x['name'] == self.habit_name:
                    x['days'][str(self.day.day())] = "green"
        else:
            for x in self.parent().habits:
                if x['name'] == self.habit_name:
                    x['days'][str(self.day.day())] = "white"

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
