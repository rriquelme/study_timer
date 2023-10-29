import sys
import datetime
import json
import calendar
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton, QLineEdit, QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint, QSize, QDate
import os

custom_green = QColor(34, 177, 34)
custom_yellow = QColor(255,201,14)
custom_gray = QColor(153,217,234)
custom_future = QColor(141,219,124)
# change dir to read json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

class HabitTracker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Habit Tracker")
        self.initUI()
    
    def d_to_s(self, d):
        return d.toString("yyyy-MM-dd")
    
    def initUI(self):
        # Create a header row with the days of the month for October
        self.hrows = QHBoxLayout()
        self.create_ui()
        button_row = QHBoxLayout()
        self.habit_input = QLineEdit()
        button_row.addWidget(self.habit_input)
        self.new_habit_button = QPushButton("New Habit")
        self.new_habit_button.clicked.connect(self.add_new_habit)
        button_row.addWidget(self.new_habit_button)
        self.sort_habits_button = QPushButton("Sort Habits")
        self.sort_habits_button.clicked.connect(self.sort_habits)
        button_row.addWidget(self.sort_habits_button)


        # Add the grid and button to the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(self.hrows)
        main_layout.addLayout(button_row)
        self.setLayout(main_layout)


    def create_ui(self):
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
        self.hrows.insertLayout(0,self.v0)
        
        self.vx = []
        for i in range(1, len_month+1):
            self.vx.append(QVBoxLayout())
            day = QDate(now.year, now.month, i)
            day_label = QLabel(str(i))#+"|"+day.toString("ddd")[0])
            self.vx[-1].addWidget(day_label)
            for habit in self.habits:
                self.vx[-1].addWidget(self.to_square(habit['days'][self.d_to_s(day)],i,habit['name']))
            self.hrows.insertLayout(i,self.vx[-1])
        
    def resize_ui(self,habit_name, days):
        self.v0.addWidget(QLabel(habit_name))
        for x in range(1, len(self.vx)+1):
            #needs fixing
            self.vx[x-1].addWidget(self.to_square(days[x],x,habit_name))

    def to_square(self, color,ndate,habit_name):
        now = datetime.datetime.now()
        day = QDate(now.year, now.month, ndate)
        square_date = datetime.datetime(now.year, now.month, ndate)
        square = Square(day,habit_name)
        if color == "Done":
            square.color = custom_green
        elif color == "Future":
            square.color = custom_future
        else:
            if datetime.datetime.today().day == day.day():
                square.color = custom_yellow
            elif day.toString("ddd")[0] == 'd' or day.toString("ddd")[0] == 's':
                square.color = custom_gray
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
                # needs fixing
                d[x] = "-"
            self.habits.append({"name": habit_name, "days": d})
            self.habit_input.clear()
            self.save_habits()
            self.resize_ui(self.habits[-1]['name'],self.habits[-1]['days'])

    def sort_habits(self):
        # Create a new window to be able to sort habits
        self.sort_window = QWidget()
        self.sort_window.setWindowTitle("Sort Habits")
        self.sort_window.resize(400, 200)
        self.sort_window.setLayout(QVBoxLayout())
        # Add the habits
        self.sort_habits = QTreeWidget()
        self.sort_habits.setDragDropMode(QTreeWidget.InternalMove)
        self.sort_habits.setDragEnabled(True)
        self.sort_habits.setDropIndicatorShown(True)
        self.sort_habits.setDragDropOverwriteMode(False)
        self.sort_habits.setDropIndicatorShown(True)
        self.sort_habits.setColumnCount(1)
        # Enable drag and drop on qtreewidget
        self.sort_habits.setHeaderLabel('Habits')
        for habit in self.habits:
            item = QTreeWidgetItem(self.sort_habits, [habit['name']])
            item.setFlags(item.flags() | Qt.ItemIsEditable)
        self.sort_window.layout().addWidget(self.sort_habits)
        # Add the save button
        apply_button = QPushButton("Apply")
        apply_button.clicked.connect(self.apply_sort)
        self.sort_window.layout().addWidget(apply_button)
        self.sort_window.show()

    def apply_sort(self):
        # print the new order of the habits
        if self.sort_habits.topLevelItemCount() == len(self.habits):
            temp_sorting_array = [ self.sort_habits.topLevelItem(x).text(0) for x in range(self.sort_habits.topLevelItemCount() ) ]
            temp_list = []
            for x in temp_sorting_array:
                for y in self.habits:
                    if x == y['name']:
                        temp_list.append(y)
                        break
            self.habits = temp_list
            self.save_habits()
            self.refresh_ui()
    
    # Create a function to refresh the ui
    def refresh_ui(self):
        # Clear the ui
        for i in range(self.hrows.count()):
            for x in range(len(self.habits)+1):
                if self.hrows.itemAt(i).itemAt(x) != None:
                    self.hrows.itemAt(i).itemAt(x).widget().hide()
                    self.hrows.itemAt(i).itemAt(x).widget().setParent(None)
                    self.hrows.itemAt(i).itemAt(x).widget().deleteLater()
            self.hrows.itemAt(i).deleteLater()

        # Recreate the ui
        self.create_ui()

    def save_habits(self):
        with open("habits.json", "w") as f:
            d = {}
            d['config'] = {}
            d['habits'] = self.habits
            json.dump(d, f, indent=4)

    def load_habits(self):
        try:
            with open("habits.json", "r") as f:
                d = json.load(f)
                self.habits = d.get('habits', [])
        except FileNotFoundError:
            self.habits = []

    def closeEvent(self, event):
        self.save_habits()

class Square(QWidget):
    def __init__(self, day,habit_name):
        super().__init__()
        self.day = day
        self.habit_name = habit_name
        self.setMinimumSize(QSize(20, 20))
        self.setMaximumSize(QSize(20, 20))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(QRect(QPoint(0, 0), QSize(20, 20)))

    def mousePressEvent(self, event):
        aux = "Done"
        for x in self.parent().habits:
                if x['name'] == self.habit_name:
                    aux = x['days'][self.parent().d_to_s(self.day)]
                    break
        now = datetime.datetime.now()
        if self.day.day() == now.day:
            if aux == "Done":
                aux = "Future"
                self.color = custom_future
            elif aux == "Future":
                aux = "-"
                if datetime.datetime.today().day == self.day.day():
                    self.color = custom_yellow
                elif self.day.toString("ddd")[0] == 'd' or self.day.toString("ddd")[0] == 's':
                    self.color = custom_gray
                else:
                    self.color = Qt.white   
            elif aux == "-":
                aux = "Done"
                self.color = custom_green
            for x in self.parent().habits:
                if x['name'] == self.habit_name:
                    x['days'][self.parent().d_to_s(self.day)] = aux
        elif aux == "Future":
            for x in self.parent().habits:
                if x['name'] == self.habit_name:
                    x['days'][self.parent().d_to_s(self.day)] = "-"

            if datetime.datetime.today().day == self.day.day():
                self.color = custom_yellow
            elif self.day.toString("ddd")[0] == 'd' or self.day.toString("ddd")[0] == 's':
                self.color = custom_gray
            else:
                self.color = Qt.white
        elif aux == "-":
            now = datetime.datetime.now()
            square_date = datetime.datetime(now.year, now.month, self.day.day())
            if now < square_date:
                for x in self.parent().habits:
                    if x['name'] == self.habit_name:
                        x['days'][self.parent().d_to_s(self.day)] = "Future"
                self.color = custom_future
            else:
                self.color = custom_green
                for x in self.parent().habits:
                    if x['name'] == self.habit_name:
                        x['days'][self.parent().d_to_s(self.day)] = "Done"
            #self.color = custom_green
        elif aux == "Done":
            for x in self.parent().habits:
                if x['name'] == self.habit_name:
                    x['days'][self.parent().d_to_s(self.day)] = "-"

            if datetime.datetime.today().day == self.day.day():
                self.color = custom_yellow
            elif self.day.toString("ddd")[0] == 'd' or self.day.toString("ddd")[0] == 's':
                self.color = custom_gray
            else:
                self.color = Qt.white
        self.update()
        self.parent().save_habits()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    habit_tracker = HabitTracker()
    habit_tracker.show()
    sys.exit(app.exec_())
