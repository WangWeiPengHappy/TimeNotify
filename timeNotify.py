import tkinter
from tkinter import messagebox
import time

# top = tkinter.Tk()
# top.mainloop()
tkinter.messagebox.showinfo("Info", "Start")
while True:
    time.sleep(60*60)
    tkinter.messagebox.showinfo("Info", "Timeout")