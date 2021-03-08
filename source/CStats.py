import os.path
import matplotlib.pyplot as plt
import numpy as np
from CWord import Word
import logging

class Statistics:
    def __init__(self, databaseName):
        self.name = databaseName
        self.database = Word(databaseName)

    def __del__(self):
        pass

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

    def showProgressGraph(self):
        x = [0,1,2,3]
        y = self.showProgress()
        plt.plot(x, y, 'bo')
        # plot approximated data
        plt.title("English progress : " + self.name)
        plt.grid(True)
        plt.winter()
        plt.show()

    def saveProgressGraph(self, fileName):
        x = [0,1,2,3]
        y = self.showProgress()
        plt.plot(x, y, 'bo')
        # plot approximated data
        plt.title("English progress : " + self.name)
        plt.grid(True)
        plt.winter()
        plt.savefig(fileName, bbox_inches='tight')        

    def countRecordsByLecture(self, lectureID):
        return len(self.database.getLectureIDs(lectureID))

    def editRecords(self) :
        self.database.exportCSV()

    def getRecordFromLecture(self, lectureID, row) :
        lectureIDs = self.database.getLectureIDs(lectureID)
        return self.database.getRow(lectureIDs[0][0] + row)

    def getRecordsFromLecture(self, lectureID) :
        _lectureRows = []
        lectureIDs = self.database.getLectureIDs(lectureID)
        for _row in range(self.countRecordsByLecture(lectureID)) :
            _lectureRows.append(self.database.getRow(lectureIDs[0][0] + _row))
            # logging.debug(self.database.getRow(lectureIDs[0][0] + _row))
        return _lectureRows

    def getRecord(self, row) :
        return self.database.show(row)

    def getRecords(self) :
        return self.database.show('ALL')

    def updateRecords(self, data) :
        self.database.updateSection(data)



if __name__ == "__main__":
    # TEST
    # Take a data from DBgetRecordsFromLecture
    database = Statistics("words.db")
    data = database.showProgress()
    logging.info(data)
