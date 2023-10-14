import unittest
import time
import tkinter as tk
from main import StudyTimer

class TestStudyTimer(unittest.TestCase):
    def setUp(self):
        self.root = tk.Tk()
        self.study_timer = StudyTimer(self.root)

    def test_timer_starts(self):
        self.study_timer.start_timer()
        self.assertIsNotNone(self.study_timer.time_start)

    def test_timer_stops(self):
        self.study_timer.start_timer()
        time.sleep(2)
        self.study_timer.stop_timer()
        self.assertIsNone(self.study_timer.time_start)

    def test_timer_updates_label(self):
        self.study_timer.start_timer()
        time.sleep(2)
        self.study_timer.update_timer()
        self.assertRegex(self.study_timer.timer_label.cget("text"), r"\d{2}:\d{2}:\d{2}")

    def tearDown(self):
        self.root.destroy()

if __name__ == '__main__':
    unittest.main()