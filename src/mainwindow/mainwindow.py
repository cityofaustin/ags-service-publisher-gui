# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pughl\Documents\python_projects\ags-service-gui\src\mainwindow\mainwindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(640, 480)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.logWindow = QtGui.QPlainTextEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier New"))
        font.setPointSize(10)
        self.logWindow.setFont(font)
        self.logWindow.setAcceptDrops(False)
        self.logWindow.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logWindow.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.logWindow.setTabChangesFocus(True)
        self.logWindow.setDocumentTitle(_fromUtf8(""))
        self.logWindow.setUndoRedoEnabled(False)
        self.logWindow.setLineWrapMode(QtGui.QPlainTextEdit.NoWrap)
        self.logWindow.setReadOnly(True)
        self.logWindow.setPlainText(_fromUtf8(""))
        self.logWindow.setCursorWidth(0)
        self.logWindow.setTextInteractionFlags(QtCore.Qt.TextSelectableByKeyboard|QtCore.Qt.TextSelectableByMouse)
        self.logWindow.setObjectName(_fromUtf8("logWindow"))
        self.horizontalLayout.addWidget(self.logWindow)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 640, 18))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuReports = QtGui.QMenu(self.menubar)
        self.menuReports.setObjectName(_fromUtf8("menuReports"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuPublishing = QtGui.QMenu(self.menubar)
        self.menuPublishing.setObjectName(_fromUtf8("menuPublishing"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionMXD_Data_Sources_Report = QtGui.QAction(MainWindow)
        self.actionMXD_Data_Sources_Report.setObjectName(_fromUtf8("actionMXD_Data_Sources_Report"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionGetInstallInfo = QtGui.QAction(MainWindow)
        self.actionGetInstallInfo.setObjectName(_fromUtf8("actionGetInstallInfo"))
        self.actionGetExecutablePath = QtGui.QAction(MainWindow)
        self.actionGetExecutablePath.setObjectName(_fromUtf8("actionGetExecutablePath"))
        self.actionPublish_Services = QtGui.QAction(MainWindow)
        self.actionPublish_Services.setObjectName(_fromUtf8("actionPublish_Services"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionTestLogWindow = QtGui.QAction(MainWindow)
        self.actionTestLogWindow.setObjectName(_fromUtf8("actionTestLogWindow"))
        self.menuFile.addAction(self.actionExit)
        self.menuReports.addAction(self.actionMXD_Data_Sources_Report)
        self.menuHelp.addAction(self.actionGetInstallInfo)
        self.menuHelp.addAction(self.actionGetExecutablePath)
        self.menuHelp.addAction(self.actionTestLogWindow)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuPublishing.addAction(self.actionPublish_Services)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuPublishing.menuAction())
        self.menubar.addAction(self.menuReports.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "AGS Service Publisher", None))
        self.menuFile.setTitle(_translate("MainWindow", "&File", None))
        self.menuReports.setTitle(_translate("MainWindow", "Reports", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.menuPublishing.setTitle(_translate("MainWindow", "Publishing", None))
        self.actionMXD_Data_Sources_Report.setText(_translate("MainWindow", "MXD Data Sources Report", None))
        self.actionExit.setText(_translate("MainWindow", "E&xit", None))
        self.actionGetInstallInfo.setText(_translate("MainWindow", "GetInstallInfo", None))
        self.actionGetExecutablePath.setText(_translate("MainWindow", "GetExecutablePath", None))
        self.actionPublish_Services.setText(_translate("MainWindow", "Publish Services", None))
        self.actionAbout.setText(_translate("MainWindow", "About...", None))
        self.actionTestLogWindow.setText(_translate("MainWindow", "TestLogWindow", None))

