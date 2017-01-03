import multiprocessing
import sys

import sip

API_NAMES = ['QDate', 'QDateTime', 'QString', 'QTextStream', 'QTime', 'QUrl', 'QVariant']
API_VERSION = 2
for name in API_NAMES:
    sip.setapi(name, API_VERSION)

from PyQt4 import QtGui
from ags_service_publisher.logging_io import setup_logger, setup_console_log_handler
from ags_service_publisher.runner import root_logger

from helpers.pathhelpers import get_app_path
from mainwindow import MainWindow

log = setup_logger(__name__)


def main():
    multiprocessing.freeze_support()
    setup_console_log_handler(root_logger, verbose=True)
    log.debug('Application started: {}'.format(get_app_path()))
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
