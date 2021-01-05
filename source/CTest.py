from tkinter import *
from CWord import Word

class Test:
    def __init__(self, databaseName) :
        self.name = databaseName
        self.database = Word(databaseName)
        self.gui = Tk() 

    def __del__(self) :
        pass

    def getSentences(self, chapter) :
        IDs = self.database.getLectureIDs(chapter)
        for index in range(IDs) :
            sentences = self.database.getSentenceByID(IDs[index])

    def makeTest(self) :
        sentences = self.getSentences(1)
        for index in range(sentences) :
            Label(self.gui, text=sentences[index]).grid(row=index)
            entryName = "E_" + index
            entryName = Entry(self.gui)
            entryName.grid(row=index, column=1)
        mainloop()