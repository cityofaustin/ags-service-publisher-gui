import sys
import traceback
from datetime import timedelta


from PyQt6 import QtCore
from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class ThreadWorker(QtCore.QObject):
    """
    Worker object that runs the target function in a separate thread and emits its result.

    Signals and parameters:

        - resultEmitted: Emitted when the thread ends.
            - Worker (QObject)
            - Exit code (int)
            - Return value or exception instance (object)
    """

    resultEmitted = QtCore.pyqtSignal(QtCore.QObject, int, object)


    def __init__(self, worker_pool, target=None, args=(), kwargs={}):
        super(ThreadWorker, self).__init__()
        self.id = worker_pool.get_next_worker_id()
        self.name = f'{type(self).__name__}-{self.id}'
        self.exitcode = None
        self.running = False
        self.elapsed_timer = None
        self.target = target
        self.args = tuple(args)
        self.kwargs = dict(kwargs)

        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)

        self.thread.started.connect(self.start)
        self.thread.finished.connect(self.stop)

        log.debug(f'{self.name} initialized on thread {str(self.thread)}')

    @QtCore.pyqtSlot()
    def start(self):
        if self.running:
            log.warn(f'{self.name} already started on thread {str(self.thread)}')
            return
        log.debug(f'{self.name} started on thread {str(self.thread)}')
        self.running = True

        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()

        log.debug(f'Thread {self.thread} started')

        QtCore.QTimer.singleShot(0, lambda: self.wrap_target_function(self.target, *self.args, **self.kwargs))


    @QtCore.pyqtSlot()
    def stop(self):
        if not self.running:
            log.warn(f'{self.name} already stopped on thread {str(self.thread)}')
            return
        self.running = False

        if self.thread.isRunning():
            log.debug(f'Terminating thread {self.thread}')
            self.thread.exit(self.exitcode)
        log.debug(f'{self.name} stopped on thread {str(self.thread)} (elapsed time {timedelta(milliseconds=self.elapsed_timer.elapsed())})')


    def wrap_target_function(self, target, *args, **kwargs):
        result = None
        try:
            log.debug(f'Wrapping target function: {target.__module__}.{target.__qualname__}')
            result = target(*args, **kwargs)
            self.exitcode = 0
        except:
            self.exitcode = 1
            result = Exception(''.join(traceback.format_exception(*sys.exc_info())))
        finally:
            self.resultEmitted.emit(self, self.exitcode, result)
