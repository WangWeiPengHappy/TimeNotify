
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
from Util import Util
import sys

g_workString = "Work: "
g_restString = "Rest: "
g_workTimeMin = 54
g_restTimeMin = 4
g_workTimeSec = g_restTimeSec = 59
g_btnStart = "start"
g_btnPause = "pause"
g_btnStop = "stop"
g_isStart = False
class TaskInfo(object):
    __startTime = ""
    __endTime = ""
    __TaskItem = ""
    __workTimeMinStart=0
    __workTimeSecStart=0
    __workTimeMinEnd=0
    __workTimeSecEnd=0
    def __init__(self) -> None:
        pass

    def setStartTime(self, startTime:str)->None:
        self.__startTime = startTime
    
    def setWorkTimeStart(self, minStart:int, secStart:int)->None:
        self.__workTimeMinStart = minStart
        self.__workTimeSecStart = secStart
    
    def setWorkTimeEnd(self, minEnd:int, secEnd:int)->None:
        self.__workTimeMinEnd = minEnd
        self.__workTimeSecEnd = secEnd

    def setEndTime(self, endTime:str)->None:
        self.__endTime = endTime
    
    def setTaskItem(self, taskItem:str)->None:
        self.__TaskItem = taskItem
    
    def calcDuration(self)->int:
        durationMin = self.__workTimeMinStart - self.__workTimeMinEnd
        durationSec = self.__workTimeSecStart - self.__workTimeSecEnd
        return durationMin*60+durationSec
    
    def getTaskInfo(self)->dict:
        content = {}
        content["item"] = self.__TaskItem
        content["start"] = self.__startTime
        content["end"] = self.__endTime
        content["duration"] = self.calcDuration()
        return content

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
    global g_taskInfo
    global g_isDebugMod
    lableTime.config(text= datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    #print(entryItemContent.get())

    if(g_isStart and CountDown()):
        if(lableCountDownName.cget("text") == g_workString):
            #Record(getCurrentTimeWithYear()+ " "+ entryItemContent.get(), RecordType.Record_File)
            g_taskInfo.setEndTime(getCurrentTimeWithYear())
            print("End==>"+str(lableCountDownMin.cget("text"))+":"+str(lableCountDownSec.cget("text")))
            g_taskInfo.setWorkTimeEnd(lableCountDownMin.cget("text"), lableCountDownSec.cget("text"))
            recordType = RecordType.Record_None if g_isDebugMod else RecordType.Record_Db
            Record(g_taskInfo.getTaskInfo(), recordType)
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
            g_taskInfo.setTaskItem(entryItemContent.get())
            g_taskInfo.setStartTime(getCurrentTimeWithYear())
            print("start==>"+str(lableCountDownMin.cget("text"))+":"+str(lableCountDownSec.cget("text")))
            g_taskInfo.setWorkTimeStart(lableCountDownMin.cget("text"), lableCountDownSec.cget("text"))
        else:
            log("lableCountDownName is invalid.")
            return
    lableTime.after(1000, UpdateTime)

def CountDown():
    min = lableCountDownMin.cget("text")
    sec = lableCountDownSec.cget("text")
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
    global g_taskInfo
    global g_isDebugMod
    if(btnText == g_btnStart):
        #start
        if(len(entryItemContent.get()) == 0):
            showInfo("warning", "Item is empty and input")
            return
        entryItemContent.config(state="disable")
        BtnStart.config(text=g_btnPause)   
        g_isStart = True
        g_taskInfo.setTaskItem(entryItemContent.get())
        g_taskInfo.setStartTime(getCurrentTimeWithYear())
        g_taskInfo.setWorkTimeStart(int(lableCountDownMin.cget("text")), int(lableCountDownSec.cget("text")))

    elif(btnText == g_btnPause):
        #pause
        g_isStart = False
        BtnStart.config(text=g_btnStart)
        entryItemContent.config(state="normal")
    elif(btnText == g_btnStop):
        #stop
        if g_isStart and lableCountDownName.cget("text") == g_workString:
            g_taskInfo.setEndTime(getCurrentTimeWithYear())
            g_taskInfo.setWorkTimeEnd(int(lableCountDownMin.cget("text")), int(lableCountDownSec.cget("text")))
            recordType = RecordType.Record_None if g_isDebugMod else RecordType.Record_Db
            Record(g_taskInfo.getTaskInfo(), recordType)
        g_isStart = False
        BtnStart.config(text=g_btnStart)
        lableCountDownName.config(text = g_workString)
        lableCountDownMin.config(text = g_workTimeMin)
        lableCountDownSec.config(text = g_workTimeSec)
        entryItemContent.config(state="normal")

    else:
        print("The text is invalid: ", btnText)
    return

if len(sys.argv) > 1:
    if str(sys.argv[1]) == "debug":
        Util.enableDebugMode()

main = tkinter.Tk()
main.title("ComeOnGuys")
#set windows on top most
main.wm_attributes("-topmost", 1) 
#it will pop windows when click the icon on docker
main.createcommand('tk::mac::ReopenApplication', main.deiconify)
#Debug mod
global g_isDebugMod
g_isDebugMod = Util.isDebugMod()
if g_isDebugMod:
    g_workTimeMin = 0#54
    g_restTimeMin = 0#4
    g_workTimeSec = g_restTimeSec = 5#59
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
global g_taskInfo 
g_taskInfo = TaskInfo()
UpdateTime()



# bt = threading.Thread(target=BackgroundThread)
# bt.start()
main.pack_propagate(0)
main.mainloop()