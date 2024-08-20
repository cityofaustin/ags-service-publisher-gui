import itertools
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
            - Worker ID (int)
            - Exit code (int)
            - Return value or exception instance (object)
    """

    resultEmitted = QtCore.pyqtSignal(int, int, object)

    def get_next_worker_id(self):
        return next(itertools.count())

    def __init__(self, parent=None, target=None, args=(), kwargs={}, timer_check_interval=1000):
        super(ThreadWorker, self).__init__(parent)
        self.id = self.get_next_worker_id()
        self.exitcode = None
        self.running = False
        self.timer = None
        self.timer_check_interval = timer_check_interval
        self.elapsed_timer = None
        self.target = target
        self.args = tuple(args)
        self.kwargs = dict(kwargs)

        self.thread = QtCore.QThread()
        self.moveToThread(self.thread)

        self.thread.started.connect(self.start)
        self.thread.finished.connect(self.stop)

        log.debug('Worker {} initialized on thread {}'.format(self.id, str(self.thread)))

    @QtCore.pyqtSlot()
    def start(self):
        if self.running:
            log.warn('Worker {} already started on thread {}'.format(self.id, str(self.thread)))
            return
        log.debug('Worker {} started on thread {}'.format(self.id, str(self.thread)))
        self.running = True

        self.elapsed_timer = QtCore.QElapsedTimer()
        self.elapsed_timer.start()

        log.debug('Thread {} started'.format(self.thread))

        self.wrap_target_function(self.target, **self.kwargs)


    @QtCore.pyqtSlot()
    def stop(self):
        if not self.running:
            log.warn('Worker {} already stopped on thread {}'.format(self.id, str(self.thread)))
            return
        self.running = False

        if self.thread.isRunning():
            log.debug('Terminating thread {} '.format(self.thread))
            self.thread.exit(self.exitcode)
        log.debug('Worker {} stopped on thread {} (elapsed time {})'.format(self.id, str(self.thread), timedelta(milliseconds=self.elapsed_timer.elapsed())))


    def wrap_target_function(self, target, *args, **kwargs):
        result = None
        try:
            log.debug(f'Wrapping target function: {target.__module__}.{target.__qualname__}')
            result = target(*args, **kwargs)
            self.exitcode = 0
        except:
            self.exitcode = 1
            result = Exception(''.join(traceback.format_exception(*sys.exc_info())))
            raise
        finally:
            self.resultEmitted.emit(self.id, self.exitcode, result)
