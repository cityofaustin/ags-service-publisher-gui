from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class SubProcessWorkerPool:

    def __init__(self):
        log.debug('Initialized worker pool')
        self.workers = {}

    def add_worker(self, worker):
        self.workers[worker.id] = worker
        log.debug('Added worker {} to worker pool'.format(worker.id))

    def start_worker(self, worker_id):
        worker = self.workers[worker_id]
        worker.thread.start()

    def quit_all_workers(self):
        for worker_id, worker in self.workers.iteritems():
            if worker.thread.isRunning():
                worker.thread.quit()
                worker.thread.wait()
