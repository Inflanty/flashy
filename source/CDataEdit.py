from CDataView import DataView

from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtWidgets import QTabWidget, QTableWidget, QTableWidgetItem, QShortcut
from PyQt5.QtGui import QKeySequence

import logging
import re

class DataEdit(DataView) :
    __editItemsUpdate = []
    __tabList = []

    def makeViewTabs(self):
        _lectures = self.database.getAllLectures()
        if _lectures == [] :
            # If all data has deleted from db
            self.addLecture()
            return
        else :
            for lecture in _lectures :
                self.table = QTableWidget(len(self.database.getLectureIDs(lecture)), self.columnCount)
                self.table.setHorizontalHeaderLabels(self.viewHorHeaders)
                self.push(self.database.getRows(lecture))
                self.tabs.addTab(self.table, "Lecture " + str(lecture))
                _data = [self.tabs, self.table]
                self.__tabList.append(_data)
        self.tabs.setCurrentIndex(QTabWidget.indexOf(self.tabs, self.table))
        self.tabs.currentChanged.connect(self.tabChanged)

    def addLecture(self) :
        super().makeViewTabs()

    def getEdited(self) :
        self.__editItemsUpdate.clear()
        self.__editItemsUpdate.extend(DataView.itemsUpdated)
        for row in self.__editItemsUpdate :
            for index in range(len(DataView.itemsDeleted)) :
                if DataView.itemsDeleted[index] in row[0] :
                    self.__editItemsUpdate.remove(row)
        self.setTabTextSaved()
        DataView.itemsUpdated.clear()
        return self.__editItemsUpdate

    def getNew(self) :
        pass
    
    ## Here we have to return data
    #  TOBEDECIDED :
    #   - how to sign data of Edited
    #   - how to sign data of Deleted
    #   - how to sign data of New
    def pull(self) :
        pass
