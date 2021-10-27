from enum import Enum
import sqlite3

class RecordType(Enum):
    Record_None=0
    Record_File=1
    Record_Db=2

filePath = "record.txt" 

def RecordToFile(content):
    with open(filePath, "a") as f:
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
#Record("hh1", RecordType.Record_File)
#Record("hh1", RecordType.Record_Db)