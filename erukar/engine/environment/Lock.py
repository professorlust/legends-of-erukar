class Lock:
    '''Class which includes all functionality for locking and unlocking'''

    def __init__(self):
        self.is_locked = True
        self.armor_class = 10
        self.durability = 5

    def on_attack(self, sender, attack_roll, damage):
        if attack_roll <= self.durability:
            return "{}'s attack on the lock had little effect.".format(sender.alias())

        self.durability -= damage
        if self.durability < 1:
            self.is_locked = False
            return "{} has destroyed the lock!".format(sender.alias())

        return "{} has damaged the lock a bit.".format(sender.alias())
