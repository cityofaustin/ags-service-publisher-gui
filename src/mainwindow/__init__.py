import os

from PyQt4 import QtGui

from mainwindow import Ui_MainWindow
from aboutdialog import AboutDialog

from ags_service_publisher import runner
from ags_service_publisher.logging_io import setup_logger
from helpers.pathhelpers import get_app_path
from helpers.arcpyhelpers import get_install_info

log = setup_logger(__name__)


class MainWindow(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.actionPublish_Services.triggered.connect(self.publish_services)
        self.actionMXD_Data_Sources_Report.triggered.connect(self.mxd_data_sources_report)
        self.actionGetInstallInfo.triggered.connect(self.get_install_info)
        self.actionGetExecutablePath.triggered.connect(self.get_executable_path)
        self.actionAbout.triggered.connect(self.about)
        self.actionExit.triggered.connect(self.close)

    def closeEvent(self, event):
        log.debug('closeEvent triggered')
        result = QtGui.QMessageBox.question(
            self,
            'Exit - AGS Service Publisher',
            'Are you sure to exit?',
            QtGui.QMessageBox.Yes,
            QtGui.QMessageBox.No
        )

        if result == QtGui.QMessageBox.Yes:
            log.debug('Exiting application!')
            event.accept()
        else:
            log.debug('Ignoring closeEvent')
            event.ignore()

    def publish_services(self):
        configs = ['LP_Testing']
        result_dialog = ResultDialog(self)

        try:
            runner.run_batch_publishing_job(included_configs=configs, warn_on_validation_errors=True, verbose=True)
            result_dialog.setWindowTitle('Success - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Information)
            result_dialog.setText('Successfully published configs: {}'.format(', '.join(configs)))
        except StandardError as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.exec_()

    def mxd_data_sources_report(self):
        configs = ['LP_Testing']
        report_name = 'test.csv'
        report_path = os.path.join(r'C:\Users\pughl\Documents\python_projects\ags-service-reports', report_name)
        result_dialog = ResultDialog(self)

        try:
            runner.run_mxd_data_sources_report(included_configs=configs, output_filename=report_path, warn_on_validation_errors=True, verbose=True)
            result_dialog.setWindowTitle('Success - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Information)
            result_dialog.setText('Report written to {}'.format(report_path))
        except StandardError as e:
            result_dialog.setWindowTitle('Error - AGS Service Publisher')
            result_dialog.setIcon(QtGui.QMessageBox.Critical)
            result_dialog.setText(str(e))
        finally:
            result_dialog.exec_()

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


class ResultDialog(QtGui.QMessageBox):
    def __init__(self, parent=None):
        QtGui.QMessageBox.__init__(self, parent)
