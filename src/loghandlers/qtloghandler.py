import logging
from PyQt4 import QtCore


class QtLogHandler(logging.Handler, QtCore.QObject):
    """
    Log handler that emits a Qt signal with the log level and log message for each handled log record.
    """

    messageEmitted = QtCore.pyqtSignal(str, str)

    def __init__(self, level=logging.DEBUG):
        logging.Handler.__init__(self, level)
        QtCore.QObject.__init__(self)

    def emit(self, record):
        if record:
            record_text = self.format(record)
            self.messageEmitted.emit(record.levelname, record_text)
