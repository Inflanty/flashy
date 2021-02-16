from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import re

# REFACTOR THIS UGLT CLASS UNTIL IS NOT TOO LATE !!!
# THE CONCEPT OF EDITING SINGLE LECTURE SHOULD BE REDESIGN.
# THE MAIN TRACK HERE SHOULD BE TO EDIT ENTIRE DATABASE, WITH OPTION TO EDIT SINGLE LECTURE.
#
# AS IS VISIBLE RIGHT NOW, THE FUNCTIONS WILL BE MULTIPLICATED.
#
# ALSO, SOME FIELDS SHOULDNT BE EDITABLE (id & ???)
#

class DatabaseEdit :
    def __init__(self, database, lectureID = 0) :
        self.database = database
        self.rowDataUpdated = []
        self.lecturesDataUpdated = []
        self.DBColumnCount = 6
        if lectureID == 0 :
            # entire database edit
            self.DBRowCount = self.database.getRecords()
        else :
            self.lectureID = re.findall(r'\d+', lectureID)[0]
            self.DBRowCount = self.database.countRecordsByLecture(self.lectureID)
        self.tabs = QTableWidget(self.DBRowCount, self.DBColumnCount)
        self.tabs.updatesEnabled()

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
        self.setDataFromLecture(self.lectureID)
        self.tabs.resizeColumnsToContents()
        self.tabs.resizeRowsToContents()
        self.MainWindow.setCentralWidget(self.tabs)
        self.tabs.show()

    def databaseEdit(self) :
        if hasattr(self, 'tabs') :
            self.tabs.close()
        self.setDataFromLecture(self.lectureID)
        self.tabs.resizeColumnsToContents()
        self.tabs.resizeRowsToContents()
        self.MainWindow.setCentralWidget(self.tabs)
        self.tabs.show()

    def setDataFromDatabase(self) :
        # TODO: Remove this uglyness
        lectureIDs = self.database.getAllIDs()
        horHeaders = ["ID", "LectureID", "Word", "Sentence", "Transation", "Category"]
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        for _rows in range(self.DBRowCount) :
            _rowsContent = self.database.getRecord(self.lectureID, _rows)
            for _columns in range(len(_rowsContent[0]) - 1) :
                newitem = QTableWidgetItem(str(_rowsContent[0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)
                QtCore.QObject.connect(newitem, QtCore.SIGNAL(itemChanged), self.storeUpdated())

    def setDataFromLecture(self) :
        # TODO: Remove this uglyness
        horHeaders = ["ID", "LectureID", "Word", "Sentence", "Transation", "Category"]
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        for _rows in range(self.database.countRecordsByLecture(self.lectureID)) :
            _rowsContent = self.database.getRecordFromLecture(self.lectureID, _rows)
            for _columns in range(len(_rowsContent[0]) - 1) :
                newitem = QTableWidgetItem(str(_rowsContent[0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)
                QtCore.QObject.connect(newitem, QtCore.SIGNAL(itemChanged), self.storeUpdated())

    def updateDataFromLecture(self) :
        _rowContent = []
        for _rows in range(self.tabs.rowCount()) :
            for _columns in range (self.DBColumnCount) :
                _singleitem = self.tabs.item(_rows, _columns)
                _rowContent.append(_singleitem.text())
            self.lecturesDataUpdated.append(_rowContent)

    # TODO : Test this!!!
    def getChangedRows(self) :
        _rowContent = []
        for _row in self.rowDataUpdated :
            for _columns in range (self.DBColumnCount) :
                _singleitem = self.tabs.item(_row, _columns)
                _rowContent.append(_singleitem.text())
            self.lecturesDataUpdated.append(_rowContent)
        return self.lecturesDataUpdated

    def storeUpdated(self) :
        sender = self.MainWindow.sender()
        item = sender.objectName()
        _row = item.row()
        if not (_row in self.lecturesDataUpdated) and (_row != -1) :
            self.rowDataUpdated.append(_row)
