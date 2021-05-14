# CDataView.py

from PyQt5.QtCore import QObject, pyqtSignal, Qt
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
            self.makeView()

    ## Class destructor
    def __del__(self) :
        pass

    # TODO : Check how much sections we have in db and create a tab for each of them
    def makeView(self) :
        self.maxColumnWidth = 50
        self.columnCount = len(self.viewHorHeaders)
        self.tabs = QTabWidget()
        self.shortcutsNewRow = QShortcut(QKeySequence('Ctrl+r'), self.tabs)
        self.shortcutsNewRow.activated.connect(self.newRow)
        self.shortcutsRmRow = QShortcut(QKeySequence('Ctrl+Del'), self.tabs)
        self.shortcutsRmRow.activated.connect(self.rmRow)
        self.makeViewTabs()

    ## Create new tab with empty tables
    #  @brief Tab is created, deta is pushed to the tab
    def makeViewTabs(self) :
        self.rowsCount = 1
        self.table = QTableWidget(self.rowsCount, self.columnCount)
        self.table.updatesEnabled()
        self.table.setHorizontalHeaderLabels(self.viewHorHeaders)
        self.push()
        self.tabs.addTab(self.table, "New")
        self.tabs.setCurrentIndex(QTabWidget.indexOf(self.tabs, self.table))
        self.tabs.currentChanged.connect(self.tabChanged)

    ## Data is push to tabs, ID column is hidden - can not be edited
    #  @brief This metod present the data in tabs.
    #         If data not specified, the tamplate will be taken
    def push(self, data = []) :
        if not data :
            _dataRow = self.viewRowTemplate
            _dataRow[0] = self.database.getLastID() + 1
            for _columns in range(self.columnCount) :
                newitem = QTableWidgetItem(_dataRow[_columns])
                self.table.setItem(0, _columns, newitem)
        else :
            _dataLen = len(data)
            for _rows in range(_dataLen) :
                _dataRow = self.__mapDbToViewFormat(data[_rows])
                for _columns in range(self.columnCount) :
                    newitem = QTableWidgetItem(_dataRow[_columns])
                    self.table.setItem(_rows, _columns, newitem)
        self.table.hideColumn(0)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.cellChanged.connect(self.update)
        self.table.resizeColumnsToContents()
        self.table.resizeRowsToContents()
        self.pushClbk()

    ## Data is push to tabs Callback
    #  @breief This method should be defined by subclass
    def pushClbk(self) :
        pass

    ## Data is pulled from view
    #  @breief This method should be defined by subclass
    def pull(self) :
        _rowContent = []
        for _row in range(self.table.rowCount()) :
            for _columns in range(self.columnCount) :
                _singleitem = self.table.item(_row, _columns).text()
                _rowContent.append(_singleitem)
            self.__updateMyItems(self.__mapViewToDbFormat(_rowContent))

    ## If data is updated, the system needs to save the row of data
    #  @brief This metod is a callback for item edit event
    #         the edited datas row will be stored in itemsUpdated
    #  TODO: If something in current vir=ew is changed, the name of a table should be updated with '*'
    def update(self) :
        _row = self.selectedRow()
        _rowContent = []
        for _columns in range (self.columnCount) :
            _singleitem = self.table.item(_row, _columns).text()
            _rowContent.append(_singleitem)
        self.__updateMyItems(self.__mapViewToDbFormat(_rowContent))
        self.setTabTextUnsaved()


    ## The Row can be addet to the data list, to be saved to database
    #  @brief Such data as ID, SectioID and category is copiet to the new row
    def newRow(self) :
        _row = self.table.rowCount()
        originID = ""
        #originID = str(int(self.table.item(_row - 1, 0).text()) + 1)
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
        _row = self.selectedRow()
        _singleitem = self.table.item(_row, 0).text()
        if _singleitem not in self.itemsDeleted :
            logging.info('Remove row : ' + str(_singleitem))
            self.table.removeRow(_row)
            self.itemsDeleted.append(_singleitem)
        else :
            logging.info('Select row to delete!')

    ## Selected row can be detected
    #  @return Selected row
    def selectedRow(self):
        if self.table.selectionModel().selectedIndexes() != [] :
            row = self.table.selectionModel().selectedIndexes()[0].row()
        else :
            row = 0
        return int(row)

    ## Selected column can be detected
    #  @return Selected column
    def selectedColumn(self):
        if self.table.selectionModel().selectedIndexes() != [] :
            column = self.table.selectionModel().selectedIndexes()[0].column()
        else :
            column = 0
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

    def tabChanged(self, index) :
        self.tabs.setCurrentIndex(index)
        self.table = self.tabs.currentWidget()

    def setTabTextUnsaved(self) :
        _index = self.tabs.currentIndex()
        _text = self.tabs.tabText(_index)
        if "*" not in _text :
            self.tabs.setTabText(_index, _text + " *")
            self.tabs.tabBar().setTabTextColor(_index, Qt.red)

    def setTabTextSaved(self) :
        for index in range(self.tabs.count()) :
            _text = self.tabs.tabText(index)
            if "*" in _text :
                self.tabs.setTabText(index, _text.replace(" *", ""))
                self.tabs.tabBar().setTabTextColor(index, Qt.white)
