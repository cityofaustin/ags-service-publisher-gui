from PyQt4 import QtCore

import os
import multiprocessing
from ags_service_publisher import runner
from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class Worker(QtCore.QObject):

    def __init__(self, parent=None):
        super(Worker, self).__init__(parent)
        self.running = False
        self.timer = None
        self.process = None
        log.debug('Worker initialized on thread {}'.format(self.thread()))

    job_success = QtCore.pyqtSignal(str)
    job_failure = QtCore.pyqtSignal(str)

    def check_process_status(self):
        if self.running:
            log.debug('Checking status of process {} (pid {})'.format(self.process.name, self.process.pid))
            if not self.process.is_alive():
                if self.process.exitcode != 0:
                    self.job_failure.emit(
                        'An error occurred in subprocess {} (pid {}, exit code {}) while running MXD data sources report!'
                        .format(self.process.name, self.process.pid, self.process.exitcode)
                    )
                else:
                    self.job_success.emit('Report successfully written to {}'.format(None))
        else:
            raise RuntimeError('Cannot check process status while worker is not running!')

    @QtCore.pyqtSlot()
    def start(self):
        log.debug('Worker started on thread {}'.format(self.thread()))
        self.running = True

        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.check_process_status)

        configs = ['LP_Testing']
        report_name = 'test.csv'
        report_path = os.path.join(r'C:\Users\pughl\Documents\python_projects\ags-service-reports', report_name)

        self.process = multiprocessing.Process(
            target=runner.run_mxd_data_sources_report,
            kwargs={
                'included_configs': configs,
                'output_filename': report_path,
                'warn_on_validation_errors': True,
                'verbose': True
            }
        )
        self.process.start()
        self.timer.start(1000)
        log.debug('Process {} (pid {}) started'.format(self.process.name, self.process.pid))

    @QtCore.pyqtSlot()
    def stop(self):
        self.running = False
        self.timer.stop()
        if self.process.is_alive():
            log.debug('Terminating process {} (pid {})'.format(self.process.name, self.process.pid))
            self.process.terminate()
            self.process.join()
        log.debug('Worker stopped on thread {}'.format(self.thread()))


