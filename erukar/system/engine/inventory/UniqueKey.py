from .Key import Key

class UniqueKey(Key):
    BriefDescription = "a key"
    BaseName = "Key"
    SuccessfulUnlock = 'You have successfully unlocked the {}.'

    def __init__(self, lock):
        self.lock = lock
        super().__init__(alias, alias)

    def toggle_lock(self, target):
        if target is self.lock:
            target.is_locked = not target.is_locked
            return True
        return False

    def on_use(self, cmd, target):
        toggled = self.toggle_lock(target)
        if toggled and self.owner is not None:
            self.owner.inventory.remove(self)
            cmd.append_result(cmd.sender_uid, self.SuccessfulUnlock.format(target.alias()))
            return True
        return False
