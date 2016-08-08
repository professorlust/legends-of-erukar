from erukar.engine.model.Containable import Containable
from erukar.engine.environment.Lock import Lock

class Container(Containable):
    def __init__(self, aliases, broad_results, inspect_results):
        super().__init__(aliases, broad_results, inspect_results)
        self.lock = Lock()
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

    def unlock(self, key):
        if self.lock is None:
            return 'Cannot unlock a container without a lock.'

        if key.lock is self.lock:
            self.lock.is_locked = False
            return 'Successfully unlocked the container'

        return 'Cannot unlock this container with that key'
