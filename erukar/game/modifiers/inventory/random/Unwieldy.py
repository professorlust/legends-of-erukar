from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Unwieldy(WeaponMod):
    Probability = 1
    Desirability = 0.5

    InventoryDescription = "-5 to attack rolls"
    BriefDescription = ""
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = ""
    VisualIdealDescription = "There is a slight shimmer around the {EssentialPart} of the {BaseName}."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You feel that the {EssentialPart} is slower than it should be."
    DetailedMinimalDescription = "You sense magic emanating from the {BaseName}."
    DetailedIdealDescription = "The {EssentialPart} shimmers slightly from a magical enchantment which makes the {BaseName} less agile."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Unwieldy " + weapon.name
