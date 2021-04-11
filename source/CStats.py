import os.path
import numpy as np
from CWord import Word
import logging

class Statistics:
    def __init__(self, databaseName):
        self.name = databaseName
        self.database = Word(databaseName)

    def __del__(self):
        self.database.closeConnection()

    def getDatabase(self) :
        return self.database

    def addProgress(self, fileName):
        if os.path.isfile(fileName):
            self.database.importCSV(fileName)
            self.database.present()
        else :
            logging.warning("File " + str(fileName) + " does not exist!")

    def getRange(self):
        weeks = list(range(0, (self.database.getLectureID() + 1)))
        return weeks

    def getRecordsNumber(self) :
        return self.database.getLastID()

    def showProgress(self):
        lectures = self.database.getLectureID()
        progress = []
        progress.append(0)
        for lectureID in range(1, lectures + 1) :
            if lectureID < 2 :
                progress.append(self.database.getLectureProgress(lectureID))
            else :
                progress.append(self.database.getLectureProgress(lectureID) + progress[lectureID - 1])
        return progress

    def showHeader(self) :
        return self.database.getColumnNames()

    def deleteLecturesRecords(self, lectureID) :
        lecturesIDs = self.database.getLectureIDs(lectureID)
        for row in lecturesIDs :
            logging.info(row[0])
            self.database.deleteRecord(row[0]) 

    def countRecordsByLecture(self, lectureID):
        return len(self.database.getLectureIDs(lectureID))

    def editRecords(self) :
        self.database.exportCSV()

    def getRecordFromLecture(self, lectureID, row) :
        lectureIDs = self.database.getLectureIDs(lectureID)
        return self.database.getRow(lectureIDs + row)

    def getRecordsFromLecture(self, lectureID) :
        _lectureRows = []
        lectureIDs = self.database.getLectureIDs(lectureID)
        for _row in range(len(lectureIDs)) :
            _lectureRows.append(self.database.getRow(lectureIDs[_row]))
        return _lectureRows

    def getRecord(self, row) :
        return self.database.getRow(row)

    def getRecords(self) :
        _lectureRows = []
        for _row in range(1, self.getRecordsNumber()) :
            _lectureRows.append(self.database.getRow(_row))
        return _lectureRows

        return self.database.present()

    def updateRecords(self, data) :
        self.database.updateSection(data)

    def addRecords(self, data) :
        self.database.addSection(data)



if __name__ == "__main__":
    # TEST
    # Take a data from DBgetRecordsFromLecture
    database = Statistics("engdata.db")
    _rowsContent = database.getRecords()
    #print(_rowsContent)
    for _rows in range(1, len(_rowsContent)) :
        for _columns in range(6) :
            print(_rowsContent[_rows][0][_columns])
            pass

