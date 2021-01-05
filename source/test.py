import sqlite3
import csv
from tkinter import *
from CStats import Statistics
from CWord import Word

test = Statistics("mem")
test.addProgress("l1.csv")
test.addProgress("l2.csv")
test.addProgress("l3.csv")
#test.saveProgressGraph("progress.png")

#test = Word("mem")
#test.importCSV("l4.csv")
#line = []
#IDs = test.getLectureIDs(4)
#for row in IDs :
#    line.append(test.getSentenceByID(row[0]) + "\t [" + test.getTransByID(row[0]) + "]")
#
#gui = Tk()
#ix = 0
#for row in line :
#    Label(gui, text=row).grid(row=ix)
#    entryName = "E_" + str(ix)
#    entryName = Entry(gui)
#    entryName.grid(row=str(ix), column=1)
#    ix = ix + 1
#mainloop() 
