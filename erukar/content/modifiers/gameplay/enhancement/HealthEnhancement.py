from ...base.WeaponMod import WeaponMod
import erukar


class HealthEnhancement(WeaponMod):
    Probability = 1
    PriceMod = 2.5

    InventoryName = "Health Enhancement"
    InventoryDescription = 'Increases maximum health by 40'
    InventoryFlavorText = ''
    MaxHealthBonus = 40

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Armor
    ]

    def modify_maximum_health(self, item, _max):
        return _max + self.MaxHealthBonus
