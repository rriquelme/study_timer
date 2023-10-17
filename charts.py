import sys
import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QGridLayout, QPushButton
from PyQt5.QtGui import QColor, QPainter, QBrush
from PyQt5.QtCore import Qt, QRect, QPoint, QSize, QDate

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
        grid = QGridLayout()
        grid.addLayout(habit_row, 0, 0)
        for j in range(1, 5):
            habit_row = QHBoxLayout()
            day_label = QLabel("Habit " + str(j)*j)
            habit_row.addWidget(day_label)

            # For each habit row, create a colored square for each day of the month
            habit_squares = []
            for i in range(1, 32):
                day = QDate(2023, 10, i)
                square = Square(day)
                habit_squares.append(square)
                habit_row.addWidget(square)

            grid.addLayout(habit_row, j, 0)

        # Create a new row for the button
        button_row = QHBoxLayout()
        button = QPushButton("New Button")
        button_row.addWidget(button)

        # Add the grid and button to the main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(grid)
        main_layout.addLayout(button_row)

        self.setLayout(main_layout)

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
        if self.color == Qt.white or self.color == Qt.yellow:
            self.color = Qt.green
        else:
            self.color = Qt.white
        self.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    habit_tracker = HabitTracker()
    habit_tracker.show()
    sys.exit(app.exec_())
