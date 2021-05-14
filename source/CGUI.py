import sys, os
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QComboBox, QListWidget
import qdarkstyle
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.examples

from CMainWindow import Ui_MainWindow
from CFileBrowser import Ui_FileBrowser
from CWord import Word
from CSVReader import MyWindow
from CDataEdit import DataEdit
from CDataNew import DataNew
from CDataView import DataView
import logging

# For MainWindow geneate :  pyuic5 -x  .\mainwindow.ui -o ..\..\source\CMainWindow.py

# TODO: If something is not saved, there should be popup window if the user wants to save latest chenges !

class GUI :
    database = "NULL"
    testme = []
    tabs = []
    __active = None
    edit = None
    new = None
    version = "alpha"

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
        self.__setActive(None)
        self.MainWindowApp.quit()
    
    def __setPalette(self) :
        dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
        self.MainWindowApp.setStyleSheet(dark_stylesheet)

    def onTriggerHook(self) :
        self.ui.actionExit.triggered.connect(lambda: self.exit())
        self.ui.actiondatabase.triggered.connect(lambda: self.fileNameOpen())
        self.ui.menuImport.triggered.connect(lambda: self.importData())
        self.ui.actionNew.triggered.connect(lambda: self.createNew())
        self.ui.actionSave.triggered.connect(lambda: self.saveChanges())
        self.ui.actionVersion.triggered.connect(lambda: self.popupHelp())
        self.ui.actionEdit.triggered.connect(lambda: self.dbEdit())

    def fileNameOpen(self) :
        if self.database == "NULL" :   
            currentPath = pathlib.Path().absolute()
            self.fileName = QtWidgets.QFileDialog()
            opentFileName = self.fileName.getOpenFileName(self.fileName, "Open File", str(currentPath), "Database Files (*.db)")
            if str(opentFileName[0]) != "" :
                self.database = Word(str(opentFileName[0]))
                self.plotDatabase()
        else :
            logging.info("Database exist!")

    def dbEdit(self) :
        if self.database != "NULL" :
            if self.__active == self.ui.graphicWidget :
                self.plotDatabaseClose()
            self.edit = DataEdit(self.database)
            self.MainWindow.setCentralWidget(self.edit.tabs)
            self.__setActive(self.edit)

    def saveChanges(self) :
        if issubclass(self.__active.__class__, DataView) :
            _deleted = self.__active.getDeleted()
            if len(_deleted) != 0 :
                self.database.deleteRecords(_deleted)
            else :
                logging.info("Nothing to delete!")
            self.database.insertRecords(self.__active.getEdited())
        else :
            logging.info("Nothing to be saved")

    def createNew(self) :
        if self.__active == self.ui.graphicWidget :
            self.plotDatabaseClose()
        if self.database != "NULL" :
            self.newLecture()
        else :
            self.newDatabase()

    def newLecture(self) :
        if self.__active == self.edit :
            self.edit.addLecture()

    def newLecture_obsolete(self) :
        if self.database != "NULL" :
            self.new = NewSection()
            self.MainWindow.setCentralWidget(self.new.tabs)
            self.__setActive(self.new)
            self.new.tabs.show()

    def newDatabase(self) :
        logging.debug("New database!")
        if self.__newDatabaseFile() :
            self.new = DataNew(self.database)
            self.MainWindow.setCentralWidget(self.new.tabs)
            self.__setActive(self.new)
            self.new.tabs.show()

    def __newDatabaseFile(self) :
        if self.database != "NULL" :
            del self.database
            self.database = "NULL"
        currentPath = pathlib.Path().absolute()
        self.newFile = QtWidgets.QFileDialog()
        opentFileName = self.newFile.getSaveFileName(self.newFile, "Save File", "newDtabase", "Database Files (*.db)")
        if str(opentFileName[0]) != "" :
            logging.info("Created new file")
            self.database = Word(str(opentFileName[0]))
            return True

    def plotDatabase(self) :
        self.ui.graphicWidget = pg.PlotWidget()
        self.MainWindow.setCentralWidget(self.ui.graphicWidget)
        self.__setActive(self.ui.graphicWidget)
        self.ui.graphicWidget.setTitle("Test Plot", color="w", size="8pt")
        self.ui.graphicWidget.setLabel('left', 'Origins', units='')
        self.ui.graphicWidget.setLabel('bottom', 'Weeks', units='')
        self.ui.graphicWidget.plot(self.__databaseGetRange(), self.__databaseShowProgress())

    def __databaseGetRange(self) :
        weeks = list(range(0, (self.database.getLectureID() + 1)))
        return weeks

    def __databaseShowProgress(self) :
        lectures = self.database.getLectureID()
        progress = []
        progress.append(0)
        for lectureID in range(1, lectures + 1) :
            if lectureID < 2 :
                progress.append(self.database.getLectureProgress(lectureID))
            else :
                progress.append(self.database.getLectureProgress(lectureID) + progress[lectureID - 1])
        return progress

    def plotDatabaseUpdate(self) :
        self.ui.graphicWidget.plot(self.__databaseGetRange(), self.__databaseShowProgress())

    def plotDatabaseClose(self) :
        self.ui.graphicWidget.close()

    def plotBarDatabase(self) :
        # plot data: x, y values
        self.ui.graphicWidget = pg.plot()
        self.ui.graphicWidget.setTitle("Test Plot", color="w", size="8pt")
        self.ui.graphicWidget.setLabel('left', 'Origins', units='')
        self.ui.graphicWidget.setLabel('bottom', 'Weeks', units='')
        bg1 = pg.BarGraphItem(x=self.__databaseGetRange(), height=self.__databaseShowProgress(), width=0.2, brush='g')
        self.ui.graphicWidget.addItem(bg1)

    def importData(self) :
        if self.database == "NULL" : 
            logging.warning("Open database first!")
        else :
            currentPath = pathlib.Path().absolute()
            self.fileName = QtWidgets.QFileDialog()
            opentFileName = self.fileName.getOpenFileName(self.fileName, "Import File", str(currentPath), "CSV Files (*.csv)")
            fileName = str(opentFileName[0])
            if os.path.isfile(fileName):
                self.database.importCSV(fileName)
            else :
                logging.warning("File " + str(fileName) + " does not exist!")
            self.plotDatabaseUpdate()

    def popupEdit(self) :
        if self.database == "NULL" : 
            logging.warning("Open database first!")
        else :
            self.listwidget = QListWidget()
            for i in range(1, len(self.__databaseGetRange())) :
                self.listwidget.insertItem(0, "Lecture " + str(i))
            self.listwidget.clicked.connect(self.clicked)
            self.listwidget.show()

    def popupHelp(self) :
        helpWindow = QMessageBox()
        helpWindow.setWindowTitle("Help")
        helpWindow.setText(str(self.version))
        helpWindow.setIcon(QMessageBox.Information)
        helpWindow.setStandardButtons(QMessageBox.Ignore)
        if  self.__active == self.edit :
            helpWindow.setInformativeText("See details, for avilable commands!")
            helpWindow.setDetailedText("No details")
        elif self.__active == self.new :
            helpWindow.setInformativeText("See details, for avilable commands!")
            helpWindow.setDetailedText("- ctrl + R : Add new row\n- ctrl + delete : Delete marked rows")
        else :
            if self.database == "NULL" :
                helpWindow.setInformativeText("The database is not loaded.\nTo load database go to file and see options.")
            else :
                helpWindow.setInformativeText("The database is loaded.\nYou can edit the database and add a new data.")

        helpWindowHndler = helpWindow.exec_()


    def clicked(self) :
        item = self.listwidget.currentItem()
        self.listwidget.close()

    def deleteData(self, lecture) :
        # Add popup to edit (chosse the lecture id from list5 list )
        self.database.deleteLecturesRecords(lecture)
        self.plotDatabaseUpdate()

    def exit(self) :
        logging.info("Exit")
        self.MainWindowApp.quit()
    
    def __setActive(self, active) :
        self.__active = active

if __name__ == "__main__":
    # TEST
    logging.basicConfig(level=logging.NOTSET)
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    Application = GUI()