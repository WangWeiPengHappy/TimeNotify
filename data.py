from contextlib import nullcontext
from enum import Enum
import os
from pickle import NONE
import sqlite3
import datetime
from Util import Util

class RecordType(Enum):
    Record_None=0
    Record_File=1
    Record_Db=2

g_recordFileMaxSize = 20*1024*1024 #20M

class Recorder(object):
    timerFloder = ""
    def __init__(self) -> None:
        self.timerFloder = "/Users/{}/Library/timer/".format(Util.getCurrentUser())
        print("folder is {}".format(self.timerFloder))
        if False == os.path.exists(self.timerFloder):
            os.mkdir(self.timerFloder)
        
    def record(self, content):
        pass

    def getCurrentTime(self):
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d %H:%M:%S')
        return ts

#file part
class FileRecorder(Recorder):
    __recordFileName = "record.txt" 
    __recordFilePath = ""
    __contentId = 0
    __recordFileMaxSize = g_recordFileMaxSize

    def __init__(self) -> None:
        super().__init__()
        self.__recordFilePath = self.timerFloder + self.__recordFileName
        if Util.isDebugMod():
            self.__recordFilePath =  self.__recordFileName
        #if not exist, then create it
        if False == os.path.exists(self.__recordFilePath):
            with open(self.__recordFilePath, "a") as f:
                pass
        self.initContentId()
        print(self.__contentId)
        

    def getCurrentTimeWithoutSpecialChar(self):
        now = datetime.datetime.now()
        ts = now.strftime('%Y-%m-%d-%H-%M-%S')
        return ts

    def initContentId(self):
        lastLine = self.tail(1)
        if lastLine ==None:
            self.__contentId = 0
            return
        lastLine = str(lastLine[0], "UTF-8")
        self.__contentId = int(lastLine[:lastLine.find(".")])

    def tail(self, n, lineSize=-100):
        try:
            with open(self.__recordFilePath, 'rb') as f:
                f.seek(0, 2)
                filesize = f.tell()
                if filesize == 0:
                    return None
                while True:
                    if filesize >= abs(lineSize):
                        f.seek(lineSize, 2)
                        s = f.readlines()
                        if len(s) >= n:
                            return s[-n:]
                        else:
                            lineSize *= 2
                    else:
                        lineSize = -filesize
        except FileNotFoundError:
            print(self.__recordFilePath + " not eixst")
            return None


    '''
    @ content[in]: dictionary type, including key item:str, start:str, end:str, duration:int
    '''
    def record(self, content):
        self.__contentId += 1
        fileContent = "{id}. ".format(id=self.__contentId)
        for item in content:
            fileContent += item
            fileContent += ": "
            fileContent += "{}".format(content[item])
            fileContent += "\t"
        fileContent += "time: "
        fileContent += self.getCurrentTime()
        #print("filecontent===" + fileContent)
        with open(self.__recordFilePath, "a") as f:
            f.write(fileContent)
            f.write("\r\n")

        if(os.path.getsize(self.__recordFilePath) >= self.__recordFileMaxSize):
            tempFileName = os.path.splitext(self.__recordFilePath)
            bakFileName = tempFileName[0]+ "-"+ self.getCurrentTimeWithoutSpecialChar()+tempFileName[1]
            os.rename(self.__recordFilePath)


#db part
class DbRecorder(Recorder):
    __dbName = "record.db"
    __dbPath = ""
    __tableName = "TaskTrace"
    __TaskTraceIndex = 0

    def __init__(self) -> None:
        super().__init__()
        self.__dbPath = self.__timerFloder + self.__dbName
        if Util.isDebugMod():
            self.__dbPath = self.__dbName
        dbConnect = sqlite3.connect(self.__dbPath)
        dbCursor = dbConnect.cursor()
        dbCursor.execute('''create table if not exists TaskTrace(
        Id int primary key not null,
        item text not null,
        start text not null,
        end text not null,
        duration int not null,
        time text
        )''')
        dbConnect.commit()

        dbCursor.execute("select max(Id) from TaskTrace")
        maxId = dbCursor.fetchone()[0]
        if maxId == None:
            self.__TaskTraceIndex = 0
        else:
            self.__TaskTraceIndex = int(maxId)

        print(self.__TaskTraceIndex)
        dbConnect.close()

    '''
        @ content[in]: dictionary type, including key item:str, start:str, end:str, duration:int
    '''
    def record(self, content):
        dbConnect = sqlite3.connect(self.__dbPath)
        dbCursor = dbConnect.cursor()
        self.__TaskTraceIndex+=1
        dbCursor.execute("insert into {tableName} values (:index, :item, :start, :end, :duration, {time})"
        .format(tableName=self.__tableName, time="datetime('now', 'localtime')"), 
        { 
        "index":self.__TaskTraceIndex,
        "item": content["item"],
        "start": content["start"],
        "end": content["end"],
        "duration":content["duration"],
        })
        #to do
        #how to output the argument of dbCursor.execute for log

        dbConnect.commit()
        dbConnect.close()

    def DelOneTask(self, taskItem):
        dbConnect = sqlite3.connect(self.__dbPath)
        dbCursor = dbConnect.cursor()
        dbCursor.execute("delete from table {tableName} where Item={item}".format(tableName=self.__tableName, item=taskItem))
        dbConnect.commit()
        dbConnect.close()

    def ClearTask(self):
        dbConnect = sqlite3.connect(self.__dbPath)
        dbCursor = dbConnect.cursor()
        dbCursor.execute("delete from {tableName}".format(tableName=self.__tableName))
        dbConnect.commit()
        dbConnect.close()

    def DelTaskTable(self):
        dbConnect = sqlite3.connect(self.__dbPath)
        dbCursor = dbConnect.cursor()
        dbCursor.execute("drop table {tableName}".format(tableName=self.__tableName))
        dbConnect.commit()
        dbConnect.close()

#console part
class ConsoleRecorder(Recorder):
    def __init__(self) -> None:
        super().__init__()
    
    def record(self, content):
        print(content)


#interface part
def Record(content, flag):
    global recorder
    if flag == RecordType.Record_File:
        recorder = FileRecorder()
    elif flag == RecordType.Record_Db:
        recorder = DbRecorder()
    elif flag ==  RecordType.Record_None:
        recorder = ConsoleRecorder()
    else:
        print("error flag:", flag)
        return

    recorder.record(content)

'''
TestForData: test for the data.py
'''
def TestForData():
    content = {}
    content["item"] = "test"
    content["start"] = "2022-05-26 1:1:1"
    content["end"] = "2022-05-26 2:2:2"
    content["duration"] = 10
    Record(content, RecordType.Record_None)
    Record(content, RecordType.Record_File)
    Record(content, RecordType.Record_Db)
