from ...base.AutomagicModifier import AutomagicModifier
import erukar


class MistAura(AutomagicModifier):
    Probability = 1
    PriceMod = 1.7

    InventoryName = "Acid Aura"
    InventoryDescription = "Deals 10 aqueous damage to all hostile creatures in a 3 unit radius every tick"
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
            erukar.content.Hydromorph,
            erukar.content.RadialArea,
            erukar.content.InflictDamage
        ]

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Misting ' + item.name
