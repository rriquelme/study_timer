import time
import tkinter as tk

class StudyTimer:
    def __init__(self, master):
        self.master = master
        master.geometry("400x250")
        master.title("Study Timer")

        self.timer_label = tk.Label(master, text="00:00:00", font=("Arial", 24))
        self.timer_label.pack(pady=20)

        button_frame = tk.Frame(master)
        button_frame.pack()

        self.start_button = tk.Button(button_frame, text="Start", command=self.start_timer, font=("Arial", 16), width=10)
        self.start_button.grid(row=0, column=0, padx=10, pady=10)

        self.stop_button = tk.Button(button_frame, text="Stop", command=self.stop_timer, state=tk.DISABLED, font=("Arial", 16), width=10)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10)

        self.save_button = tk.Button(button_frame, text="Save", command=self.save_timer, state=tk.DISABLED, font=("Arial", 16), width=10)
        self.save_button.grid(row=1, column=0, padx=10, pady=10)

        self.reset_button = tk.Button(button_frame, text="Reset", command=self.reset_timer, state=tk.DISABLED, font=("Arial", 16), width=10)
        self.reset_button.grid(row=1, column=1, padx=10, pady=10)

        self.time_start = None

    def set_button_configs(self, start_state, stop_state, save_state, reset_state):
        self.start_button.config(state=start_state)
        self.stop_button.config(state=stop_state)
        self.save_button.config(state=save_state)
        self.reset_button.config(state=reset_state)

    def start_timer(self):
        self.time_start = time.time()
        self.update_timer()
        self.set_button_configs(tk.DISABLED, tk.NORMAL, tk.DISABLED, tk.DISABLED)

    def stop_timer(self):
        self.time_start = None
        self.set_button_configs(tk.NORMAL, tk.DISABLED, tk.NORMAL, tk.NORMAL)

    def save_timer(self):
        file = open('saved_times.txt','a')
        diff_time = time.time() - self.time_start
        file.write("".join([time.ctime(),' ',str(int(diff_time/3600)),'hours,',str(int((diff_time%3600)/60)),'mins,',str(int((diff_time%3600)%60)),'seconds','\n']))
        file.close()
        self.set_button_configs(tk.NORMAL, tk.DISABLED, tk.DISABLED, tk.NORMAL)

    def reset_timer(self):
        self.timer_label.config(text="00:00:00")
        self.time_start = None
        self.set_button_configs(tk.NORMAL, tk.DISABLED, tk.DISABLED, tk.DISABLED)

    def update_timer(self):
        if self.time_start is not None:
            diff_time = time.time() - self.time_start
            hours = int(diff_time/3600)
            mins = int((diff_time%3600)/60)
            seconds = int((diff_time%3600)%60)
            self.timer_label.config(text="{:02d}:{:02d}:{:02d}".format(hours, mins, seconds))
            self.master.after(1000, self.update_timer)

if __name__ == '__main__':
    root = tk.Tk()
    study_timer = StudyTimer(root)
    root.mainloop()
