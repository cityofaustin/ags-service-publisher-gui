from PyQt4 import QtCore

import multiprocessing
from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class Worker(QtCore.QObject):

    def __init__(self, parent=None, target=None, args=None, kwargs=None):
        super(Worker, self).__init__(parent)
        self.running = False
        self.timer = None
        self.process = None
        self.target = target
        self.args = args if args is not None else tuple()
        self.kwargs = kwargs if kwargs is not None else dict()
        log.debug('Worker initialized on thread {}'.format(self.thread()))

    job_success = QtCore.pyqtSignal(str)
    job_failure = QtCore.pyqtSignal(str)

    def check_process_status(self):
        if self.running:
            log.debug('Checking status of subprocess {} (pid {})'.format(self.process.name, self.process.pid))
            if self.process.exitcode == 0:
                message = 'Subprocess {} finished successfully (pid {}, exit code {})'.format(
                    self.process.name, self.process.pid, self.process.exitcode
                )
                self.job_success.emit(message)
                log.debug(message)
            elif self.process.exitcode > 0:
                message = 'An error occurred in subprocess {} (pid {}, exit code {})'.format(
                    self.process.name, self.process.pid, self.process.exitcode
                )
                self.job_failure.emit(message)
                log.debug(message)
            else:
                message = 'Subprocess {} (pid {}) is still active'.format(self.process.name, self.process.pid)
                log.debug(message)
        else:
            message = 'Cannot check process status while worker is not running!'
            log.error(message)
            raise RuntimeError(message)

    @QtCore.pyqtSlot()
    def start(self):
        log.debug('Worker started on thread {}'.format(self.thread()))
        self.running = True

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_process_status)

        self.process = multiprocessing.Process(
            target=self.target,
            args=self.args,
            kwargs=self.kwargs
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


