import erukar
from erukar.engine.inventory.Key import Key

class TieredKey(Key):
    MaximumStackQuantity = 9999
    Persistent = True
    BriefDescription = "a {Tier} key"
    WrongTarget = 'Invalid target for use with a {Tier} key.'
    FailedToUnlock = 'This lock is a {} tier; you cannot unlock it with a {} key.'
    Tier = 'Iron'

    def __init__(self):
        super().__init__('Key')

    def on_use(self, cmd, target):
        if isinstance(target, erukar.engine.environment.Passage):
            if not target.door:
                return 'There is nothing in this direction to unlock.', False
            target = target.door

        if isinstance(target, erukar.engine.environment.Door):
            if not target.lock:
                return 'This door has no lock to unlock.', False
            target = target.lock

        if not isinstance(target, erukar.engine.environment.TieredLock):
            return self.mutate(self.WrongTarget), False

        if target.tier == self.Tier and target.is_locked:
            self.consume()
            target.is_locked = False
        return self.mutate('The {Tier} lock has been successfully unlocked.'), not target.is_locked
