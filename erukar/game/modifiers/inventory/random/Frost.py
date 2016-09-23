from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Frost(WeaponMod):
    Probability = 1
    Desirability = 8.0
    InventoryDescription = "[1, 4] Cold Damage"
    BriefDescription = "frost coats the {EssentialPart}"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems to be covered in frost."
    VisualIdealDescription = "The {BaseName} is coated in a white frost, and on closer look you believe the {EssentialPart} may actually be ice."
    SensoryMinimalDescription = "You feel cold. You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You feel cold. You sense an elemental enchantment radiating from the {EssentialPart}."
    DetailedMinimalDescription = "Magical frost envelops the {EssentialPart}, draining the heat from the room."
    DetailedIdealDescription = "The {BaseName} has a Frost elemental enchantment, draining the heat from the room and coating the {EssentialPart} with thick layers of frost."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Frosted " + weapon.name
        weapon.damages.append(Damage("Cold", [1,4], "", (np.random.uniform, (0,1))))
