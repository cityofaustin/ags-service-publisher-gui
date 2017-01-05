import os

from PyQt4 import QtGui
from ags_service_publisher import runner
from ags_service_publisher.logging_io import setup_logger

from aboutdialog import AboutDialog
from helpers.arcpyhelpers import get_install_info
from helpers.pathhelpers import get_app_path
from helpers.texthelpers import escape_html
from loghandlers.qtloghandler import QtLogHandler
from mainwindow import Ui_MainWindow
from publishdialog import PublishDialog
from mxdreportdialog import MXDReportDialog
from resultdialog import ResultDialog
from workers.subprocessworker import SubprocessWorker
from workers.workerpool import WorkerPool

log = setup_logger(__name__)


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionPublish_Services.triggered.connect(self.show_publish_dialog)
        self.actionMXD_Data_Sources_Report.triggered.connect(self.show_mxd_report_dialog)
        self.actionGetInstallInfo.triggered.connect(self.get_install_info)
        self.actionGetExecutablePath.triggered.connect(self.get_executable_path)
        self.actionAbout.triggered.connect(self.about)
        self.actionTestLogWindow.triggered.connect(self.test_log_window)
        self.actionExit.triggered.connect(self.close)

        self.worker_pool = WorkerPool()

        self.log_handler = QtLogHandler()
        self.log_handler.messageEmitted.connect(self.log_message)
        runner.root_logger.addHandler(self.log_handler)

        self.config_dir = os.getenv(
            'AGS_SERVICE_PUBLISHER_CONFIG_DIR',
            os.path.abspath(os.path.join(os.path.dirname(get_app_path()), 'configs'))
        )

        self.log_dir = os.getenv(
            'AGS_SERVICE_PUBLISHER_LOG_DIR',
            os.path.abspath(os.path.join(os.path.dirname(get_app_path()), 'logs'))
        )

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
            self.worker_pool.stop_all_workers()
            log.debug('Exiting application!')
            event.accept()
        else:
            log.debug('Ignoring closeEvent')
            event.ignore()

    def publish_services(self, included_configs, included_services, included_envs, included_instances):
        worker = SubprocessWorker(
            target=runner.run_batch_publishing_job,
            kwargs={
                'included_configs': included_configs,
                'included_services': included_services,
                'included_envs': included_envs,
                'included_instances': included_instances,
                'config_dir': self.config_dir,
                'log_dir': self.log_dir
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker.id)

    def mxd_data_sources_report(self, included_configs, included_services, included_envs, output_filename):
        worker = SubprocessWorker(
            target=runner.run_mxd_data_sources_report,
            kwargs={
                'included_configs': included_configs,
                'included_services': included_services,
                'included_envs': included_envs,
                'output_filename': output_filename,
                'warn_on_validation_errors': True,
                'config_dir': self.config_dir
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker.id)

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

    def show_publish_dialog(self):
        publish_dialog = PublishDialog(self)
        publish_dialog.publishSelected.connect(self.publish_services)
        publish_dialog.exec_()

    def show_mxd_report_dialog(self):
        mxd_report_dialog = MXDReportDialog(self)
        mxd_report_dialog.runReport.connect(self.mxd_data_sources_report)
        mxd_report_dialog.exec_()

    def test_log_window(self):
        self.log_info_message('info')
        self.log_debug_message('debug')
        self.log_success_message('success')
        self.log_warning_message('warning')
        self.log_error_message('error')

    def handle_worker_message(self, worker_id, level, message):
        message = 'Worker {}: {}'.format(worker_id, message)
        self.log_message(level, message)

    def handle_worker_result(self, worker_id, exitcode, result):
        log.debug('Worker {} resulted in exitcode {} with result value: {}'.format(worker_id, exitcode, result))
        if exitcode == 0:
            self.log_success_message(result)
        else:
            self.log_error_message(result)

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
