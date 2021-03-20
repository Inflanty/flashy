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
            self.DBRowCount = self.database.getRecordsNumber() - 1
        else :
            self.lectureID = re.findall(r'\d+', lectureID)[0]
            self.DBRowCount = self.database.countRecordsByLecture(self.lectureID)
        self.itemsUpdated = []
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
            _rowsContent = self.database.getRecords()
        else :
            _rowsContent = self.database.getRecordsFromLecture(self.lectureID)
        # Every item has own data, pulled from database
        for _rows in range(len(_rowsContent)) :
            # TODO: restrict item ID from editing
            for _columns in range(6) :
                newitem = QTableWidgetItem(str(_rowsContent[_rows][0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)
        self.tabs.cellChanged.connect(self.itemUpdateClbk)
        self.tabs.resizeColumnsToContents()
        self.tabs.resizeRowsToContents()
        self.tabs.show()

    ## Get selected row
    #  @return selected row
    def selectedRow(self):
        if self.tabs.selectionModel().hasSelection():
            row =  self.tabs.selectionModel().selectedIndexes()[0].row()
            return int(row)

    ## Get selected column
    #  @return selected column
    def selectedColumn(self):
        column =  self.tabs.selectionModel().selectedIndexes()[0].column()
        return int(column)

    ## If data is updated, the system needs to save the row of data
    #  @brief This metod is a callback for item edit event
    #         the edited datas row will be stored in itemsUpdated
    def itemUpdateClbk(self) :
        # Do not update the ID
        if (self.selectedColumn() == 0) :
            logging.warning("The element will be not saved")
            return
        _row = self.selectedRow()
        _rowContent = []
        for _columns in range (self.DBColumnCount) :
            _singleitem = self.tabs.item(_row, _columns).text()
            _rowContent.append(_singleitem)
        self.__updateMyItems(_rowContent)

    ## Updated row should be saved in itemsUpdated list,
    #  if particular ID already exist, it has to be updated in the same place
    #  @param rowOfItems row of items to be updated
    #  @return None if position exist
    def __updateMyItems(self, rowOfItems) :
        _len = len(self.itemsUpdated)
        if _len > 0 :
            for _singleRow in range(_len) :
                if (rowOfItems[0] == self.itemsUpdated[_singleRow][0]) :
                    self.itemsUpdated[_singleRow] = rowOfItems
                    return
        self.itemsUpdated.append(rowOfItems)

    ## To allow edited data save, the class should return edited data
    #  @return Edited rows content
    def getEdited(self) :
        return self.itemsUpdated

