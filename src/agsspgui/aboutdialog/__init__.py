from PyQt4 import QtGui

from .aboutdialog_ui import Ui_AboutDialog


class AboutDialog(QtGui.QDialog, Ui_AboutDialog):
    def __init__(self, parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setupUi(self)
