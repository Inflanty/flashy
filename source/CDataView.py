# CDataView.py

from PyQt5.QtCore import QObject, pyqtSignal, Qt
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QShortcut
from PyQt5.QtGui import QKeySequence

import logging
import re

## TODO: Before saving the function has to go through all elements in the itemsUpdated (see item ID)
#        and check if there are some fields that was not entered. 
#        only last element could be not enetered so maybe it is better to check only last element, but how ?
#        it maybe could be done by checking current column/row ?
#        but mabe it is not true, maybe not only last element could be not enetede, if user use noiw row shotcut,
#        it might not capture a current item  ?????

class DataView :
    """ DataView class to support database view

    The class can pull data from database and push to View Window (see push)
    This class doues not support editing data lecture by lecture
        TODO: Each lecture should be in separate tab
        NOTE: This class use CWord directly, no need to use CStats

    viewHorHeaders    - Horisontal header to be set in the window
    viewRowTemplate   - Template for a new row in Window
    itemsUpdated      - List with updated items
    itemsDeleted      - List with deleted items
    """
    viewHorHeaders = ['ID', 'SECTION', 'WORD', 'TRANSLATION', 'CATEGORY', 'SENTENCE']
    viewRowTemplate = ['1', '', '', '', 'NULL', '']
    itemsUpdated = []
    itemsDeleted = []

    def __init__(self, database) :
        if database == "NULL" or database == None :
            logging.error("Database not exist")
        else :
            self.database = database
            self.makeView()

    def __del__(self) :
        pass

    def makeView(self) :
        """ TODO : Check how much sections we have in db and create a tab for each of them """
        self.maxColumnWidth = 50
        self.columnCount = len(self.viewHorHeaders)
        self.tabs = QTabWidget()
        self.shortcutsNewRow = QShortcut(QKeySequence('Ctrl+r'), self.tabs)
        self.shortcutsNewRow.activated.connect(self.newRow)
        self.shortcutsRmRow = QShortcut(QKeySequence('Ctrl+Del'), self.tabs)
        self.shortcutsRmRow.activated.connect(self.rmRow)
        self.makeViewTabs()

    def makeViewTabs(self) :
        """Create new tab with empty tables

        Tab is created, deta is pushed to the tab
        """
        self.rowsCount = 1
        self.table = QTableWidget(self.rowsCount, self.columnCount)
        self.table.updatesEnabled()
        self.table.setHorizontalHeaderLabels(self.viewHorHeaders)
        self.push()
        self.tabs.addTab(self.table, "New")
        self.tabs.setCurrentIndex(QTabWidget.indexOf(self.tabs, self.table))
        self.tabs.currentChanged.connect(self.tabChanged)

    def push(self, data = []) :
        """Data is push to tabs, ID column is hidden - can not be edited

        This metod present the data in tabs.
        If data not specified, the tamplate will be taken
        """
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

    def pull(self) :
        """ Data is pulled from view

        This method should be defined by subclass
        """
        _rowContent = []
        for _row in range(self.table.rowCount()) :
            for _columns in range(self.columnCount) :
                _singleitem = self.table.item(_row, _columns).text()
                _rowContent.append(_singleitem)
            self.__updateMyItems(self.__mapViewToDbFormat(_rowContent))

    def update(self) :
        """ If data is updated, the system needs to save the row of data
 
        This metod is a callback for item edit event
        the edited datas row will be stored in itemsUpdated
        TODO: If something in current vir=ew is changed, the name of a table should be updated with '*'
        """
        _row = self.selectedRow()
        _rowContent = []
        for _columns in range (self.columnCount) :
            _singleitem = self.table.item(_row, _columns).text()
            _rowContent.append(_singleitem)
        self.__updateMyItems(self.__mapViewToDbFormat(_rowContent))
        self.setTabTextUnsaved()

    def newRow(self) :
        """ The Row can be addet to the data list, to be saved to database

        Such data as ID, SectioID and category is copiet to the new row
        """
        _row = self.table.rowCount()
        originID = ""
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

    def newRowClbk(self) :
        """ Callback

        This method should be defined by subclass 
        """
        pass

    def rmRow(self) :
        """ Remove row from view and store deleted ID """
        _row = self.selectedRow()
        try :
            _singleitem = self.table.item(_row, 0).text()
        except AttributeError:
            logging.info('Nothing to delete!')
            return
        if _singleitem not in self.itemsDeleted :
            logging.info('Remove row : ' + str(_singleitem))
            self.table.removeRow(_row)
            self.itemsDeleted.append(_singleitem)
            self.setTabTextUnsaved()
        else :
            logging.info('Select row to delete!')

    def selectedRow(self):
        """ Selected row can be detected
        Return selected row
        """
        if self.table.selectionModel().selectedIndexes() != [] :
            row = self.table.selectionModel().selectedIndexes()[0].row()
        else :
            row = 0
        return int(row)

    def selectedColumn(self):
        """ Selected column can be detected

        Return selected column
        """
        if self.table.selectionModel().selectedIndexes() != [] :
            column = self.table.selectionModel().selectedIndexes()[0].column()
        else :
            column = 0
        return int(column)

    def __updateMyItems(self, rowOfItems) :
        """  Updated row should be saved in itemsUpdated list
        
        If particular ID already exist, it has to be updated in the same place
        rowOfItems - Row of items to be updated
        Return None if position exist
        """
        _len = len(self.itemsUpdated)
        if _len > 0 :
            for _singleRow in range(_len) :
                if rowOfItems[0] == self.itemsUpdated[_singleRow][0] :
                    self.itemsUpdated[_singleRow] = rowOfItems
                    return
        self.itemsUpdated.append(rowOfItems)

    def __checkIfEdited(self, row) :
        """ Single row should contain data to be saved
        
        Check if there is a data in the row
        row - Row to be checked
        Return True if row is edited
        """
        for _item in row :
            if re.match("^(?![\s\S])", _item) == None :
                return True
        return False

    def __mapViewToDbFormat(self, row) :
        """ Data format could be different between DB and View

        mapp data in row to DB format
        row - Single row with data to be mapped
        Return mapped row
        """
        _columnMap = [0, 1, 2, 5, 3, 4]
        _rowMapped = []
        for _item in range(self.columnCount) :
            _rowMapped.append(row[_columnMap[_item]])
        return _rowMapped

    def __mapDbToViewFormat(self, row) :
        """ Data format could be different between DB and View
 
        mapp data from DB to view format
        row - Single row with data to be mapped
        Return mapped row
        """
        _columnMap = [0, 1, 2, 4, 5, 3]
        _rowMapped = []
        for _item in range(self.columnCount) :
            _rowMapped.append(str(row[_columnMap[_item]]))
        return _rowMapped

    def tabChanged(self, index) :
        """ Keep track og current tabs and table

        index - take the index of current tab 
        """
        self.tabs.setCurrentIndex(index)
        self.table = self.tabs.currentWidget()

    def setTabTextUnsaved(self) :
        """ Tab name should be changed if contains unsaved changes """
        _index = self.tabs.currentIndex()
        _text = self.tabs.tabText(_index)
        if "*" not in _text :
            self.tabs.setTabText(_index, _text + " *")
            self.tabs.tabBar().setTabTextColor(_index, Qt.red)

    def setTabTextSaved(self) :
        """ Tab name should be as default if changes were saved """
        for index in range(self.tabs.count()) :
            _text = self.tabs.tabText(index)
            if "*" in _text :
                self.tabs.setTabText(index, _text.replace(" *", ""))
                self.tabs.tabBar().setTabTextColor(index, Qt.white)

    def getDeleted(self) :
        """ Get all deleted data """
        _deleted = []
        _deleted.extend(self.itemsDeleted)
        self.itemsDeleted.clear()
        return _deleted
