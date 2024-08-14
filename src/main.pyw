import logging
import multiprocessing
import sys

from PyQt6 import QtWidgets
from ags_service_publisher.logging_io import setup_logger, setup_console_log_handler

from agsspgui.helpers.pathhelpers import get_app_path
from agsspgui.mainwindow import MainWindow

log = setup_logger(__name__)

if __name__ == '__main__':
    multiprocessing.freeze_support()
    if not hasattr(sys, 'frozen'):
        setup_console_log_handler(logging.root, verbose=True)
    log.debug('Application started: {}'.format(get_app_path()))
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
