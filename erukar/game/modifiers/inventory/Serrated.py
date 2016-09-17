from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Serrated(WeaponMod):
    Probability = 1
    Desirability = 1
    InventoryDescription = "Bypasses some leather protection"
    BriefDescription = "The {EssentialPart} is serrated."
    AbsoluteMinimalDescription = "The {EssentialPart} is serrated."
    VisualMinimalDescription = "The {EssentialPart} is serrated."
    VisualIdealDescription = "The {EssentialPart} is serrated."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} is serrated."
    DetailedIdealDescription = "The {EssentialPart} is serrated."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Serrated " + weapon.name
