import erukar
from erukar.engine.inventory.Key import Key

class TieredKey(Key):
    MaximumStackQuantity = 9999
    Persistent = True
    BriefDescription = "a {Tier} key"
    WrongTarget = 'Invalid target for use with a {Tier} key.'
    FailedToUnlock = 'This lock is a {} tier; you cannot unlock it with a {} key.'
    BaseName = "{Tier} Key"
    Tier = 'Iron'

    def __init__(self):
        super().__init__(self.mutate(self.BaseName))

    def on_use(self, cmd, target):
        if not isinstance(target, erukar.engine.environment.TieredLock):
            return self.mutate(self.WrongTarget), False

        if target.tier == self.Tier and target.is_locked:
            self.consume()
            target.is_locked = False
            cmd.append_result(cmd.sender_uid, self.mutate(self.SuccessfulUnlock, {'target':target.alias()}))

        return not target.is_locked
