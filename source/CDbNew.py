from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QShortcut
import logging, re

## Documentation for NewSection class
#
#  The class provide all neccessary functionalities for add new section into databse
class NewSection :
    ## NewSection Class constructor
    def __init__(self) :
        self.columnCount = 5
        self.maxColumnWidth = 50
        self.tabs = QTableWidget(1, self.columnCount)
        self.tabs.updatesEnabled()
        self.shortcutsNewRow = QShortcut(QKeySequence('Ctrl+r'), self.tabs)
        self.shortcutsNewRow.activated.connect(self.setNewRow)
        self.shortcutsRmRow = QShortcut(QKeySequence('Ctrl+Del'), self.tabs)
        self.shortcutsRmRow.activated.connect(self.rmSelectedRow)
        self.createNewSection()

    ## NewSection Class destructor
    def __del__(self) :
        self.tabs.clear()

    ## As a main class functionality, we provide here an option to create new section,
    #  as a section data, the user can refer to a data from part. Lecture
    #  TODO: ADD option to write category
    def createNewSection(self) :
        _horHeaders = ['SECTION', 'WORD', 'TRANSLATION', 'CATEGORY', 'SENTENCE']
        self.tabs.setHorizontalHeaderLabels(_horHeaders)
        for _columns in range(self.columnCount) :
            if _columns == 3 :
                newitem = QTableWidgetItem('NULL')
            else :
                newitem = QTableWidgetItem('')
            self.tabs.setItem(0, _columns, newitem)
        self.tabs.horizontalHeader().setStretchLastSection(True)
        # Nothing in rows, minimal value
        self.tabs.resizeRowsToContents()

    def getEdited(self) :
        _rowContent = []
        _rowsContent = []
        for _rows in range(self.tabs.rowCount()) :
            _rowContent = []
            for _columns in range(self.columnCount) :
                _singleitem = self.tabs.item(_rows, _columns).text()
                _rowContent.append(_singleitem)
            if self.__checkIfEdited(_rowContent) :
                _rowsContent.append(self.__mapRowToDbFormat(_rowContent))
        return _rowsContent

    def setNewRow(self) :
        _row = self.tabs.rowCount()
        # Store previouse ID
        sectionID = self.tabs.item(_row - 1, 0).text()
        logging.info('New row : ' + str(_row))
        self.tabs.insertRow(_row)
        self.tabs.resizeRowsToContents()
        for _columns in range(self.columnCount) :
            if _columns == 0 :   
                newitem = QTableWidgetItem(sectionID)
            else :
                newitem = QTableWidgetItem('')
            self.tabs.setItem(_row, _columns, newitem)
            self.tabs.showRow(_row)

    def rmSelectedRow(self) :
        _row = self.selectedRow()
        if _row != None :
            logging.info('Remove row : ' + str(_row + 1))
            self.tabs.removeRow(_row)
        else :
            logging.info('Relect row to delete!')

    def selectedRow(self):
        if self.tabs.selectionModel().hasSelection():
            row =  self.tabs.selectionModel().selectedIndexes()[0].row()
            return int(row)

    def selectedColumn(self):
        column =  self.tabs.selectionModel().selectedIndexes()[0].column()
        return int(column)

    def __checkIfEdited(self, row) :
        for _item in row :
            if re.match("^(?![\s\S])", _item) == None :
                return True
        return False

    def __mapRowToDbFormat(self, row) :
        # Columns in the class are mixed compare to db
        _columnMap = [0, 1, 4, 2, 3]
        _rowMapped = []
        for _item in range(len(row)) :
            _rowMapped.append(row[_columnMap[_item]])
        return _rowMapped
