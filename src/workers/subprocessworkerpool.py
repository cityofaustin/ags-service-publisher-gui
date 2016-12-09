from PyQt4 import QtCore

import itertools

from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class SubProcessWorkerPool:
    get_next_worker_id = itertools.count().next
    get_next_thread_id = itertools.count().next

    def __init__(self):
        log.debug('Initialized worker pool')
        self.workers = {}
        self.threads = {}

    def add_worker(self, worker):
        worker_id = self.get_next_worker_id()
        self.workers[worker_id] = worker
        log.debug('Added worker {} to worker pool'.format(worker_id))
        return worker_id

    def start_worker(self, worker_id):
        worker = self.workers[worker_id]
        thread_id = self.get_next_thread_id()
        thread = QtCore.QThread()
        self.threads[thread_id] = thread
        worker.moveToThread(thread)

        thread.started.connect(worker.start)
        thread.finished.connect(worker.stop)

        thread.start()
        log.debug('Started worker {} on thread {}'.format(worker_id, thread_id))

    def quit_all_threads(self):
        for thread_id, thread in self.threads.iteritems():
            thread.quit()
            thread.wait()
