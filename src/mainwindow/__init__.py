import os

from PyQt4 import QtCore, QtGui

from mainwindow import Ui_MainWindow
from aboutdialog import AboutDialog
from resultdialog import ResultDialog

from ags_service_publisher import runner
from ags_service_publisher.logging_io import setup_logger
from helpers.pathhelpers import get_app_path
from helpers.texthelpers import escape_html
from helpers.arcpyhelpers import get_install_info
from workers.subprocessworkerpool import SubProcessWorkerPool
from workers.subprocessworker import SubProcessWorker
from loghandlers.qtloghandler import QtLogHandler

log = setup_logger(__name__)


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, log_queue=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionPublish_Services.triggered.connect(self.publish_services)
        self.actionMXD_Data_Sources_Report.triggered.connect(self.mxd_data_sources_report)
        self.actionGetInstallInfo.triggered.connect(self.get_install_info)
        self.actionGetExecutablePath.triggered.connect(self.get_executable_path)
        self.actionAbout.triggered.connect(self.about)
        self.actionTestLogWindow.triggered.connect(self.test_log_window)
        self.actionExit.triggered.connect(self.close)

        self.worker_pool = SubProcessWorkerPool()

        self.log_queue = log_queue

        self.log_handler = QtLogHandler()
        self.log_handler.messageEmitted.connect(self.log_message)
        runner.root_logger.addHandler(self.log_handler)

    def closeEvent(self, event):
        log.debug('closeEvent triggered')
        result = QtGui.QMessageBox.question(
            self,
            'Exit - AGS Service Publisher',
            'Are you sure you want to exit?',
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No
        )

        if result == QtGui.QMessageBox.Yes:
            self.worker_pool.quit_all_threads()
            log.debug('Exiting application!')
            event.accept()
        else:
            log.debug('Ignoring closeEvent')
            event.ignore()

    def publish_services(self):
        configs = ['LP_Testing']
        included_services = ['Boundaries', 'PlanningCadastre']
        worker = SubProcessWorker(
            target=runner.run_batch_publishing_job,
            kwargs={
                'included_configs': configs,
                'included_services': included_services,
                'warn_on_validation_errors': True,
                'verbose': True
            },
            log_queue=self.log_queue
        )

        worker_id = self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker_id)

    def mxd_data_sources_report(self):
        configs = ['LP_Testing']
        included_services = ['Boundaries', 'PlanningCadastre']
        report_name = 'test.csv'
        report_path = os.path.join(r'C:\Users\pughl\Documents\python_projects\ags-service-reports', report_name)

        worker = SubProcessWorker(
            target=runner.run_mxd_data_sources_report,
            kwargs={
                'included_configs': configs,
                'included_services': included_services,
                'output_filename': report_path,
                'warn_on_validation_errors': True,
                'verbose': True
            },
            log_queue=self.log_queue
        )

        worker_id = self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker_id)

    def get_install_info(self):
        result_dialog = ResultDialog(self)

        try:
            result_dialog.setWindowTitle('ArcGIS Install Info - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Information)
            result_dialog.setText(str(get_install_info()))
        except StandardError as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.exec_()

    def get_executable_path(self):
        result_dialog = ResultDialog(self)

        try:
            result_dialog.setWindowTitle('Executable Path - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Information)
            result_dialog.setText(get_app_path())
        except StandardError as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.exec_()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def test_log_window(self):
        self.log_info_message('info')
        self.log_debug_message('debug')
        self.log_success_message('success')
        self.log_warning_message('warning')
        self.log_error_message('error')

    def log_message(self, level, message):
        if level == 'INFO':
            self.log_info_message(message)
        elif level == 'DEBUG':
            self.log_debug_message(message)
        elif level == 'WARNING':
            self.log_warning_message(message)
        elif level == 'ERROR':
            self.log_error_message(message)
        else:
            raise RuntimeError('Unknown message level: {}'.format(level))

    def log_info_message(self, message):
        self.logWindow.appendHtml('<font color="black">{}</font>'.format(escape_html(message)))

    def log_debug_message(self, message):
        self.logWindow.appendHtml('<font color="gray">{}</font>'.format(escape_html(message)))

    def log_warning_message(self, message):
        self.logWindow.appendHtml('<font color="blue">{}</font>'.format(escape_html(message)))

    def log_success_message(self, message):
        self.logWindow.appendHtml('<font color="green">{}</font>'.format(escape_html(message)))

    def log_error_message(self, message):
        self.logWindow.appendHtml('<font color="red">{}</font>'.format(escape_html(message)))
