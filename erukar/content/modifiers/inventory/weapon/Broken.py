from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon
import math

class Broken(WeaponMod):
    Probability = 2
    Desirability = 0.0625
    InventoryDescription = "Drastically reduces efficacy"
    BriefDescription = "{EssentialPart} is broken."
    AbsoluteMinimalDescription = "The {EssentialPart} has been broken."
    VisualMinimalDescription = "The {EssentialPart} has been broken."
    VisualIdealDescription = "The {EssentialPart} has been broken."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} has been broken."
    DetailedIdealDescription = "The {EssentialPart} has been broken."
    Adjective = ""

    DurabilityMuiltiplier = 0

    InventoryDescription = "Removes minimum damage, halves maximum, and removes scaling"
    InventoryName = "Broken"

    def apply_to(self, weapon):
        weapon.name = "Broken " + weapon.name
        weapon.stat_influences = {}
        max_dam = weapon.damages[0].damage[1]
        weapon.damages[0].damage = [0, int(math.floor(max_dam/2))]
        super().apply_to(weapon)
