from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Blessed(WeaponMod):
    Probability = 1
    Desirability = 2.0

    BriefDescription = ""
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = ""
    VisualIdealDescription = ""
    SensoryMinimalDescription = "The {SupportPart} feels spiritual."
    SensoryIdealDescription = "You feel a sense of holiness emanating from the {SupportPart}."
    DetailedMinimalDescription = "The {SupportPart} feels spiritual."
    DetailedIdealDescription = "You feel a sense of holiness emanating from the {SupportPart}."
    Adjective = ""

    InventoryDescription = "Deals 1.25x damage against demons and undead; 1.5x damage in holy areas"
    InventoryName = "Blessed"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Blessed " + weapon.name

