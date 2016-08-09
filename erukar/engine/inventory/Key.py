from .Item import Item
import random

class Key(Item):
    sizes = [
        "large ",
        "small ",
        "tiny ",
        ""]

    def __init__(self, lock):
        self.lock = lock
        self.material = lock.material
        self.size = random.choice(self.sizes)
        alias = '{}{} Key'.format(self.size, self.material)

        super().__init__(alias, alias)

    def toggle_lock(self, target):
        if target is self.lock:
            target.is_locked = not target.is_locked
            return True
        return False
