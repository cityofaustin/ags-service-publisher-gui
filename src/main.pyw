import sys, multiprocessing

from ags_service_publisher.runner import root_logger
from ags_service_publisher.logging_io import setup_logger, setup_console_log_handler
from helpers.pathhelpers import get_app_path

from PyQt4 import QtGui

from mainwindow import MainWindow

log = setup_logger(__name__)


def main():
    setup_console_log_handler(root_logger, verbose=True)
    log.debug('Application started: {}'.format(get_app_path()))
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow(None)
    main_window.show()
    app.exec_()


if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
