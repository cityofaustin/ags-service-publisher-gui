from ags_service_publisher.logging_io import setup_logger

log = setup_logger(__name__)


class WorkerPool:

    def __init__(self):
        log.debug('Initialized worker pool')
        self.workers = {}

    def add_worker(self, worker):
        log.debug('Adding worker {} to worker pool'.format(worker.id))
        worker.resultEmitted.connect(self.remove_worker)
        self.workers[worker.id] = worker

    def remove_worker(self, worker_id):
        log.debug('Removing worker {} from worker pool'.format(worker_id))
        worker = self.workers[worker_id]
        self.stop_worker(worker_id)
        worker.thread.deleteLater()
        worker.deleteLater()
        del self.workers[worker.id]
        del worker

    def start_worker(self, worker_id):
        log.debug('Starting worker {} in worker pool'.format(worker_id))
        worker = self.workers[worker_id]
        worker.thread.start()

    def stop_worker(self, worker_id):
        log.debug('Stopping worker {} in worker pool'.format(worker_id))
        worker = self.workers[worker_id]
        if worker.thread.isRunning():
            worker.thread.quit()
            worker.thread.wait()

    def stop_all_workers(self):
        log.debug('Stopping all workers in worker pool')
        for worker_id, worker in self.workers.items():
            self.stop_worker(worker_id)

    def remove_all_workers(self):
        log.debug('Removing all workers from worker pool')
        for worker_id, worker in self.workers.items():
            self.remove_worker(worker_id)
