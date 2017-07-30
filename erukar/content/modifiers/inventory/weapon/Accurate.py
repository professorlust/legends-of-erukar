from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon, Observation
import numpy as np

class Accurate(WeaponMod):
    Probability = 1
    Desirability = 8.0

    InventoryName = "Accurate"
    InventoryDescription = "+10 to Attack Rolls"

    Glances = [
    ]

    Inspects = [
    ]

    def on_calculate_attack_roll(self, result, target):
        return result + 10
        
