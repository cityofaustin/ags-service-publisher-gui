import sys, multiprocessing

from ags_service_publisher.runner import root_logger
from ags_service_publisher.mplog import open_queue
from ags_service_publisher.logging_io import setup_logger, setup_console_log_handler
from helpers.pathhelpers import get_app_path

from PyQt4 import QtGui

from mainwindow import MainWindow

log = setup_logger(__name__)


def main():
    multiprocessing.freeze_support()
    with open_queue() as log_queue:
        setup_console_log_handler(root_logger, verbose=True)
        log.debug('Application started: {}'.format(get_app_path()))
        app = QtGui.QApplication(sys.argv)
        main_window = MainWindow(None, log_queue)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == '__main__':
    main()
