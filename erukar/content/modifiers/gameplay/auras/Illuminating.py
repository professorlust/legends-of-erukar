from ...base.LightManipulatingItemModifier import LightManipulatingItemModifier
from erukar.system.engine import Observation, Damage, DamageScalar
import erukar


class Illuminating(LightManipulatingItemModifier):
    Probability = 1
    PriceMod = 1.7

    InventoryName = "Illuminating"
    InventoryDescription = "This item radiates light"
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
        self.max_distance = 8
        self.power = 0.8
        weapon.name = "Illuminated " + weapon.name
