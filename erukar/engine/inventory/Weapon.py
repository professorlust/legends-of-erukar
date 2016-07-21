from .Item import Item
from erukar.engine.model.Damage import Damage
import numpy as np

class Weapon(Item):
    BaseName = "Weapon"
    AttackRange = 0 # Maximum number of rooms beyond our current room that we can reach
    RangePenalty = 5

    DamageRange = [1, 2]
    DamageType = "ambiguous"
    DamageModifier = ""

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    def __init__(self):
        super().__init__(self.BaseName)
        self.name = self.BaseName
        self.item_type = "weapon"
        self.equipment_locations = ['right','left']
        self.damages = [Damage(self.DamageType, list(self.DamageRange), self.DamageModifier,\
                               (self.Distribution, self.DistributionProperties))]

    def roll(self, attacker):
        return [(d.roll(attacker), d.name) for d in self.damages]

    def describe(self):
        return self.name

    def on_inspect(self):
        damage_desc = '\n'.join(['\t• {0} {1}'.format(d.damage,d.name) for d in self.damages])
        return '{0}\n{1}'.format(self.name, damage_desc)
