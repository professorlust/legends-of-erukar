from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Large(WeaponMod):
    Probability = 1
    Desirability = 2.0

    InventoryDescription = "Cosmetic"
    BriefDescription = "The {EssentialPart} is disproportionately large."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems large."
    VisualIdealDescription = "The {EssentialPart} is disproportionately large in comparison to the rest of the {BasePart}."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} seems large."
    DetailedIdealDescription = "The {EssentialPart} is disproportionately large in comparison to the rest of the {BasePart}."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Large " + weapon.name
