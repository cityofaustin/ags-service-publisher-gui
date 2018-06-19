# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\pughl\Documents\python_projects\ags-service-gui\src\publishdialog\publishdialog.ui',
# licensing of 'C:\Users\pughl\Documents\python_projects\ags-service-gui\src\publishdialog\publishdialog.ui' applies.
#
# Created: Tue Jun 19 18:25:33 2018
#      by: pyside2-uic  running on PySide2 5.11.0a1.dev1528378291
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_PublishDialog(object):
    def setupUi(self, PublishDialog):
        PublishDialog.setObjectName("PublishDialog")
        PublishDialog.resize(544, 416)
        PublishDialog.setWindowTitle("Publish Services")
        PublishDialog.setSizeGripEnabled(True)
        PublishDialog.setModal(True)
        self.gridLayout = QtWidgets.QGridLayout(PublishDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.splitter = QtWidgets.QSplitter(PublishDialog)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.servicesTree = QtWidgets.QTreeWidget(self.layoutWidget)
        self.servicesTree.setAlternatingRowColors(True)
        self.servicesTree.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.servicesTree.setColumnCount(2)
        self.servicesTree.setObjectName("servicesTree")
        self.servicesTree.header().setMinimumSectionSize(100)
        self.servicesTree.header().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.servicesTree)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.instancesTree = QtWidgets.QTreeWidget(self.layoutWidget1)
        self.instancesTree.setAlternatingRowColors(True)
        self.instancesTree.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.instancesTree.setColumnCount(2)
        self.instancesTree.setObjectName("instancesTree")
        self.instancesTree.header().setMinimumSectionSize(100)
        self.instancesTree.header().setStretchLastSection(False)
        self.verticalLayout_2.addWidget(self.instancesTree)
        self.gridLayout.addWidget(self.splitter, 0, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(PublishDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(PublishDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), PublishDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), PublishDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(PublishDialog)

    def retranslateUi(self, PublishDialog):
        self.label.setText(QtWidgets.QApplication.translate("PublishDialog", "Services to publish:", None, -1))
        self.servicesTree.headerItem().setText(0, QtWidgets.QApplication.translate("PublishDialog", "Name", None, -1))
        self.servicesTree.headerItem().setText(1, QtWidgets.QApplication.translate("PublishDialog", "Type", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("PublishDialog", "Instances to publish to:", None, -1))
        self.instancesTree.headerItem().setText(0, QtWidgets.QApplication.translate("PublishDialog", "Name", None, -1))
        self.instancesTree.headerItem().setText(1, QtWidgets.QApplication.translate("PublishDialog", "Type", None, -1))

