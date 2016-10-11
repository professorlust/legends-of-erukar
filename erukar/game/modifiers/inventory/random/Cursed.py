from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Cursed(WeaponMod):
    Probability = 1
    Desirability = 2.0

    InventoryDescription = "Strong against holy creatures"
    BriefDescription = ""
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = ""
    VisualIdealDescription = ""
    SensoryMinimalDescription = "The {SupportPart} feels cursed."
    SensoryIdealDescription = "You feel a sense of unholiness emanating from the {SupportPart}."
    DetailedMinimalDescription = "The {SupportPart} feels cursed."
    DetailedIdealDescription = "You feel a sense of unholiness emanating from the {SupportPart}."
    Adjective = ""

    InventoryDescription = "To be determined"
    InventoryName = "Cursed"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Cursed " + weapon.name



