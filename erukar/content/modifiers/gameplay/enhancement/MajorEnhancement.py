from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation, ErukarActor
import random
import erukar


class MajorEnhancement(WeaponMod):
    Probability = 1
    PriceMod = 2.0

    InventoryName = "Major Enhancement"
    InventoryFlavorText = ''
    ShouldRandomizeOnApply = True

    Glances = [
    ]

    Inspects = [
    ]

    PersistentAttributes = ['enhancement_type', 'InventoryName', 'InventoryDescription']

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition
    ]

    def randomize(self, parameters=None):
        self.enhancement_type = random.choice(ErukarActor.AttributeTypes)
        self.InventoryName = 'Major {} Enhancement'.format(self.enhancement_type.capitalize())
        self.InventoryDescription = 'Provides +6 {}'.format(self.enhancement_type.capitalize())

    def on_alias(self, alias):
        return '{} of Major {} Enhancement'.format(alias, self.enhancement_type.capitalize())

    def apply_to(self, other):
        super().apply_to(other)
        setattr(self, self.enhancement_type, 6)
