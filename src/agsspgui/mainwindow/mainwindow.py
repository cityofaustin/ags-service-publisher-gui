import logging

from PyQt6 import QtCore, QtWidgets
from ags_service_publisher.runner import Runner
from ags_service_publisher.logging_io import setup_logger

from ..aboutdialog import AboutDialog
from ..helpers.arcpyhelpers import get_install_info
from ..helpers.confighelpers import reload_configs
from ..helpers.pathhelpers import get_app_path, get_config_dir, get_log_dir, get_report_dir
from ..helpers.texthelpers import escape_html
from ..loghandlers.qtloghandler import QtLogHandler
from .mainwindow_ui import Ui_MainWindow
from ..publishdialog import PublishDialog
from ..aprxconverterdialog import APRXConverterDialog
from ..mxdreportdialog import MXDReportDialog
from ..datasetusagesreportdialog import DatasetUsagesReportDialog
from ..datastoresreportdialog import DataStoresReportDialog
from ..resultdialog import ResultDialog
from ..workers import SubprocessWorker, ThreadWorker, WorkerPool

log = setup_logger(__name__)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.defaultGeometry = self.saveGeometry()
        self.defaultWindowState = self.saveState()
        self.settings = QtCore.QSettings()
        self.actionPublish_Services.triggered.connect(self.show_publish_dialog)
        self.actionAPRX_Converter.triggered.connect(self.show_aprx_converter_dialog)
        self.actionMXD_Data_Sources_Report.triggered.connect(self.show_mxd_report_dialog)
        self.actionDataset_Usages_Report.triggered.connect(self.show_dataset_usages_report_dialog)
        self.actionData_Stores_Report.triggered.connect(self.show_data_stores_report_dialog)
        self.actionGetInstallInfo.triggered.connect(self.get_install_info)
        self.actionGetExecutablePath.triggered.connect(self.get_executable_path)
        self.actionAbout.triggered.connect(self.about)
        self.actionReload_configuration_files.triggered.connect(lambda: self.load_configs(show_result_on_success=True, reload=True))
        self.actionResetSettingsToDefault.triggered.connect(self.reset_settings_to_default)
        self.actionTestLogWindow.triggered.connect(self.test_log_window)
        self.actionExit.triggered.connect(self.close)

        self.worker_pool = WorkerPool()

        self.log_handler = QtLogHandler()
        self.log_handler.messageEmitted.connect(self.log_message)
        logging.root.addHandler(self.log_handler)

        self.config_dir = get_config_dir()
        self.log_dir = get_log_dir()
        self.report_dir = get_report_dir()

        QtCore.QTimer.singleShot(0, self.read_settings)
        QtCore.QTimer.singleShot(0, self.load_configs)
    
    def write_settings(self):
        self.settings.beginGroup('WindowSettings/MainWindow')
        self.settings.setValue('geometry', self.saveGeometry())
        self.settings.setValue('windowState', self.saveState())
        self.settings.endGroup()

    def read_settings(self):
        self.settings.beginGroup('WindowSettings/MainWindow')
        self.restoreGeometry(self.settings.value('geometry', QtCore.QByteArray()))
        self.restoreState(self.settings.value('windowState', QtCore.QByteArray()))
        self.settings.endGroup()
    
    def reset_settings_to_default(self):
        log.debug('Resetting settings to default')
        self.settings.clear()
        self.restoreGeometry(self.defaultGeometry)
        self.restoreState(self.defaultWindowState)
        self.move(self.screen().geometry().center() - QtCore.QRect(QtCore.QPoint(), self.frameGeometry().size()).center())
    
    def closeEvent(self, event):
        log.debug('MainWindow closeEvent triggered')
        result = QtWidgets.QMessageBox.question(
            self,
            'Exit - AGS Service Publisher',
            'Are you sure you want to exit?',
            QtWidgets.QMessageBox.StandardButton.Yes,
            QtWidgets.QMessageBox.StandardButton.No
        )

        if result == QtWidgets.QMessageBox.StandardButton.Yes:
            self.worker_pool.stop_all_workers()
            log.debug('Exiting application!')
            self.write_settings()
            event.accept()
        else:
            log.debug(f'Ignoring MainWindow closeEvent')
            event.ignore()
    
    def load_configs(self, show_result_on_success=False, reload=False):
        self.menubar.setEnabled(False)
        result_dialog = ResultDialog(self)
        mode = 'reload' if reload else 'load'

        def show_reload_configs_result(worker, exitcode, result):
            try:
                if exitcode != 0:
                    raise RuntimeError(
                        f'An error occurred in {worker.name} (exit code: {exitcode}) while {mode}ing config files: {result}'
                    )
                if show_result_on_success:
                    result_dialog.setWindowTitle('Success - AGS Service Publisher')
                    result_dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
                    result_dialog.setText(str(result))
                    result_dialog.open()
            except Exception as e:
                result_dialog.setWindowTitle('Error - AGS Service Publisher')
                result_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                result_dialog.setText(str(e))
                result_dialog.open()

        worker = ThreadWorker(
            self.worker_pool,
            target=reload_configs,
            kwargs={
                'config_dir': self.config_dir,
                'mode': mode,
                'include_userconfig': True,
            }
        )
        worker.resultEmitted.connect(self.handle_worker_result)
        worker.resultEmitted.connect(show_reload_configs_result)
        worker.resultEmitted.connect(lambda: self.menubar.setEnabled(True))
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker)

    def publish_services(self, included_configs, included_services, included_envs, included_instances, create_backups, copy_source_files_from_staging_folder, delete_existing_services, publish_services):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir)
        worker = SubprocessWorker(
            self.worker_pool,
            target=runner.run_batch_publishing_job,
            kwargs={
                'included_configs': included_configs,
                'included_services': included_services,
                'included_envs': included_envs,
                'included_instances': included_instances,
                'create_backups': create_backups,
                'copy_source_files_from_staging_folder': copy_source_files_from_staging_folder,
                'delete_existing_services': delete_existing_services,
                'publish_services': publish_services,
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker)

    def run_aprx_converter(self, included_configs, included_services, included_envs):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir, report_dir=self.report_dir)
        worker = SubprocessWorker(
            self.worker_pool,
            target=runner.batch_convert_mxd_to_aprx,
            kwargs={
                'included_configs': included_configs,
                'included_services': included_services,
                'included_envs': included_envs,
                'warn_on_validation_errors': True
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker)

    def mxd_data_sources_report(self, included_configs, included_services, included_envs, output_filename):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir, report_dir=self.report_dir)
        worker = SubprocessWorker(
            self.worker_pool,
            target=runner.run_map_data_sources_report,
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
        self.worker_pool.start_worker(worker)

    def dataset_usages_report(self, included_datasets, included_envs, included_instances, output_filename):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir, report_dir=self.report_dir)
        worker = SubprocessWorker(
            self.worker_pool,
            target=runner.run_dataset_usages_report,
            kwargs={
                'included_datasets': included_datasets,
                'included_envs': included_envs,
                'included_instances': included_instances,
                'output_filename': output_filename
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker)

    def data_stores_report(self, included_envs, included_instances, output_filename):
        runner = Runner(config_dir=self.config_dir, log_dir=self.log_dir, report_dir=self.report_dir)
        worker = SubprocessWorker(
            self.worker_pool,
            target=runner.run_data_stores_report,
            kwargs={
                'included_envs': included_envs,
                'included_instances': included_instances,
                'output_filename': output_filename
            }
        )

        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker)

    def get_install_info(self):
        result_dialog = ResultDialog(self)

        def show_install_info_result(worker, exitcode, result):
            try:
                if exitcode != 0:
                    raise RuntimeError(
                        f'An error occurred in {worker.name} (exit code: {exitcode}) while getting ArcGIS Install Info: {result}'
                    )
                result_dialog.setWindowTitle('ArcGIS Install Info - AGS Service Publisher')
                result_dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
                result_dialog.setText(str(result))
            except Exception as e:
                result_dialog.setWindowTitle('Error - AGS Service Publisher')
                result_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
                result_dialog.setText(str(e))
            finally:
                result_dialog.open()

        worker = SubprocessWorker(
            self.worker_pool,
            target=get_install_info,
        )
        worker.messageEmitted.connect(self.handle_worker_message)
        worker.resultEmitted.connect(self.handle_worker_result)
        worker.resultEmitted.connect(show_install_info_result)
        self.worker_pool.add_worker(worker)
        self.worker_pool.start_worker(worker)

    def get_executable_path(self):
        result_dialog = ResultDialog(self)

        try:
            result_dialog.setWindowTitle('Executable Path - AGS Service Publisher')
            result_dialog.setIcon(QtWidgets.QMessageBox.Icon.Information)
            result_dialog.setText(get_app_path())
        except Exception as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtWidgets.QMessageBox.Icon.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.open()

    def about(self):
        about_dialog = AboutDialog(self)
        about_dialog.open()

    def show_publish_dialog(self):
        try:
            publish_dialog = PublishDialog(self)
            publish_dialog.publishSelected.connect(self.publish_services)
            publish_dialog.open()
        except Exception:
            log.exception('An error occurred while showing the Publish dialog')

    def show_aprx_converter_dialog(self):
        try:
            mxd_report_dialog = APRXConverterDialog(self)
            mxd_report_dialog.runConverter.connect(self.run_aprx_converter)
            mxd_report_dialog.open()
        except Exception:
            log.exception('An error occurred while showing the MXD Report dialog')

    def show_mxd_report_dialog(self):
        try:
            mxd_report_dialog = MXDReportDialog(self)
            mxd_report_dialog.runReport.connect(self.mxd_data_sources_report)
            mxd_report_dialog.open()
        except Exception:
            log.exception('An error occurred while showing the MXD Report dialog')

    def show_dataset_usages_report_dialog(self):
        try:
            dataset_usages_report_dialog = DatasetUsagesReportDialog(self)
            dataset_usages_report_dialog.runReport.connect(self.dataset_usages_report)
            dataset_usages_report_dialog.open()
        except Exception:
            log.exception('An error occurred while showing the Dataset Usages Report dialog')

    def show_data_stores_report_dialog(self):
        try:
            data_stores_report_dialog = DataStoresReportDialog(self)
            data_stores_report_dialog.runReport.connect(self.data_stores_report)
            data_stores_report_dialog.open()
        except Exception:
            log.exception('An error occurred while showing the Data Stores Report dialog')

    def test_log_window(self):
        self.log_info_message('info')
        self.log_debug_message('debug')
        self.log_success_message('success')
        self.log_warning_message('warning')
        self.log_error_message('error')

    def handle_worker_message(self, worker, level, message):
        message = f'{worker.name}: {message}'
        log.log(level, message)

    def handle_worker_result(self, worker, exitcode, result):
        log.debug(f'{worker.name} resulted in exitcode {exitcode} with result value: {result}')
        if exitcode == 0:
            self.log_success_message(result)
        else:
            self.log_error_message(result)

    def log_message(self, level, message):
        levelname = logging.getLevelName(level)
        if levelname == 'INFO':
            self.log_info_message(message)
        elif levelname == 'DEBUG':
            self.log_debug_message(message)
        elif levelname == 'WARNING':
            self.log_warning_message(message)
        elif levelname == 'ERROR':
            self.log_error_message(message)
        else:
            raise RuntimeError(f'Unknown message level: {level}')

    def log_info_message(self, message):
        self.logWindow.appendPlainText(message)
    def log_debug_message(self, message):
        self.logWindow.appendHtml(f'<font color="gray">{escape_html(message)}</font>')

    def log_warning_message(self, message):
        self.logWindow.appendHtml(f'<font color="blue">{escape_html(message)}</font>')

    def log_success_message(self, message):
        self.logWindow.appendHtml(f'<font color="green">{escape_html(message)}</font>')

    def log_error_message(self, message):
        self.logWindow.appendHtml(f'<font color="red">{escape_html(message)}</font>')
