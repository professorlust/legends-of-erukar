from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
from erukar.engine.model.Observation import Observation
import numpy as np

class Acid(WeaponMod):
    Probability = 1
    Desirability = 8.0

    InventoryName = "Acid Elemental"
    InventoryDescription = "Adds a small amount of non-scaling acid damage to physical attacks"

    Glances = [
        Observation(acuity=10, sense=0, result="with condensation on the {EssentialPart}"),
        Observation(acuity=25, sense=0, result="dripping with acid")
    ]

    Inspects = [
        Observation(acuity=10, sense=0, result="The {EssentialPart} has some sort of condensation on it."),
        Observation(acuity=25, sense=0, result="The {EssentialPart} is dripping with acid!")
    ]

    def apply_to(self, weapon):
        weapon.name = "Acid " + weapon.name
        weapon.damages.append(Damage("Acid", [1,4], "", (np.random.uniform, (0,1))))
        super().apply_to(weapon)
