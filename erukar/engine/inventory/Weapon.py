from .Item import Item
from erukar.engine.model.Damage import Damage
import numpy as np

class Weapon(Item):
    BaseName = "Weapon"

    DamageRange = [1, 2]
    DamageType = "ambiguous"
    DamageModifier = ""

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    def __init__(self, name=""):
        if name == "":
            name = self.BaseName
        super().__init__("weapon", name)
        self.damages = [Damage(self.DamageType, list(self.DamageRange), self.DamageModifier, (self.Distribution, self.DistributionProperties))]

    def roll(self, attacker):
        return [(d.roll(attacker), d.name) for d in self.damages]

    def describe(self):
        return self.name

    def on_inspect(self):
        damage_desc = '\n'.join(['\t• {0} {1}'.format(d.damage, d.name) for d in self.damages])
        return '{0}\n{1}'.format(self.name, damage_desc)
