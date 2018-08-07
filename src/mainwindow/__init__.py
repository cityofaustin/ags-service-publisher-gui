from PySide2 import QtWidgets
from ags_service_publisher.runner import Runner, root_logger
from ags_service_publisher.logging_io import setup_logger

from aboutdialog import AboutDialog
from helpers.arcpyhelpers import get_install_info
from helpers.pathhelpers import get_app_path, get_config_dir, get_log_dir, get_report_dir
from helpers.texthelpers import escape_html
from loghandlers.qtloghandler import QtLogHandler
from mainwindow_ui import Ui_MainWindow
from publishdialog import PublishDialog
from mxdreportdialog import MXDReportDialog
from datasetusagesreportdialog import DatasetUsagesReportDialog
from resultdialog import ResultDialog
from workers.subprocessworker import SubprocessWorker
from workers.workerpool import WorkerPool

log = setup_logger(__name__)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionPublish_Services.triggered.connect(self.show_publish_dialog)
        self.actionMXD_Data_Sources_Report.triggered.connect(self.show_mxd_report_dialog)
        self.actionDataset_Usages_Report.triggered.connect(self.show_dataset_usages_report_dialog)
        self.actionGetInstallInfo.triggered.connect(self.get_install_info)
        self.actionGetExecutablePath.triggered.connect(self.get_executable_path)
        self.actionAbout.triggered.connect(self.about)
        self.actionTestLogWindow.triggered.connect(self.test_log_window)
        self.actionExit.triggered.connect(self.close)

        self.worker_pool = WorkerPool()

        self.log_handler = QtLogHandler()
        self.log_handler.messageEmitted.connect(self.log_message)
        root_logger.addHandler(self.log_handler)

        self.config_dir = get_config_dir()
        self.log_dir = get_log_dir()
        self.report_dir = get_report_dir()

    def closeEvent(self, event):
        log.debug('closeEvent triggered')
        result = QtWidgets.QMessageBox.question(
            self,
            'Exit - AGS Service Publisher',
            'Are you sure you want to exit?',
            QtWidgets.QMessageBox.Yes,
            QtWidgets.QMessageBox.No
        )

        if result == QtWidgets.QMessageBox.Yes:
            self.worker_pool.stop_all_workers()
            log.debug('Exiting application!')
            event.accept()
        else:
            log.debug('Ignoring closeEvent')
            event.ignore()

    def publish_services(self, included_configs, included_services, included_envs, included_instances):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir)
        worker = SubprocessWorker(
            target=runner.run_batch_publishing_job,
            kwargs={
                'included_configs': included_configs,
                'included_services': included_services,
                'included_envs': included_envs,
                'included_instances': included_instances
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker.id)

    def mxd_data_sources_report(self, included_configs, included_services, included_envs, output_filename):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir)
        worker = SubprocessWorker(
            target=runner.run_mxd_data_sources_report,
            kwargs={
                'included_configs': included_configs,
                'included_services': included_services,
                'included_envs': included_envs,
                'output_filename': output_filename,
                'warn_on_validation_errors': True
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker.id)

    def dataset_usages_report(self, included_envs, included_instances, output_filename):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir)
        worker = SubprocessWorker(
            target=runner.run_dataset_usages_report,
            kwargs={
                'included_envs': included_envs,
                'included_instances': included_instances,
                'output_filename': output_filename
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
            result_dialog.setIcon(QtWidgets.QMessageBox.Information)
            result_dialog.setText(str(get_install_info()))
        except StandardError as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.exec_()

    def get_executable_path(self):
        result_dialog = ResultDialog(self)

        try:
            result_dialog.setWindowTitle('Executable Path - AGS Service Publisher')
            result_dialog.setIcon(QtWidgets.QMessageBox.Information)
            result_dialog.setText(get_app_path())
        except StandardError as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtWidgets.QMessageBox.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.exec_()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()

    def show_publish_dialog(self):
        try:
            publish_dialog = PublishDialog(self)
            publish_dialog.publishSelected.connect(self.publish_services)
            publish_dialog.exec_()
        except Exception:
            log.exception('An error occurred while showing the Publish dialog')
            raise

    def show_mxd_report_dialog(self):
        try:
            mxd_report_dialog = MXDReportDialog(self)
            mxd_report_dialog.runReport.connect(self.mxd_data_sources_report)
            mxd_report_dialog.exec_()
        except Exception:
            log.exception('An error occurred while showing the MXD Report dialog')
            raise

    def show_dataset_usages_report_dialog(self):
        try:
            dataset_usages_report_dialog = DatasetUsagesReportDialog(self)
            dataset_usages_report_dialog.runReport.connect(self.dataset_usages_report)
            dataset_usages_report_dialog.exec_()
        except Exception:
            log.exception('An error occurred while showing the Dataset Usages Report dialog')
            raise

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
