from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, ErukarActor
import random
import erukar


class Enhancement(WeaponMod):
    Probability = 1
    PriceMod = 1.75

    InventoryName = "Enhancement"
    InventoryFlavorText = ''
    ShouldRandomizeOnApply = True

    Glances = [
    ]

    Inspects = [
    ]

    PersistentAttributes = ['enhancement_type', 'InventoryName', 'InventoryDescription']

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Armor
    ]

    def randomize(self, parameters=None):
        self.enhancement_type = random.choice(ErukarActor.AttributeTypes)
        self.InventoryName = '{} Enhancement'.format(self.enhancement_type.capitalize())
        self.InventoryDescription = 'Provides +4 {}'.format(self.enhancement_type.capitalize())

    def on_alias(self, alias):
        return '{} of {} Enhancement'.format(alias, self.enhancement_type.capitalize())

    def apply_to(self, other):
        super().apply_to(other)
        setattr(self, self.enhancement_type, 4)
