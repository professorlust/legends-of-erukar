from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Sharp(WeaponMod):
    Probability = 1
    Desirability = 1
    InventoryDescription = "Bypasses some metal protection"
    BriefDescription = "The {EssentialPart} is sharp."
    AbsoluteMinimalDescription = "The {EssentialPart} is sharp."
    VisualMinimalDescription = "The {EssentialPart} is sharp."
    VisualIdealDescription = "The {EssentialPart} is sharp."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} is sharp."
    DetailedIdealDescription = "The {EssentialPart} is sharp."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Sharp " + weapon.name


