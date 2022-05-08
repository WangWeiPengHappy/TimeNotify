
from asyncio.streams import start_server
import tkinter
from tkinter.constants import BOTTOM, CENTER, LEFT, RIGHT, TOP
#import timer
import datetime
from tkinter import Button, Entry, Frame, Label, Toplevel, messagebox
from apscheduler.schedulers.background import BackgroundScheduler 
from threading import Timer
from data import Record
from data import RecordType

g_workString = "Work: "
g_restString = "Rest: "
g_workTimeMin = 54
g_restTimeMin = 4
g_workTimeSec = g_restTimeSec = 59
g_btnStart = "start"
g_btnPause = "pause"
g_btnStop = "stop"
g_isStart = False
def showInfo(title, content):
    messagebox.showinfo(title, content, parent=main)#parent=main for messagebox is topmost

def log(info):
    print(info)

def getCurrentTimeWithYear():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d %H:%M:%S')
    return ts

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
    global g_isStart
    lableTime.config(text= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #print(entryItemContent.get())

    if(g_isStart and CountDown()):
        if(lableCountDownName.cget("text") == g_workString):
            Record(getCurrentTimeWithYear()+ " "+ entryItemContent.get(), RecordType.Record_File)
            entryItemContent.config(state="normal")
            rest()
            lableCountDownName.config(text = g_restString)
            lableCountDownMin.config(text = g_restTimeMin)
            lableCountDownSec.config(text = g_restTimeSec)
        elif (lableCountDownName.cget("text") == g_restString):
            #Record("Rest", RecordType.Record_File)
            work()
            entryItemContent.config(state="disabled")
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

# def topWin():
#     tp = Toplevel(main)
#     tp.attributes("-topmost", True)

def HandleBtnEvent(btnText):
    global g_isStart
    if(btnText == g_btnStart):
        #start
        if(len(entryItemContent.get()) == 0):
            showInfo("warning", "Item is empty and input")
            return
        entryItemContent.config(state="disable")
        BtnStart.config(text=g_btnPause)   
        g_isStart = True
    elif(btnText == g_btnPause):
        #pause
        g_isStart = False
        BtnStart.config(text=g_btnStart)
        entryItemContent.config(state="normal")
    elif(btnText == g_btnStop):
        #stop
        g_isStart = False
        BtnStart.config(text=g_btnStart)
        lableCountDownName.config(text = g_workString)
        lableCountDownMin.config(text = g_workTimeMin)
        lableCountDownSec.config(text = g_workTimeSec)
        entryItemContent.config(state="normal")

    else:
        print("The text is invalid: ", btnText)
    return

main = tkinter.Tk()
main.title("ComeOnGuys")
#set windows on top most
main.wm_attributes("-topmost", 1) 
#it will pop windows when click the icon on docker
main.createcommand('tk::mac::ReopenApplication', main.deiconify)

#窗口布局
framePlaceholderTop = Frame(main)
framePlaceholderTop.config(height= int(0.25* main.winfo_height()))
framePlaceholderTop.pack(side=TOP, anchor="w")
frameItem = tkinter.Frame(main)
frameItem.pack(side= TOP, anchor="w")
ItemName = "Item"
lableItemName = Label(frameItem, text= ItemName, font=60)
lableItemName.pack(side= LEFT, anchor="w")
entryItemContent = Entry(frameItem)
entryItemContent.pack(side= LEFT, anchor="w")

frameCountDown = tkinter.Frame(main)
frameCountDown.pack(side=TOP, anchor="w")
lableCountDownName= Label(frameCountDown, text= g_workString, font=60)
lableCountDownName.pack(anchor = "s", side = LEFT)
lableCountDownMin = Label(frameCountDown, text= g_workTimeMin, font=60)
lableCountDownMin.pack(side=LEFT, anchor="w")
lableCountDownColon= Label(frameCountDown, text=":", font=60)
lableCountDownColon.pack(side=LEFT, anchor="w")
lableCountDownSec= Label(frameCountDown, text= g_workTimeSec, font=60)
lableCountDownSec.pack(side=LEFT, anchor="w")
frameControl = Frame(main)
frameControl.pack(side=TOP, anchor="w")
BtnStart = Button(frameControl, text= g_btnStart, font=60)
BtnStart.config(command= lambda:HandleBtnEvent(BtnStart.cget("text")))
BtnStart.pack(side=LEFT)
BtnStop = Button(frameControl, text= g_btnStop, font=60)
BtnStop.config(command= lambda:HandleBtnEvent(BtnStop.cget("text")))
BtnStop.pack(side=LEFT)

frameTime = Frame(main)
frameTime.pack(side=BOTTOM, anchor="e")
lableTime = Label(frameTime, font=20)
lableTime.pack(side=LEFT, anchor="w")
# framePlaceholderBottom = Frame(main)
# framePlaceholderBottom.config(height= int(0.25* main.winfo_height()))
# framePlaceholderBottom.pack(side=BOTTOM, anchor="w")
UpdateTime()



# bt = threading.Thread(target=BackgroundThread)
# bt.start()
main.pack_propagate(0)
main.mainloop()