from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem
import re

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
            self.DBRowCount = self.database.getRecords()
        else :
            self.lectureID = re.findall(r'\d+', lectureID)[0]
            self.DBRowCount = self.database.countRecordsByLecture(self.lectureID)
        self.rowDataUpdated = []
        # We do not want to have origin ID and link from db
        self.tabs = QTableWidget(self.DBRowCount, self.DBColumnCount)
        self.tabs.updatesEnabled()
        self.lectureID = lectureID

    ## DatabaseEdit destructor
    def __del__(slef) :
        self.lectureID = 0

    ## Data is pull from db and push to tabs
    #  @brief This metod present the data in tabs
    def dataPresent(self) :
        horHeaders = self.database.showHeader()
        self.tabs.setHorizontalHeaderLabels(horHeaders)
        # The data can be edited in lecture mode
        #  OR as a whole blob of data
        if (self.lectureID == 0) :
            _rowsContent = self.database.getRecordsFromDatabase()
        else :
            _rowsContent = self.database.getRecordsFromLecture(self.lectureID)
        # Every item has own data, pulled from database
        for _rows in range(self.DBRowCount) :
            # TODO: restrict item ID from editing
            for _columns in range(len(_rowsContent[0]) - 1) :
                newitem = QTableWidgetItem(str(_rowsContent[0][_columns]))
                self.tabs.setItem(_rows, _columns, newitem)
                QtCore.QObject.connect(newitem, QtCore.SIGNAL(itemChanged), self.itemUpdateClbk())
        # The structure needs to be adjusted
        # TODO: Fix this
        self.tabs.resizeColumnsToContents()
        self.tabs.resizeRowsToContents()
        self.tabs.show()

    ## I data is updated, the system needs to save the row of data
    #  @brief This metod is a callback for item edit event
    #         the edited datas row will be stored in rowDataUpdated
    def itemUpdateClbk(self) :
        sender = self.MainWindow.sender()
        item = sender.objectName()
        _row = item.row()
        _rowContent = []
        # If item is not exist the row() return -1
        if not (_row in self.rowDataUpdated) and (_row != -1) :
            # Save entire row here to not bother later with searching for ID
            for _columns in range (self.DBColumnCount) :
                _singleitem = self.tabs.item(_row, _columns)
                _rowContent.append(_singleitem.text())
            self.rowDataUpdated.append(_rowContent)

    ## To allow edited data save, the class should return edited data
    #  @return Edited rows content
    def getEdited(self) :
        return self.rowDataUpdated
