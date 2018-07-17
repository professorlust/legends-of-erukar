from ...base.AutomagicModifier import AutomagicModifier
import erukar


class ElectricAura(AutomagicModifier):
    Probability = 1
    PriceMod = 1.7

    InventoryName = "Electric Aura"
    InventoryDescription = "Deals 10 lightning damage to all hostile creatures in a 3 unit radius every tick"
    InventoryFlavorText = ''

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor,
        erukar.system.Weapon
    ]

    def get_effects(self):
        return [
            erukar.content.PotionSource,
            erukar.content.Electromorph,
            erukar.content.RadialArea,
            erukar.content.InflictDamage
        ]

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Static-field ' + item.name
