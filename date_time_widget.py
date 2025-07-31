import tkinter as tk
from datetime import datetime
#import time
#import threading

class DateTimeWidget(tk.Label):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, font=("Arial", 12), fg="white", bg="black", **kwargs)
        self.update_time()

    def update_time(self):
        now = datetime.now()
        formatted = now.strftime("%A, %d/%m/%Y %H:%M:%S")
        self.config(text=formatted)
        self.after(1000, self.update_time)  # Update every second

# Standalone test
if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="black")
    root.title("Date-Time Display")

    dt_widget = DateTimeWidget(root)
    dt_widget.pack(pady=10)

    root.mainloop()
