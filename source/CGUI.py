import sys
import pathlib
from PyQt5 import QtCore, QtGui, QtWidgets
from CMainWindow import Ui_MainWindow
from CFileBrowser import Ui_FileBrowser

class GUI :
    def __init__(self):
        self.mainWindowApp = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.onTriggerHook()
        MainWindow.show()
        sys.exit(self.mainWindowApp.exec_())

    def __del__(self):
        pass

    def onTriggerHook(self) :
        self.ui.actionExit.triggered.connect(lambda: self.exit())
        self.ui.actiondatabase.triggered.connect(lambda: self.fileName())

    def fileName(self) :
        currentPath = pathlib.Path().absolute()
        self.fileName = QtWidgets.QFileDialog()
        self.fileName.getOpenFileName(self.fileName, "Open File", str(currentPath), "Database Files (*.db)")


    def choseFile(self) :
        #path = pathlib.Path().absolute()
        path = "C:\Windows"
        self.openFileModel = QtWidgets.QFileSystemModel()
        self.openFileModel.setRootPath((QtCore.QDir.rootPath()))

        self.openFile=QtWidgets.QDialog()
        self.openFile.ui=Ui_FileBrowser()
        self.openFile.ui.setupUi(self.openFile)
        self.openFile.ui.treeView.setModel(self.openFileModel)
        self.openFile.ui.treeView.setRootIndex(self.openFileModel.index(path))
        self.openFile.ui.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.openFile.ui.treeView.customContextMenuRequested.connect(self.userContexMenu)
        self.openFile.ui.openButton.clicked.connect(self.printPath)
        self.openFile.ui.cancelButton.clicked.connect(self.choseFileClose)

        self.openFile.exec_()
        self.openFile.show()
        self.choseFileClose()

    def userContexMenu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction("Open")
        open.triggered.connect(self.printPath)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def printPath(self) :
        index = self.openFile.ui.treeView.currentIndex()
        filePath = self.openFileModel.filePath(index)
        print(filePath)
        self.choseFileClose()

    def choseFileClose(self) :
        self.openFile.done(0)

    def exit(self) :
        print("Exit")
        self.mainWindowApp.quit()

if __name__ == "__main__":
    # TEST
    Application = GUI()