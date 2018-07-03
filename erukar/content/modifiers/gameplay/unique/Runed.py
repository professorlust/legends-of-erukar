from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Damage, DamageScalar
import erukar


class Runed(WeaponMod):
    Probability = 1
    PriceMod = 3.0

    InventoryName = "Runed"
    InventoryDescription = 'Channels arcane energy into attacks, adding additional arcane damage on hit'
    InventoryFlavorText = ''

    Requirement = 8
    EnergyPercentage = 0.05
    ScaleAmount = 1.75

    PersistentAttributes = ['raw_damage', 'scale_percentage']

    Glances = [
    ]

    Inspects = [
    ]

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition
    ]

    def get_additional_damages(self, weapon, is_attack=False):
        energy = int(weapon.owner.maximum_arcane_energy() * Runed.EnergyPercentage)
        if is_attack:
            if energy > weapon.owner.arcane_energy:
                return
            weapon.owner.arcane_energy -= energy
        yield Damage('arcane', [
            DamageScalar(
                energy,
                'acuity',
                scale_amount=Runed.ScaleAmount,
                requirement=Runed.Requirement)
        ])
