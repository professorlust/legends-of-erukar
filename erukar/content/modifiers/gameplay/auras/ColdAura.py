from ...base.DamagingAuraModifier import DamagingAuraModifier
import erukar


class ColdAura(DamagingAuraModifier):
    Probability = 1
    PriceMod = 1.7

    InventoryName = "Cold Aura"
    InventoryDescription = "Deals 10 cold damage to all hostile creatures in a 3 unit radius every tick"
    InventoryFlavorText = ''

    DamageType = 'ice'
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
        item.name = 'Frost-emitting ' + item.name
