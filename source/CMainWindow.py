# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(925, 587)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.formLayout = QtWidgets.QFormLayout(self.centralwidget)
        self.formLayout.setObjectName("formLayout")
        self.graphicWidget = QtWidgets.QWidget(self.centralwidget)
        self.graphicWidget.setObjectName("graphicWidget")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.graphicWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 925, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOpen = QtWidgets.QMenu(self.menuFile)
        self.menuOpen.setObjectName("menuOpen")
        self.menuImport = QtWidgets.QMenu(self.menuFile)
        self.menuImport.setObjectName("menuImport")
        self.menuEdit = QtWidgets.QMenu(self.menuFile)
        self.menuEdit.setObjectName("menuEdit")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionVersion = QtWidgets.QAction(MainWindow)
        self.actionVersion.setObjectName("actionVersion")
        self.actiondatabase = QtWidgets.QAction(MainWindow)
        self.actiondatabase.setObjectName("actiondatabase")
        self.actionCSV_File = QtWidgets.QAction(MainWindow)
        self.actionCSV_File.setShortcutContext(QtCore.Qt.WindowShortcut)
        self.actionCSV_File.setObjectName("actionCSV_File")
        self.actionNew = QtWidgets.QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.action = QtWidgets.QAction(MainWindow)
        self.action.setText("")
        self.action.setObjectName("action")
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.menuOpen.addAction(self.actiondatabase)
        self.menuImport.addAction(self.actionCSV_File)
        self.menuEdit.addAction(self.action)
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.menuOpen.menuAction())
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.menuEdit.menuAction())
        self.menuFile.addAction(self.menuImport.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionVersion)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.menuFile.setStatusTip(_translate("MainWindow", "Manage a file"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOpen.setStatusTip(_translate("MainWindow", "Open a File"))
        self.menuOpen.setTitle(_translate("MainWindow", "Open"))
        self.menuImport.setStatusTip(_translate("MainWindow", "Import a file"))
        self.menuImport.setTitle(_translate("MainWindow", "Import"))
        self.menuEdit.setTitle(_translate("MainWindow", "Edit"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionVersion.setText(_translate("MainWindow", "Version"))
        self.actionVersion.setStatusTip(_translate("MainWindow", "Show APP version"))
        self.actiondatabase.setText(_translate("MainWindow", "Database"))
        self.actiondatabase.setStatusTip(_translate("MainWindow", "Open SQLlite database"))
        self.actiondatabase.setShortcut(_translate("MainWindow", "Ctrl+D"))
        self.actionCSV_File.setText(_translate("MainWindow", "CSV File"))
        self.actionCSV_File.setStatusTip(_translate("MainWindow", "Import CSV file"))
        self.actionCSV_File.setShortcut(_translate("MainWindow", "Ctrl+I"))
        self.actionNew.setText(_translate("MainWindow", "New"))
        self.actionNew.setStatusTip(_translate("MainWindow", "Create a new file"))
        self.actionNew.setShortcut(_translate("MainWindow", "Ctrl+N"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
