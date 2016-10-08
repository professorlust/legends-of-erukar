from erukar.engine.inventory.Key import Key

class TieredKey(Key):
    Persistent = True
    BriefDescription = "a {tier_material} key"
    WrongTarget = 'Invalid target for use with a {Tier} key.'
    FailedToUnlock = 'This lock is a {} tier; you cannot unlock it with a {} key.'
    BaseName = "{tier_material} Key"
    Tier = 'Iron'

    def on_use(self, target):
        if not isinstance(target, erukar.engine.environment.TieredLock):
            return self.mutate(self.WrongTarget), False

        if target.tier is self.Tier and target.is_locked:
            self.consume_key()
            target.is_locked = False
            return self.mutate(self.SuccessfulUnlock, {'target':target.alias()}), True

        return self.FailedToUnlock.format(target.tier, self.Tier), False

    def consume_key(self):
        self.quantity -= 1
        if self.quantity <= 0:
            self.owner.inventory.remove(self)
