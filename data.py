from enum import Enum
import os
import sqlite3
import datetime

class RecordType(Enum):
    Record_None=0
    Record_File=1
    Record_Db=2

timerFloder = "/Users/eric_wang/Library/timer/"
recordFileName = "record.txt" 
recordFilePath = timerFloder + recordFileName
g_recordFileMaxSize = 20*1024*1024 #20M

def getCurrentTime():
    now = datetime.datetime.now()
    ts = now.strftime('%Y-%m-%d-%H-%M-%S')
    return ts

def RecordToFile(content):
    if False == os.path.exists(timerFloder):
        os.mkdir(timerFloder)

    if(os.path.getsize(recordFilePath) >= g_recordFileMaxSize):
        tempFileName = os.path.splitext(recordFilePath)
        bakFileName = tempFileName[0]+ "-"+getCurrentTime()+tempFileName[1]
        os.rename(recordFilePath,bakFileName)

    with open(recordFilePath, "a") as f:
        f.write(content)
        f.write("\r\n")

def RecordToDb(content):
    print("not support")
    # con = sqlite3.connect("record.db")
    # c = con.cursor()
    # #check table exist
    # #insert 
    # con.commit()
    # con.close()


def Record(content, flag):
    if flag == RecordType.Record_File:
        RecordToFile(content)
    elif flag == RecordType.Record_Db:
        RecordToDb(content)
    elif flag ==  RecordType.Record_None:
        print(content)
    else:
        print("error flag:", flag)

#for test
#Record("test Record_File", RecordType.Record_File)
#Record("test Record_Db", RecordType.Record_Db)