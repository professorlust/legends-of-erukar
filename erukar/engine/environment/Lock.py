from erukar.engine.model.EnvironmentPiece import EnvironmentPiece
import random

class Lock(EnvironmentPiece):
    '''Class which includes all functionality for locking and unlocking'''

    materials = [
        "ornamental",
        "copper",
        "steel",
        "silver",
        "brass",
        "bronze",
        "iron"]

    def __init__(self):
        self.material = random.choice(self.materials)
        name = '{} lock'.format(self.material)
        super().__init__([name])
        self.direction = None 
        self.is_locked = True
        self.armor_class = 10
        self.durability = 5

    def on_inspect(self, *_):
        if self.is_locked:
            return 'The lock is secured and latched, barring any entry into the room.'
        return 'The lock has been unlocked and does not prevent the door from opening.'

    def on_attack(self, sender, attack_roll, damage):
        if attack_roll <= self.durability:
            return "{}'s attack on the lock had little effect.".format(sender.alias())

        self.durability -= damage
        if self.durability < 1:
            self.is_locked = False
            return "{} has destroyed the lock!".format(sender.alias())

        return "{} has damaged the lock a bit.".format(sender.alias())
