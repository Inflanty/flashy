import sys
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
import pyqtgraph.examples

from CMainWindow import Ui_MainWindow
from CFileBrowser import Ui_FileBrowser
from CStats import Statistics

class GUI :
    database = "NULL"

    def __init__(self):
        self.MainWindowApp = QtWidgets.QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.onTriggerHook()
        self.MainWindowApp.lastWindowClosed.connect(self.exit)
        self.MainWindow.show()
        sys.exit(self.MainWindowApp.exec_())

    def __del__(self):
        print("Bye")
        if self.database != "NULL" :
            self.database.closeConnection()
        else :
            pass
        self.MainWindowApp.quit()

    def onTriggerHook(self) :
        self.ui.actionExit.triggered.connect(lambda: self.exit())
        self.ui.actiondatabase.triggered.connect(lambda: self.fileNameOpen())

    def fileNameOpen(self) :
        currentPath = pathlib.Path().absolute()
        self.fileName = QtWidgets.QFileDialog()
        opentFileName = self.fileName.getOpenFileName(self.fileName, "Open File", str(currentPath), "Database Files (*.db)")
        self.database = Statistics(str(opentFileName[0]))
        self.plotDatabase()

    def plotDatabase(self) :
        self.ui.graphicWidget = pg.PlotWidget()
        self.MainWindow.setCentralWidget(self.ui.graphicWidget)
        self.ui.graphicWidget.setTitle("Test Plot", color="w", size="8pt")
        self.ui.graphicWidget.setLabel('left', 'Origins', units='')
        self.ui.graphicWidget.setLabel('bottom', 'Weeks', units='')
        # plot data: x, y values
        self.ui.graphicWidget.plot(self.database.getRange(), self.database.showProgress())

    def exit(self) :
        print("Exit")
        #self.MainWindowApp.aboutToQuit.connect(self.MainWindow.closeEvent())
        self.MainWindowApp.quit()

if __name__ == "__main__":
    # TEST
    Application = GUI()