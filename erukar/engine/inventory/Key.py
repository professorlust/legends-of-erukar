from erukar.engine.inventory.StackableItem import StackableItem
import random

class Key(StackableItem):
    Persistent = False
    BriefDescription = "a key"
    BaseName = "Key"
    SuccessfulUnlock = 'You have successfully unlocked the {target}.'
    FailedToUnlock = 'You have failed to unlock the  {target}.'

    def on_use(self, target):
        if isinstance(target, erukar.engine.environment.Lock) and target.is_locked:
            target.is_locked = False
            self.owner.inventory.remove(self)
            return self.mutate(self.SuccessfulUnlock,{'target': target.alias()}), True
        return self.mutate(self.FailedToUnlock,{'target': target.alias()}), False
