from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Holy(WeaponMod):
    Probability = 0.2
    Desirability = 4.0

    BriefDescription = ""
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = ""
    VisualIdealDescription = ""
    SensoryMinimalDescription = "The {SupportPart} feels spiritual."
    SensoryIdealDescription = "You feel a sense of holiness emanating from the {SupportPart}."
    DetailedMinimalDescription = "The {SupportPart} feels spiritual."
    DetailedIdealDescription = "You feel a sense of holiness emanating from the {SupportPart}."
    Adjective = ""

    InventoryDescription = "Deals 150% damage to undead and demons; creates a holy aura"
    InventoryName = "Holy"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Holy " + weapon.name


