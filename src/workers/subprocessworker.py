import itertools
import multiprocessing
import sys
import traceback

from PyQt4 import QtCore
from ags_service_publisher.logging_io import setup_logger
from ags_service_publisher.mplog import logged_call

log = setup_logger(__name__)


class SubprocessWorker(QtCore.QObject):
    """
    Worker that runs the target function in a separate sub-process, watches its exitcode periodically and emits a
    signal with the worker ID, exit code and return value or exception instance when the process has exited.
    """

    result = QtCore.pyqtSignal(int, int, object)

    get_next_worker_id = itertools.count().next

    def __init__(self, parent=None, target=None, args=(), kwargs={}, timer_check_interval=1000, log_queue=None):
        super(SubprocessWorker, self).__init__(parent)
        self.id = self.get_next_worker_id()
        self.running = False
        self.timer = None
        self.timer_check_interval=timer_check_interval
        self.process = None
        self.log_queue = log_queue
        self.result_queue = multiprocessing.Queue()
        self.target = target
        self.args = tuple(args)
        self.kwargs = dict(kwargs)

        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)

        self.thread.started.connect(self.start)
        self.thread.finished.connect(self.stop)

        log.debug('Worker {} initialized on thread {}'.format(self.id, str(self.thread)))

    def check_process_status(self):
        if not self.running:
            message = 'Cannot check process status while worker is not running!'
            log.error(message)
            raise RuntimeError(message)
        log.debug('Checking status of subprocess {} (pid {})'.format(self.process.name, self.process.pid))
        if not self.process.is_alive():
            message = 'Subprocess {} ended (pid {}, exit code {})'.format(
                self.process.name, self.process.pid, self.process.exitcode
            )
            log.debug(message)
            self.result.emit(self.id, self.process.exitcode, self.result_queue.get())
        else:
            message = 'Subprocess {} (pid {}) is still active'.format(self.process.name, self.process.pid)
            log.debug(message)

    @QtCore.pyqtSlot()
    def start(self):
        if self.running:
            log.warn('Worker {} already started on thread {}'.format(self.id, str(self.thread)))
            return
        log.debug('Worker {} started on thread {}'.format(self.id, str(self.thread)))
        self.running = True

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.check_process_status)

        self.process = multiprocessing.Process(
            target=wrap_logged_call,
            args=(self.target, self.log_queue, self.result_queue) + self.args,
            kwargs=self.kwargs
        )

        self.process.start()
        self.timer.start(self.timer_check_interval)
        log.debug('Subprocess {} (pid {}) started'.format(self.process.name, self.process.pid))

    @QtCore.pyqtSlot()
    def stop(self):
        if not self.running:
            log.warn('Worker {} already stopped on thread {}'.format(self.id, str(self.thread)))
            return
        self.running = False
        self.timer.stop()
        if self.process.is_alive():
            log.debug('Terminating subprocess {} (pid {})'.format(self.process.name, self.process.pid))
            self.process.terminate()
            self.process.join()
        log.debug('Worker {} stopped on thread {}'.format(self.id, str(self.thread)))


def wrap_logged_call(func, log_queue, result_queue, *args, **kwargs):
    try:
        result = logged_call(log_queue, func, *args, **kwargs)
        result_queue.put(result)
    except:
        result = Exception(''.join(traceback.format_exception(*sys.exc_info())))
        result_queue.put(result)
        raise
