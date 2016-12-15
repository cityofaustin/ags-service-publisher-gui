# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pughl\Documents\python_projects\ags-service-gui\src\publishdialog\publishdialog.ui'
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

class Ui_PublishDialog(object):
    def setupUi(self, PublishDialog):
        PublishDialog.setObjectName(_fromUtf8("PublishDialog"))
        PublishDialog.setWindowTitle(_fromUtf8("Publish Services"))
        PublishDialog.setSizeGripEnabled(True)
        PublishDialog.setModal(True)
        self.gridLayout = QtGui.QGridLayout(PublishDialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.splitter = QtGui.QSplitter(PublishDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.widget = QtGui.QWidget(self.splitter)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.widget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.servicesTree = QtGui.QTreeWidget(self.widget)
        self.servicesTree.setAlternatingRowColors(True)
        self.servicesTree.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.servicesTree.setColumnCount(2)
        self.servicesTree.setObjectName(_fromUtf8("servicesTree"))
        self.servicesTree.header().setMinimumSectionSize(100)
        self.servicesTree.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.servicesTree)
        self.widget1 = QtGui.QWidget(self.splitter)
        self.widget1.setObjectName(_fromUtf8("widget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(self.widget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.instancesTree = QtGui.QTreeWidget(self.widget1)
        self.instancesTree.setAlternatingRowColors(True)
        self.instancesTree.setSelectionMode(QtGui.QAbstractItemView.NoSelection)
        self.instancesTree.setColumnCount(2)
        self.instancesTree.setObjectName(_fromUtf8("instancesTree"))
        self.instancesTree.header().setMinimumSectionSize(100)
        self.instancesTree.header().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.instancesTree)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(PublishDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(PublishDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), PublishDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), PublishDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PublishDialog)

    def retranslateUi(self, PublishDialog):
        self.label.setText(_translate("PublishDialog", "Services to publish:", None))
        self.servicesTree.headerItem().setText(0, _translate("PublishDialog", "Name", None))
        self.servicesTree.headerItem().setText(1, _translate("PublishDialog", "Type", None))
        self.label_2.setText(_translate("PublishDialog", "Instances to publish to:", None))
        self.instancesTree.headerItem().setText(0, _translate("PublishDialog", "Name", None))
        self.instancesTree.headerItem().setText(1, _translate("PublishDialog", "Type", None))

