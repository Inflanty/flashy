from CDataView import DataView

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QShortcut
from PyQt5.QtGui import QKeySequence

import logging
import re

class DataNew(DataView) :

    def getEdited(self) :
        self.pull()
        self.setTabTextSaved()
        # Check the difference between __newItemsUpdate AND DataView.itemsUpdated
        # if some elements are different, we should take newest version
        return DataView.itemsUpdated

    ## Remove row from view and store deleted ID
    def rmRow(self) :
        _row = self.selectedRow() + 1
        if _row != None :
            logging.info('Remove row : ' + str(_row))
            self.table.removeRow(_row - 1)
        else :
            logging.info('Select row to delete!')
