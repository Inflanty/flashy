from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import re
import logging

## Documentation for DatabaseEdit class
#
#  The class provide all neccessary functionalities for database edit
class DatabaseEdit :
    ## DatabaseEdit constructor
    #  @param database name of the database to edit
    #  @param lectureID lecture to edit, if 0 entire db will be edited
    def __init__(self, database, lectureID = 0) :
        self.database = database
        self.DBColumnCount = 6
        if lectureID == 0 :
            # entire database edit
            self.lectureID = lectureID
            self.DBRowCount = self.database.getRecords()
        else :
            self.lectureID = re.findall(r'\d+', lectureID)[0]
            self.DBRowCount = self.database.countRecordsByLecture(self.lectureID)
        self.rowDataUpdated = []
        # We do not want to have origin ID and link from db
        self.tabs = QTableWidget(self.DBRowCount, self.DBColumnCount)
        self.tabs.updatesEnabled()

    ## DatabaseEdit destructor
    def __del__(self) :
        self.lectureID = 0

    ## Data is pull from db and push to tabs
    #  @brief This metod present the data in tabs
    def dataPresent(self) :
        horHeaders = self.database.showHeader()
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        # The data can be edited as a blob of data
        #  OR in lecture mode
        if (self.lectureID == 0) :
            _rowsContent = self.database.getRecordsFromDatabase()
        else :
            _rowsContent = self.database.getRecordsFromLecture(self.lectureID)
        # Every item has own data, pulled from database
        for _rows in range(self.DBRowCount) :
            # TODO: restrict item ID from editing
            for _columns in range(6) :
                newitem = QTableWidgetItem(str(_rowsContent[_rows][0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)
        self.tabs.cellChanged.connect(self.itemUpdateClbk)
        self.tabs.resizeColumnsToContents()
        self.tabs.resizeRowsToContents()
        self.tabs.show()

    def selectedRow(self):
        if self.tabs.selectionModel().hasSelection():
            row =  self.tabs.selectionModel().selectedIndexes()[0].row()
            return int(row)

    def selectedColumn(self):
        column =  self.tabs.selectionModel().selectedIndexes()[0].column()
        return int(column)

    ## I data is updated, the system needs to save the row of data
    #  @brief This metod is a callback for item edit event
    #         the edited datas row will be stored in rowDataUpdated
    #  TODO: Can't update the same row twice
    def itemUpdateClbk(self) :
        # Do not update the ID
        if (self.selectedColumn() == 0) :
            logging.warning("The element will be not saved")
            return
        item = self.tabs.selectedItems()[0]
        _row = self.selectedRow()
        _rowContent = []
        for _columns in range (self.DBColumnCount) :
            _singleitem = self.tabs.item(_row, _columns)
            _singleitemcontent = _singleitem.text()
            # Break if the element already exist
            if (_columns == 0) :
                for _singleRow in range(len(self.rowDataUpdated)) :
                    if (_singleitemcontent in self.rowDataUpdated[_singleRow]) :
                        logging.warning("Can not add, " + _singleitemcontent + ". Already exist!")
                        return
            _rowContent.append(_singleitemcontent)
        self.rowDataUpdated.append(_rowContent)
        logging.warning(self.rowDataUpdated)

    ## To allow edited data save, the class should return edited data
    #  @return Edited rows content
    def getEdited(self) :
        return self.rowDataUpdated
