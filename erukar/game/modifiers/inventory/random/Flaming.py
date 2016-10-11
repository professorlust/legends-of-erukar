from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
import numpy as np

class Flaming(WeaponMod):
    Probability = 1
    Desirability = 8.0
    BriefDescription = "flames erupt from the {EssentialPart}"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems to be on fire."
    VisualIdealDescription = "Jets of flames erupt from the {EssentialPart}, illuminating the room slightly."
    SensoryMinimalDescription = "You feel heat radiating from the {EssentialPart}. You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You feel heat radiating from the {BaseName}. You sense an elemental enchantment radiating from the {EssentialPart}."
    DetailedMinimalDescription = "Magical flames coat the {EssentialPart}, enveloping the room in heat."
    DetailedIdealDescription = "The {BaseName} has an Fire elemental enchantment, producing heat and jets of flames from the {EssentialPart}."
    Adjective = ""

    InventoryName = "Fire Elemental"
    InventoryDescription = "Adds a small amount of non-scaling fire damage to physical attacks"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name += " of the Flames"
        weapon.damages.append(Damage("Fire", [1,4], "", (np.random.uniform, (0,1))))
