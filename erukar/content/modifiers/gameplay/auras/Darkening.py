from ...base.LightManipulatingItemModifier import LightManipulatingItemModifier
from erukar.system.engine import Weapon, Observation, Damage, DamageScalar
import erukar


class Darkening(LightManipulatingItemModifier):
    Probability = 1
    PriceMod = 1.6

    InventoryName = "Darkening"
    InventoryDescription = "Absorbs and decays light nearby, darkening the area significantly"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
        erukar.system.Weapon,
        erukar.system.Ammunition
    ]

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.max_distance = 3
        self.power = -1.0
        weapon.name = "Darkened " + weapon.name
