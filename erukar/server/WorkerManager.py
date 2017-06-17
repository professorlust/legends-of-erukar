from erukar.engine.model.Manager import Manager

class WorkerManager(Manager):
    def __init__(self):
        super().__init__()
        self.workers = []
        self.processes = []
        self.frozen_processes
