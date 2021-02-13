from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import re

class DatabaseEdit :
    def __init__(self, database, lectureID) :
        self.database = database
        self.lectureID = re.findall(r'\d+', lectureID)[0]
        self.DBColumnCount = 6
        self.DBRowCount = self.database.countRecordsByLecture(self.lectureID)
        self.tabs = QTableWidget(self.DBRowCount, self.DBColumnCount)
        self.tabs.updatesEnabled()
        self.lecturesDataUpdated = []

    def __del__(self):
        pass

    def databaseOpen(self) :
        self.dataPresent()
        self.tabs.resizeColumnsToContents()
        self.tabs.resizeRowsToContents()
        self.tabs.show()

    def dataPresent(self) :
        horHeaders = self.database.showHeader()
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        self.lectureContent = []
        for _rows in range(self.DBRowCount) :
            _rowsContent = self.database.getRecordFromLecture(self.lectureID, _rows)
            self.lectureContent.append(_rowsContent)
            for _columns in range(len(_rowsContent[0]) - 1) :
                newitem = QTableWidgetItem(str(_rowsContent[0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)

    def lectureEdit(self) :
            if hasattr(self, 'tabs') :
                self.tabs.close()
            #self.setData()
            self.setDataFromLecture(self.lectureID)
            self.tabs.resizeColumnsToContents()
            self.tabs.resizeRowsToContents()
            self.MainWindow.setCentralWidget(self.tabs)
            self.tabs.show()

    def setData(self):
        horHeaders = []
        for n, key in enumerate(sorted(self.data.keys())):
            horHeaders.append(key)
            for m, item in enumerate(self.data[key]):
                newitem = QTableWidgetItem(item)
                self.tabs.setItem(m, n, newitem)
        self.tabs.setHorizontalHeaderLabels(horHeaders)

    def setDataFromLecture(self) :
        # TODO: Remove this uglyness
        horHeaders = ["ID", "LectureID", "Word", "Sentence", "Transation", "Category"]
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        for _rows in range(self.database.countRecordsByLecture(self.lectureID)) :
            # TODO: Implement getRecordFromLecture()
            _rowsContent = self.database.getRecordFromLecture(self.lectureID, _rows)
            for _columns in range(len(_rowsContent[0]) - 1) :
                newitem = QTableWidgetItem(str(_rowsContent[0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)

    def updateDataFromLecture(self) :
        _rowContent = []
        for _rows in range(self.tabs.rowCount()) :
            for _columns in range (self.DBColumnCount) :
                _singleitem = self.tabs.item(_rows, _columns)
                _rowContent.append(_singleitem.text())
            self.lecturesDataUpdated.append(_rowContent)