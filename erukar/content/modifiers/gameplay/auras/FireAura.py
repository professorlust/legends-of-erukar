from ...base.AutomagicModifier import AutomagicModifier
import erukar


class FireAura(AutomagicModifier):
    Probability = 1
    PriceMod = 1.7

    InventoryName = "Fire Aura"
    InventoryDescription = "Deals 10 fire damage to all hostile creatures in a 3 unit radius every tick"
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
            erukar.content.Pyromorph,
            erukar.content.RadialArea,
            erukar.content.InflictDamage
        ]

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Sweltering ' + item.name
