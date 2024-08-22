import itertools

from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class WorkerPool:

    def __init__(self):
        log.debug('Initialized worker pool')
        self.workers = {}
        self.id_iterator = itertools.count()

    def get_next_worker_id(self):
        return next(self.id_iterator)

    def add_worker(self, worker):
        worker.resultEmitted.connect(self.remove_worker)
        log.debug(f'Adding {worker.name} to worker pool')
        self.workers[worker.id] = worker

    def remove_worker(self, worker):
        log.debug(f'Removing {worker.name} from worker pool')
        self.stop_worker(worker)
        worker.thread.deleteLater()
        worker.deleteLater()
        del self.workers[worker.id]
        del worker

    def start_worker(self, worker):
        log.debug(f'Starting {worker.name} in worker pool')
        worker.thread.start()

    def stop_worker(self, worker):
        log.debug(f'Stopping {worker.name} in worker pool')
        if worker.thread.isRunning():
            worker.thread.quit()
            worker.thread.wait()

    def stop_all_workers(self):
        log.debug('Stopping all workers in worker pool')
        for worker in self.workers.values():
            self.stop_worker(worker)

    def remove_all_workers(self):
        log.debug('Removing all workers from worker pool')
        for worker in self.workers.values():
            self.remove_worker(worker)
