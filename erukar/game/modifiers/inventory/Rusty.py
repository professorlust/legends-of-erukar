from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Rusty(WeaponMod):
    Probability = 5
    Desirability = 0.125
    InventoryDescription = "Reduces efficacy"
    BriefDescription = "{EssentialPart} is rusty."
    AbsoluteMinimalDescription = "The {EssentialPart} is covered in rust."
    VisualMinimalDescription = "The {EssentialPart} is covered in rust."
    VisualIdealDescription = "The {EssentialPart} is covered in rust."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} is covered in rust."
    DetailedIdealDescription = "The {EssentialPart} is covered in rust."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.damages[0].damage[1] -= 1
        weapon.name = "Rusty " + weapon.name
