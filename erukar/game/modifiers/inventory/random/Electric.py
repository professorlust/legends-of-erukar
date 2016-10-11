from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Electric(WeaponMod):
    Probability = 1
    Desirability = 8.0

    BriefDescription = "the {SupportPart} drips with acid"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems to be sparking."
    VisualIdealDescription = "Sparks and electrical arcs regularly dance off of the {EssentialPart} of the {BaseName}."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense an elemental enchantment radiating from the {EssentialPart}."
    DetailedMinimalDescription = "The {EssentialPart} seems to be magically producing sparks."
    DetailedIdealDescription = "The {BaseName} has an Electrical elemental enchantment, producing jolts of electricity and sparks from the {EssentialPart}."
    Adjective = ""

    InventoryName = "Electric Elemental"
    InventoryDescription = "Adds a small amount of non-scaling electric damage to physical attacks"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name += " of Lightning"
        weapon.damages.append(Damage("Electric", [1,4], "", (np.random.uniform, (0,1))))
