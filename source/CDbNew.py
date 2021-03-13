from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QShortcut
import logging

class NewSection :
    def __init__(self) :
        self.columnCount = 4
        self.maxColumnWidth = 50
        self.tabs = QTableWidget(1, self.columnCount)
        self.tabs.updatesEnabled()
        self.shortcutsNewRow = QShortcut(QKeySequence('Ctrl+r'), self.tabs)
        self.shortcutsNewRow.activated.connect(self.setNewRow)
        self.shortcutsRmRow = QShortcut(QKeySequence('Ctrl+Del'), self.tabs)
        self.shortcutsRmRow.activated.connect(self.rmSelectedRow)
        self.setNewSection()

    def __del__(self) :
        self.tabs.clear()

    def setNewSection(self) :
        horHeaders = ['Section ID', 'Word', 'Translation', 'Sentence']
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        for _columns in range(self.columnCount) :
            newitem = QTableWidgetItem('')
            self.tabs.setItem(0, _columns, newitem)
        self.tabs.horizontalHeader().setStretchLastSection(True)
        # Nothing in rows, minimal value
        self.tabs.resizeRowsToContents()

    def getNewSection(self) :
        _rowContent = []
        _rowsContent = []
        for _rows in range(self.tabs.rowCount()) :
            for _columns in range(self.columnCount) :
                _singleitem = self.tabs.item(_rows, _columns).text()
                _rowContent.append(_singleitem)
            _rowsContent.append(_singleitem)
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