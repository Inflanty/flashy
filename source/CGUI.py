import sys
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QComboBox, QListWidget
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.examples

from CMainWindow import Ui_MainWindow
from CFileBrowser import Ui_FileBrowser
from CStats import Statistics
from CSVReader import MyWindow
from CDatabaseEdit import DatabaseEdit


# For MainWindow geneate :  pyuic5 -x  .\mainwindow.ui -o ..\..\source\CMainWindow.py

class GUI :
    database = "NULL"
    testme = []
    tabs = []

    def __init__(self):
        self.MainWindowApp = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.onTriggerHook()
        self.MainWindowApp.lastWindowClosed.connect(self.exit)
        #pyqtgraph.examples.run()
        self.MainWindow.show()
        sys.exit(self.MainWindowApp.exec_())

    def __del__(self):
        print("Bye")
        if self.database != "NULL" :
            self.database.closeConnection()
            self.database = "NULL"
        else :
            pass
        self.MainWindowApp.quit()

    def onTriggerHook(self) :
        self.ui.actionExit.triggered.connect(lambda: self.exit())
        self.ui.actiondatabase.triggered.connect(lambda: self.fileNameOpen())
        self.ui.menuImport.triggered.connect(lambda: self.importData())
        self.ui.actionNew.triggered.connect(lambda: self.newLecture())
        self.ui.actionSave.triggered.connect(lambda: self.saveDatabase())

    def fileNameOpen(self) :
        if self.database == "NULL" :   
            currentPath = pathlib.Path().absolute()
            self.fileName = QtWidgets.QFileDialog()
            opentFileName = self.fileName.getOpenFileName(self.fileName, "Open File", str(currentPath), "Database Files (*.db)")
            self.database = Statistics(str(opentFileName[0]))
            self.plotDatabase()
            self.createActionOnEdit(self.database.getRange())
        else :
            print("Database exist!")

    def createActionOnEdit(self, lectureList) :
        # First edit existing action
        self.ui.name = []
        self.ui.name.append(self.ui.action)
        self.ui.name[0] = self.ui.action
        if len(lectureList) > 2 :
            # Edit ALL
            self.ui.name[0].setObjectName("ALL")
            self.ui.menuEdit.addAction(self.ui.name[0])
            self.ui.name[0].setText(QtCore.QCoreApplication.translate("MainWindow", "ALL"))
            self.ui.name[0].triggered.connect(self.dbEdit)
            # Lectures edit
            for i in range(1, len(lectureList) + 1) :
                self.ui.name.append(QtWidgets.QAction(self.MainWindow))
                self.ui.name[i].setObjectName("Lecture " + str(i))
                self.ui.menuEdit.addAction(self.ui.name[i - 1])
                self.ui.name[i].setText(QtCore.QCoreApplication.translate("MainWindow", "Lecture " + str(i)))
                self.ui.name[i].triggered.connect(self.lectureEdit)

    # TODO: entire db edit
    def dbEdit(self) :
        if self.database != "NULL" :
            print("To be implemented")

    def lectureEdit(self) :
        if self.database != "NULL" :
            sender = self.MainWindow.sender()
            lectureID = sender.objectName()
            if(self.ui.graphicWidget.isActiveWindow()) :
                self.plotDatabaseClose()
            self.data = DatabaseEdit(self.database, lectureID)
            self.MainWindow.setCentralWidget(self.data.tabs)
            self.data.databaseOpen()

    def saveDatabase(self) :
        if self.database != "NULL" :
            self.data.updateDataFromLecture()
            self.database.updateLecture(self.data.lecturesDataUpdated)

    # TODO: TEST IT!
    def saveChanges(self) :
        if self.database != "NULL" :
            self.database.updateLecture(self.data.getChangedRows())

    def newLecture(self) :
        print("New File..!")

    def plotDatabase(self) :
        self.ui.graphicWidget = pg.PlotWidget()
        self.MainWindow.setCentralWidget(self.ui.graphicWidget)
        self.ui.graphicWidget.setTitle("Test Plot", color="w", size="8pt")
        self.ui.graphicWidget.setLabel('left', 'Origins', units='')
        self.ui.graphicWidget.setLabel('bottom', 'Weeks', units='')
        self.ui.graphicWidget.plot(self.database.getRange(), self.database.showProgress())

    def plotDatabaseUpdate(self) :
        self.ui.graphicWidget.plot(self.database.getRange(), self.database.showProgress())

    def plotDatabaseClose(self) :
        self.ui.graphicWidget.close()

    def plotBarDatabase(self) :
        # plot data: x, y values
        self.ui.graphicWidget = pg.plot()
        self.ui.graphicWidget.setTitle("Test Plot", color="w", size="8pt")
        self.ui.graphicWidget.setLabel('left', 'Origins', units='')
        self.ui.graphicWidget.setLabel('bottom', 'Weeks', units='')
        bg1 = pg.BarGraphItem(x=self.database.getRange(), height=self.database.showProgress(), width=0.2, brush='g')
        self.ui.graphicWidget.addItem(bg1)

    def importData(self) :
        if self.database == "NULL" : 
            print("Open database first!")
        else :
            currentPath = pathlib.Path().absolute()
            self.fileName = QtWidgets.QFileDialog()
            opentFileName = self.fileName.getOpenFileName(self.fileName, "Import File", str(currentPath), "CSV Files (*.csv)")
            self.database.addProgress(str(opentFileName[0]))
            self.plotDatabaseUpdate()

    def popupEdit(self) :
        if self.database == "NULL" : 
            print("Open database first!")
        else :
            self.listwidget = QListWidget()
            for i in range(1, len(self.database.getRange())) :
                self.listwidget.insertItem(0, "Lecture " + str(i))
            self.listwidget.clicked.connect(self.clicked)
            self.listwidget.show()

    def clicked(self) :
        item = self.listwidget.currentItem()
        print(item.text())
        self.listwidget.close()

    def deleteData(self, lecture) :
        # Add popup to edit (chosse the lecture id from list5 list )
        self.database.deleteLecturesRecords(lecture)
        self.plotDatabaseUpdate()

    def exit(self) :
        print("Exit")
        #self.MainWindowApp.aboutToQuit.connect(self.MainWindow.closeEvent())
        self.MainWindowApp.quit()

if __name__ == "__main__":
    # TEST
    Application = GUI()