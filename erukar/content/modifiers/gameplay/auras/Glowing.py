from ...base.LightManipulatingItemModifier import LightManipulatingItemModifier
from erukar.system.engine import Observation, Damage, DamageScalar
import erukar


class Glowing(LightManipulatingItemModifier):
    Probability = 1
    PriceMod = 1.3

    InventoryName = "Glowing"
    InventoryDescription = "This item radiates dim light"
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
        self.power = 0.5
        weapon.name = "Glowing " + weapon.name
