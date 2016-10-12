from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Acid(WeaponMod):
    Probability = 1
    Desirability = 8.0

    InventoryName = "Acid Elemental"
    InventoryDescription = "Adds a small amount of non-scaling acid damage to physical attacks"

    BriefDescription = "{alias} dripping with acid"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} has some sort of translucent green condensation on it."
    VisualIdealDescription = "You see that the {EssentialPart} has acid condensation on it."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense an elemental enchantment radiating from the {EssentialPart}."
    DetailedMinimalDescription = "The {EssentialPart} seems to have some sort of magical, translucent green condensation on it."
    DetailedIdealDescription = "The {BaseName} has an Acid elemental enchantment, producing translucent green acid condensation on the {EssentialPart}."
    Adjective = ""

    def apply_to(self, weapon):
        weapon.name = "Acid " + weapon.name
        weapon.damages.append(Damage("Acid", [1,4], "", (np.random.uniform, (0,1))))
        super().apply_to(weapon)
