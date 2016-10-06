from erukar.engine.inventory.StackableItem import StackableItem
import random

class Key(StackableItem):
    Persistent = False
    BriefDescription = "a key"
    BaseName = "Key"
    SuccessfulUnlock = 'You have successfully unlocked the {}.'

    def __init__(self, lock):
        self.lock = lock
        alias = 'key'
        super().__init__(alias, alias)

    def toggle_lock(self, target):
        if target is self.lock:
            target.is_locked = not target.is_locked
            return True
        return False

    def on_use(self, target):
        toggled = self.toggle_lock(target)
        if toggled and self.owner is not None:
            self.owner.inventory.remove(self)
            return self.SuccessfulUnlock.format(target.alias()), True
        return '', False
