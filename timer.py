import tkinter
from tkinter.constants import BOTTOM, CENTER, LEFT, RIGHT
#import timer
import datetime
from tkinter import Label, messagebox
from apscheduler.schedulers.background import BackgroundScheduler 
from threading import Timer
import threading

g_workString = "Work: "
g_restString = "Rest: "
g_workTimeMin = 54
g_restTimeMin = 4
g_workTimeSec = g_restTimeSec = 59

def showInfo(title, content):
    messagebox.showinfo(title, content)

def log(info):
    print(info)

def GetCurrentTime():
    now = datetime.datetime.now()
    ts = now.strftime('%H:%M:%S')
    return ts
#update time
def work():
    log("work")
    log(GetCurrentTime())
    showInfo("work", "Should go to work")

def rest():
    log("rest")
    log(GetCurrentTime())
    showInfo("rest", "Should have a rest")

def controler():
    log("controler")

# def doScheduler():
#     myscheduler = BackgroundScheduler()
#     #myscheduler.add_job(work, "interval", seconds=1, id= "work")
#     #myscheduler.add_job(controler, "cron", second=5, id="contorler")
#     myscheduler.start()

def doScheduler():
    restTimer = Timer(55*60, rest)
    restTimer.start()
    restTimer.join()
    workTimer = Timer(5*60, work)
    workTimer.start()
    workTimer.join()

def BackgroundThread():
    while True:
        doScheduler()

def UpdateTime():
    lableTime.config(text= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    if(CountDown()):
        if(lableCountDownName.cget("text") == g_workString):
            rest()
            lableCountDownName.config(text = g_restString)
            lableCountDownMin.config(text = g_restTimeMin)
            lableCountDownSec.config(text = g_restTimeSec)

        elif (lableCountDownName.cget("text") == g_restString):
            work()
            lableCountDownName.config(text = g_workString)
            lableCountDownMin.config(text = g_workTimeMin)
            lableCountDownSec.config(text = g_workTimeSec)
        else:
            log("lableCountDownName is invalid.")
            return

    lableTime.after(1000, UpdateTime)

def CountDown():
    min = int(lableCountDownMin.cget("text"))
    sec = int(lableCountDownSec.cget("text"))
    if (sec!=0):
        sec -= 1
    elif (min != 0):
        min -= 1
        sec = 59
    else :
        return True
    lableCountDownMin.config(text=min)
    lableCountDownSec.config(text=sec)
    return False


main = tkinter.Tk()
main.title("ComeOn")
lableTime = Label(main, font=20)
lableTime.pack(anchor="w",side=BOTTOM)

lableCountDownName= Label(main, text= g_workString, font=60)
lableCountDownName.pack(side=LEFT, anchor="e")
lableCountDownMin = Label(main, text= g_workTimeMin, font=60)
lableCountDownMin.pack(side=LEFT, anchor="w")
lableCountDownColon= Label(main, text=":", font=60)
lableCountDownColon.pack(side=LEFT, anchor="w")
lableCountDownSec= Label(main, text= g_workTimeSec, font=60)
lableCountDownSec.pack(side=LEFT, anchor="w")

UpdateTime()



# bt = threading.Thread(target=BackgroundThread)
# bt.start()
main.pack_propagate(0)
main.mainloop()