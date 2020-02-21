import logging
from PyQt4 import QtCore


class QtLogHandler(logging.Handler):
    """
    Log handler that emits a Qt signal with the log level and log message for each handled log record.
    """

    def __init__(self, *args, **kwargs):
        super(QtLogHandler, self).__init__(*args, **kwargs)
        self.emitter = QtLogMessageEmitter()
        self.messageEmitted = self.emitter.messageEmitted

    def emit(self, record):
        if record:
            record_text = self.format(record)
            self.emitter.emit_message(record.levelno, record_text)


class QtLogMessageEmitter(QtCore.QObject):
    """
    QObject that emits a Qt signal with the log level and log message for each handled log record.
    """

    messageEmitted = QtCore.pyqtSignal(int, str)

    def __init__(self):
        super(QtLogMessageEmitter, self).__init__()

    def emit_message(self, level, record_text):
        self.messageEmitted.emit(level, record_text)
