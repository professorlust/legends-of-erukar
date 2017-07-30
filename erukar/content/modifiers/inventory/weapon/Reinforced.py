from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon
import math

class Reinforced(WeaponMod):
    Probability = 2
    Desirability = 0.0625
    
    DurabilityMuiltiplier = 1.5
    WeightMultiplier = 1.5

    InventoryDescription = "Increases maximum durability at the cost of increased weight"
    InventoryName = "Reinforced"

    def apply_to(self, weapon):
        weapon.name = "Reinforced " + weapon.name
        super().apply_to(weapon)

