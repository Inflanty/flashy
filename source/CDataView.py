# CDataView.py

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QShortcut
from PyQt5.QtGui import QKeySequence

import logging
import re

## DataView class to support database view
#  @brief The class can pull data from database and push to View Window (see push)
#         Class use database, directly from Word class from CWord, CStats is probably obsolete
#  @param viewHorHeaders    - Horisontal header to be set in the window
#  @param viewRowTemplate   - Template for a new row in Window
#  @param itemsUpdated      - List with updated items
#  @param itemsDeleted      - List with deleted items
class DataView :
    viewHorHeaders = ['ID', 'SECTION', 'WORD', 'TRANSLATION', 'CATEGORY', 'SENTENCE']
    viewRowTemplate = ['1', '', '', '', 'NULL', '']
    itemsUpdated = []
    itemsDeleted = []
    ## DataView constructor
    #  This class doues not support editing data lecture by lecture
    #  TODO: Each lecture should be in separate tab
    #  NOTE: This class use CWord directly, no need to use CStats
    #  @param database name of the database to edit
    def __init__(self, database) :
        if database == "NULL" or database == None :
            logging.error("Database not exist")
        else :
            self.database = database
            self.maxColumnWidth = 50
            self.columnCount = len(self.viewHorHeaders)
            self.rowsCount = self.database.getLastID()
            if self.rowsCount == 0 :
                self.table = QTableWidget(1, self.columnCount)
            else :
                self.table = QTableWidget(self.rowsCount, self.columnCount)
            self.table.updatesEnabled()
            self.tabs = QTabWidget()
            self.tabs.addTab(self.table, "ALL")
            self.shortcutsNewRow = QShortcut(QKeySequence('Ctrl+r'), self.tabs)
            self.shortcutsNewRow.activated.connect(self.newRow)
            self.shortcutsRmRow = QShortcut(QKeySequence('Ctrl+Del'), self.tabs)
            self.shortcutsRmRow.activated.connect(self.rmRow)
            self.table.setHorizontalHeaderLabels(self.viewHorHeaders)
            self.push()

    ## Class destructor
    def __del__(self) :
        self.table.clear()

    ## Data is push to tabs, ID column is hidden - can not be edited
    #  @brief This metod present the data in tabs
    def push(self) :
        _dataLen = self.database.getLastID()
        _dataRows = self.database.getRows()
        for _rows in range(_dataLen) :
            if _dataLen == 0 :
                _dataRow = self.viewRowTemplate
            else :
                _dataRow = self.__mapDbToViewFormat(_dataRows[_rows])
            for _columns in range(self.columnCount) :
                newitem = QTableWidgetItem(_dataRow[_columns])
                self.table.setItem(_rows, _columns, newitem)
        self.table.hideColumn(0)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellChanged.connect(self.update)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()

    ## Data is pulled from view
    #  @breief This method should be defined by subclass
    def pull(self) :
        pass

    ## If data is updated, the system needs to save the row of data
    #  @brief This metod is a callback for item edit event
    #         the edited datas row will be stored in itemsUpdated
    def update(self) :
        _row = self.selectedRow()
        logging.warning(_row)
        _rowContent = []
        for _columns in range (self.columnCount) :
            _singleitem = self.table.item(_row, _columns).text()
            _rowContent.append(_singleitem)
        self.__updateMyItems(self.__mapViewToDbFormat(_rowContent))

    ## The Row can be addet to the data list, to be saved to database
    #  @brief Such data as ID, SectioID and category is copiet to the new row
    def newRow(self) :
        _row = self.table.rowCount()
        originID = str(int(self.table.item(_row - 1, 0).text()) + 1)
        sectionID = self.table.item(_row - 1, 1).text()
        category = self.table.item(_row - 1, 4).text()
        self.table.insertRow(_row)
        for _columns in range(self.columnCount) :
            if _columns == 0 :  
                newitem = QTableWidgetItem(originID)
            elif _columns == 1 :  
                newitem = QTableWidgetItem(sectionID)
            elif _columns == 4 :
                newitem = QTableWidgetItem(category)
            else :
                newitem = QTableWidgetItem('')
            self.table.setItem(_row, _columns, newitem)
            self.table.resizeRowsToContents()
            self.table.showRow(_row)
        if originID in self.itemsDeleted :
            self.itemsDeleted.remove(originID)
        self.newRowClbk()

    ## Callback
    #  @breief This method should be defined by subclass 
    def newRowClbk(self) :
        pass

    ## Remove row from view and store deleted ID
    def rmRow(self) :
        _row = self.selectedRow() + 1
        if _row != None :
            logging.info('Remove row : ' + str(_row))
            self.table.removeRow(_row - 1)
            if _row not in self.itemsDeleted :
                self.itemsDeleted.append(_row)
        else :
            logging.info('Select row to delete!')

    ## Selected row can be detected
    #  @return Selected row
    def selectedRow(self):
        if self.table.selectionModel().hasSelection():
            row =  self.table.selectionModel().selectedIndexes()[0].row()
            return int(row)

    ## Selected column can be detected
    #  @return Selected column
    def selectedColumn(self):
        column =  self.table.selectionModel().selectedIndexes()[0].column()
        return int(column)

    ## Updated row should be saved in itemsUpdated list
    #  @breif If particular ID already exist, it has to be updated in the same place
    #  @param rowOfItems - Row of items to be updated
    #  @return None if position exist
    def __updateMyItems(self, rowOfItems) :
        _len = len(self.itemsUpdated)
        if _len > 0 :
            for _singleRow in range(_len) :
                if rowOfItems[0] == self.itemsUpdated[_singleRow][0] :
                    self.itemsUpdated[_singleRow] = rowOfItems
                    return
        self.itemsUpdated.append(rowOfItems)

    ## Single row should contain data to be saved
    #  @brief Check if there is a data in the row
    #  @param row - Row to be checked
    #  @return True if row is edited
    def __checkIfEdited(self, row) :
        for _item in row :
            if re.match("^(?![\s\S])", _item) == None :
                return True
        return False

    ## Data format could be different between DB and View
    #  @brief mapp data in row to DB format
    #  @param row - Single row with data to be mapped
    #  @return mapped row
    def __mapViewToDbFormat(self, row) :
        _columnMap = [0, 1, 2, 5, 3, 4]
        _rowMapped = []
        for _item in range(self.columnCount) :
            _rowMapped.append(row[_columnMap[_item]])
        return _rowMapped

    ## Data format could be different between DB and View
    #  @brief mapp data from DB to view format
    #  @param row - Single row with data to be mapped
    #  @return mapped row
    def __mapDbToViewFormat(self, row) :
        _columnMap = [0, 1, 2, 4, 5, 3]
        _rowMapped = []
        for _item in range(self.columnCount) :
            _rowMapped.append(str(row[_columnMap[_item]]))
        return _rowMapped
