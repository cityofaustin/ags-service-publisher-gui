from PySide2 import QtWidgets


class ResultDialog(QtWidgets.QMessageBox):
    def __init__(self, parent=None):
        QtWidgets.QMessageBox.__init__(self, parent)
