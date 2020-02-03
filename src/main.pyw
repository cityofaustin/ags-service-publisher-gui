import multiprocessing
import os
import sys

if not hasattr(sys, 'frozen'):
    import sip

    API_NAMES = ['QDate', 'QDateTime', 'QString', 'QTextStream', 'QTime', 'QUrl', 'QVariant']
    API_VERSION = 2
    for name in API_NAMES:
        sip.setapi(name, API_VERSION)

    os.environ['PATH'] = ';'.join((r'C:\Program Files\ArcGIS\Pro\bin', os.environ['PATH']))
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin')
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\Resources\ArcPy')
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\Resources\ArcToolbox\Scripts')
    sys.path.append(r'C:\Program Files\ArcGIS\Pro\bin\Python\envs\arcgispro-py3\Lib\site-packages')

from PyQt4 import QtGui
from ags_service_publisher.logging_io import setup_logger, setup_console_log_handler

from agsspgui.helpers.pathhelpers import get_app_path
from agsspgui.mainwindow import MainWindow

log = setup_logger(__name__)
main_logger = setup_logger()


def main():
    multiprocessing.freeze_support()
    setup_console_log_handler(main_logger, verbose=True)
    log.debug('Application started: {}'.format(get_app_path()))
    app = QtGui.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
