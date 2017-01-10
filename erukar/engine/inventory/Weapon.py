from .Item import Item
from erukar.engine.model.Damage import Damage
import numpy as np

class Weapon(Item):
    Persistent = True
    BaseName = "Weapon"
    EssentialPart = "weapon"
    AttackRange = 0 # Maximum number of rooms beyond our current room that we can reach
    RangePenalty = 5
    EquipmentLocations = ['right','left']

    DamageRange = [1, 2]
    DamageType = "ambiguous"
    DamageModifier = ""

    Distribution = np.random.uniform
    DistributionProperties = (0, 1)

    SuccessfullyAttackWith = 'Your attack hits {target}!'
    YouAreHitBy = 'You are hit by {subject}\'s {weapon_name}!'

    def __init__(self):
        super().__init__(self.BaseName)
        self.name = self.BaseName
        self.item_type = "weapon"
        self.damages = [Damage(self.DamageType, list(self.DamageRange), self.DamageModifier,\
                               (self.Distribution, self.DistributionProperties), scales=True)]

    def roll(self, attacker):
        efficacy = self.efficacy_for(attacker)
        return [(d.roll(attacker)*efficacy if d.scales else d.roll(attacker), d.name) for d in self.damages]

    def on_inventory(self):
        return '{} ({}%)'.format(self.format(), int(100*self.durability_coefficient))

    def on_inventory_inspect(self, lifeform):
        scale = self.efficacy_for(lifeform)
        mod = lifeform.get(self.DamageModifier)
        name = '{} ({} / {})'.format(self.format(), int(self.durability()), int(self.max_durability()))
        damage_desc = '\n'.join(['{:>11} {} to {} {} Damage'.format('•',
            int((mod if d.scales else 0) + d.damage[0]*scale),
            int((mod if d.scales else 0) + d.damage[1]*scale), d.name)
            for d in self.damages])
        mods = ([self.material] + self.modifiers) if self.material else self.modifiers
        mod_desc = '\n'.join(['{:>11} {}: {}'.format('•',d.InventoryName, d.mutate(d.InventoryDescription)) for d in mods])
        return '\n'.join([name, damage_desc, mod_desc])
