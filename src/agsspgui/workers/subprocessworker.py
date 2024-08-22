import multiprocessing
import sys
import traceback
from datetime import timedelta
from logging.handlers import QueueHandler, QueueListener


from PyQt6 import QtCore
from ags_service_publisher.logging_io import setup_logger

from ..loghandlers.qtloghandler import QtLogHandler

log = setup_logger(__name__)


class SubprocessWorker(QtCore.QObject):
    """
    Worker object that runs the target function in a separate sub-process, checking its exitcode periodically.

    Signals and parameters:

        - messageEmitted: Emitted whenever the target function's root logger emits a message
            - Worker ID (int)
            - Log level (int)
            - Log message (str)
        - resultEmitted: Emitted when the process ends.
            - Worker ID (int)
            - Exit code (int)
            - Return value or exception instance (object)
    """

    messageEmitted = QtCore.pyqtSignal(int, int, str)
    resultEmitted = QtCore.pyqtSignal(int, int, object)

    def __init__(self, worker_pool, target=None, args=(), kwargs={}, timer_check_interval=1000, log_handler=None):
        super(SubprocessWorker, self).__init__()
        self.id = worker_pool.get_next_worker_id()
        self.running = False
        self.timer = None
        self.timer_check_interval = timer_check_interval
        self.elapsed_timer = None
        self.process = None
        self.log_handler = log_handler if log_handler is not None else QtLogHandler()
        self.log_handler.messageEmitted.connect(self.handle_message)
        self.log_queue = multiprocessing.Queue()
        self.result_queue = multiprocessing.Queue()
        self.log_queue_listener = QueueListener(self.log_queue, self.log_handler)
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
            message = 'Subprocess {} ended (pid {}, exit code {}, elapsed time {})'.format(
                self.process.name, self.process.pid, self.process.exitcode, timedelta(milliseconds=self.elapsed_timer.elapsed())
            )
            log.debug(message)
            self.resultEmitted.emit(self.id, self.process.exitcode, self.result_queue.get())
        else:
            message = 'Subprocess {} (pid {}) is still active (elapsed time {})'.format(self.process.name, self.process.pid, timedelta(milliseconds=self.elapsed_timer.elapsed()))
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
        self.elapsed_timer = QtCore.QElapsedTimer()

        self.log_queue_listener.start()

        self.process = multiprocessing.Process(
            target=wrap_target_function,
            args=(self.target, self.log_queue, self.result_queue) + self.args,
            kwargs=self.kwargs
        )

        self.process.start()
        self.timer.start(self.timer_check_interval)
        self.elapsed_timer.start()
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
        log.debug('Worker {} stopped on thread {} (elapsed time {})'.format(self.id, str(self.thread), timedelta(milliseconds=self.elapsed_timer.elapsed())))

        self.log_queue_listener.stop()

    @QtCore.pyqtSlot(int, str)
    def handle_message(self, level, message):
        self.messageEmitted.emit(self.id, level, message)


def wrap_target_function(target, log_queue, result_queue, *args, **kwargs):
    try:
        setup_logger(namespace=None, handler=QueueHandler(log_queue))
        log.debug(f'Wrapping target function: {target.__module__}.{target.__qualname__}')
        result = target(*args, **kwargs)
        result_queue.put(result)
    except:
        result = Exception(''.join(traceback.format_exception(*sys.exc_info())))
        result_queue.put(result)
        raise
