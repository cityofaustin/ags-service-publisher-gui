from PyQt4 import QtGui


class ResultDialog(QtGui.QMessageBox):
    def __init__(self, parent=None):
        QtGui.QMessageBox.__init__(self, parent)
