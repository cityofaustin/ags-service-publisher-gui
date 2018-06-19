from PySide2 import QtWidgets

from aboutdialog import Ui_AboutDialog


class AboutDialog(QtWidgets.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
