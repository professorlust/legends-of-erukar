from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Small(WeaponMod):
    Probability = 1
    Desirability = 0.5

    InventoryDescription = "Cosmetic"
    BriefDescription = "The {EssentialPart} is disproportionately small."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems small."
    VisualIdealDescription = "The {EssentialPart} is disproportionately small in comparison to the rest of the {BasePart}."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} seems small."
    DetailedIdealDescription = "The {EssentialPart} is disproportionately small in comparison to the rest of the {BasePart}."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Small " + weapon.name
