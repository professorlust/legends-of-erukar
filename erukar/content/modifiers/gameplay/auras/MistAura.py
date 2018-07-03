from ...base.DamagingAuraModifier import DamagingAuraModifier
from erukar.system.engine import Damage, DamageScalar, Lifeform
import erukar


class MistAura(DamagingAuraModifier):
    Probability = 1
    PriceMod = 1.7

    InventoryName = "Acid Aura"
    InventoryDescription = "Deals 10 aqueous damage to all hostile creatures in a 3 unit radius every tick"
    InventoryFlavorText = ''

    DamageType = 'aqueous'
    RawDamage = 10
    ScalarStat = 'acuity'
    ScaleAmount = 1.5
    Requirement = 0

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
        erukar.system.Weapon
    ]

    def apply_to(self, item):
        super().apply_to(item)
        self.max_distance = 3
        self.power = 1.0
        item.name = 'Misting ' + item.name
