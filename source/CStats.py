import os.path
import matplotlib.pyplot as plt
import numpy as np
from CWord import Word

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
            print("File " + str(fileName) + " does not exist!")

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

    def countRecordsByDate(self, date):
        pass
