import sys
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QComboBox, QListWidget
import qdarkstyle
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.examples

from CMainWindow import Ui_MainWindow
from CFileBrowser import Ui_FileBrowser
from CStats import Statistics
from CSVReader import MyWindow
from CDbEdit import DatabaseEdit
from CDbNew import NewSection
import logging

# For MainWindow geneate :  pyuic5 -x  .\mainwindow.ui -o ..\..\source\CMainWindow.py

class GUI :
    database = "NULL"
    testme = []
    tabs = []

    def __init__(self):
        self.MainWindowApp = QtWidgets.QApplication(sys.argv)
        self.__setPalette()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.onTriggerHook()
        self.MainWindowApp.lastWindowClosed.connect(self.exit)
        self.MainWindow.show()
        sys.exit(self.MainWindowApp.exec_())

    def __del__(self):
        logging.info("Bye")
        if self.database != "NULL" :
            self.database.closeConnection()
            self.database = "NULL"
        else :
            pass
        self.MainWindowApp.quit()
    
    def __setPalette(self) :
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.MainWindowApp.setStyleSheet(dark_stylesheet)

    def onTriggerHook(self) :
        self.ui.actionExit.triggered.connect(lambda: self.exit())
        self.ui.actiondatabase.triggered.connect(lambda: self.fileNameOpen())
        self.ui.menuImport.triggered.connect(lambda: self.importData())
        self.ui.actionNew.triggered.connect(lambda: self.newLecture())
        self.ui.actionSave.triggered.connect(lambda: self.saveChanges())

    def fileNameOpen(self) :
        if self.database == "NULL" :   
            currentPath = pathlib.Path().absolute()
            self.fileName = QtWidgets.QFileDialog()
            opentFileName = self.fileName.getOpenFileName(self.fileName, "Open File", str(currentPath), "Database Files (*.db)")
            self.database = Statistics(str(opentFileName[0]))
            self.plotDatabase()
            self.createActionOnEdit(self.database.getRange())
        else :
            logging.info("Database exist!")

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
                self.ui.name[i].triggered.connect(self.dbEdit)

    def dbEdit(self) :
        if self.database != "NULL" :
            sender = self.MainWindow.sender()
            lectureID = sender.objectName()
            if self.ui.graphicWidget.isActiveWindow() :
                self.plotDatabaseClose()
            if lectureID == "ALL" :
                lectureID = 0
            self.edit = DatabaseEdit(self.database, lectureID)
            self.MainWindow.setCentralWidget(self.edit.tabs)
            self.edit.dataPresent()

    def saveChanges(self) :
        if self.database != "NULL" :
            self.database.updateRecords(self.edit.getEdited())

    def newLecture(self) :
        if self.database != "NULL" :
            if self.ui.graphicWidget.isActiveWindow() :
                self.plotDatabaseClose()
            self.new = NewSection()
            self.MainWindow.setCentralWidget(self.new.tabs)
            self.new.tabs.show()

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
            logging.warning("Open database first!")
        else :
            currentPath = pathlib.Path().absolute()
            self.fileName = QtWidgets.QFileDialog()
            opentFileName = self.fileName.getOpenFileName(self.fileName, "Import File", str(currentPath), "CSV Files (*.csv)")
            self.database.addProgress(str(opentFileName[0]))
            self.plotDatabaseUpdate()

    def popupEdit(self) :
        if self.database == "NULL" : 
            logging.warning("Open database first!")
        else :
            self.listwidget = QListWidget()
            for i in range(1, len(self.database.getRange())) :
                self.listwidget.insertItem(0, "Lecture " + str(i))
            self.listwidget.clicked.connect(self.clicked)
            self.listwidget.show()

    def clicked(self) :
        item = self.listwidget.currentItem()
        self.listwidget.close()

    def deleteData(self, lecture) :
        # Add popup to edit (chosse the lecture id from list5 list )
        self.database.deleteLecturesRecords(lecture)
        self.plotDatabaseUpdate()

    def exit(self) :
        logging.info("Exit")
        #self.MainWindowApp.aboutToQuit.connect(self.MainWindow.closeEvent())
        self.MainWindowApp.quit()

if __name__ == "__main__":
    # TEST
    logging.basicConfig(level=logging.NOTSET)
    Application = GUI()

#https://stackoverflow.com/questions/48256772/dark-theme-for-qt-widgets

#from PyQt5.QtWidgets import QApplication
#from PyQt5.QtGui import QPalette, QColor
#
#app = QApplication([])
## Force the style to be the same on all OSs:
#app.setStyle("Fusion")
#
## Now use a palette to switch to dark colors:
#palette = QPalette()
#palette.setColor(QPalette.Window, QColor(53, 53, 53))
#palette.setColor(QPalette.WindowText, Qt.white)
#palette.setColor(QPalette.Base, QColor(25, 25, 25))
#palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
#palette.setColor(QPalette.ToolTipBase, Qt.black)
#palette.setColor(QPalette.ToolTipText, Qt.white)
#palette.setColor(QPalette.Text, Qt.white)
#palette.setColor(QPalette.Button, QColor(53, 53, 53))
#palette.setColor(QPalette.ButtonText, Qt.white)
#palette.setColor(QPalette.BrightText, Qt.red)
#palette.setColor(QPalette.Link, QColor(42, 130, 218))
#palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
#palette.setColor(QPalette.HighlightedText, Qt.black)
#app.setPalette(palette)