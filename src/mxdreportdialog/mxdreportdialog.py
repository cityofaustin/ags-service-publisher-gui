# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pughl\Documents\python_projects\ags-service-gui\src\mxdreportdialog\mxdreportdialog.ui'
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

class Ui_MXDReportDialog(object):
    def setupUi(self, MXDReportDialog):
        MXDReportDialog.setObjectName(_fromUtf8("MXDReportDialog"))
        MXDReportDialog.resize(544, 416)
        MXDReportDialog.setWindowTitle(_fromUtf8("MXD Data Sources Report"))
        MXDReportDialog.setSizeGripEnabled(True)
        MXDReportDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(MXDReportDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(MXDReportDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.layoutWidget = QtGui.QWidget(self.splitter)
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.servicesTree = QtGui.QTreeWidget(self.layoutWidget)
        self.servicesTree.setAlternatingRowColors(True)
        self.servicesTree.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.servicesTree.setColumnCount(2)
        self.servicesTree.setObjectName(_fromUtf8("servicesTree"))
        self.servicesTree.header().setMinimumSectionSize(100)
        self.servicesTree.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.servicesTree)
        self.layoutWidget1 = QtGui.QWidget(self.splitter)
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.envsTree = QtGui.QTreeWidget(self.layoutWidget1)
        self.envsTree.setAlternatingRowColors(True)
        self.envsTree.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.envsTree.setColumnCount(2)
        self.envsTree.setObjectName(_fromUtf8("envsTree"))
        self.envsTree.header().setMinimumSectionSize(100)
        self.envsTree.header().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.envsTree)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(MXDReportDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 2, 0, 1, 1)
        self.widget = QtGui.QWidget(MXDReportDialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.widget)
        self.horizontalLayout_4.setMargin(0)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_4.addWidget(self.label_3)
        self.outputfileLineEdit = QtGui.QLineEdit(self.widget)
        self.outputfileLineEdit.setObjectName(_fromUtf8("outputfileLineEdit"))
        self.horizontalLayout_4.addWidget(self.outputfileLineEdit)
        self.outputfileButton = QtGui.QPushButton(self.widget)
        self.outputfileButton.setObjectName(_fromUtf8("outputfileButton"))
        self.horizontalLayout_4.addWidget(self.outputfileButton)
        self.gridLayout.addWidget(self.widget, 1, 0, 1, 1)

        self.retranslateUi(MXDReportDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), MXDReportDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), MXDReportDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(MXDReportDialog)

    def retranslateUi(self, MXDReportDialog):
        self.label.setText(_translate("MXDReportDialog", "Services to report:", None))
        self.servicesTree.headerItem().setText(0, _translate("MXDReportDialog", "Name", None))
        self.servicesTree.headerItem().setText(1, _translate("MXDReportDialog", "Type", None))
        self.label_2.setText(_translate("MXDReportDialog", "Environments to report:", None))
        self.envsTree.headerItem().setText(0, _translate("MXDReportDialog", "Name", None))
        self.envsTree.headerItem().setText(1, _translate("MXDReportDialog", "Type", None))
        self.label_3.setText(_translate("MXDReportDialog", "Output file:", None))
        self.outputfileButton.setText(_translate("MXDReportDialog", "...", None))

