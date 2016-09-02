from erukar.engine.model.Containable import Containable
from erukar.engine.environment.Lock import Lock

class Container(Containable):
    def __init__(self, aliases):
        super().__init__(aliases)
        self.lock = None
        self.description = broad_results

    def on_open(self, sender):
        if self.lock is not None:
            if self.lock.is_locked:
                return "This container is locked!"

        return "Opened a chest"

    def on_close(self, sender):
        return "Closed a chest"

    def describe(self):
        return Containable.describe(self)

    def on_inspect(self, *_):
        return Containable.on_inspect(self)
