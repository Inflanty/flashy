import sys
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
#from pyqtgraph import PlotWidget
#import pyqtgraph as pg

from CMainWindow import Ui_MainWindow
from CFileBrowser import Ui_FileBrowser
from CWord import Word

class GUI :
    database = "NULL"

    def __init__(self):
        self.mainWindowApp = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.onTriggerHook()
        MainWindow.show()
        sys.exit(self.mainWindowApp.exec_())

    def __del__(self):
        if self.database != "NULL" :
            self.database.closeConnection()
        else :
            pass

    def onTriggerHook(self) :
        self.ui.actionExit.triggered.connect(lambda: self.exit())
        self.ui.actiondatabase.triggered.connect(lambda: self.fileNameOpen())

    def fileNameOpen(self) :
        currentPath = pathlib.Path().absolute()
        self.fileName = QtWidgets.QFileDialog()
        opentFileName = self.fileName.getOpenFileName(self.fileName, "Open File", str(currentPath), "Database Files (*.db)")
        self.database = Word(str(opentFileName[0]))

    def exit(self) :
        print("Exit")
        self.mainWindowApp.quit()

if __name__ == "__main__":
    # TEST
    Application = GUI()