from ...base.WeaponMod import WeaponMod

class Serrated(WeaponMod):
    Probability = 1
    Desirability = 1
    BriefDescription = "The {EssentialPart} is serrated."
    AbsoluteMinimalDescription = "The {EssentialPart} is serrated."
    VisualMinimalDescription = "The {EssentialPart} is serrated."
    VisualIdealDescription = "The {EssentialPart} is serrated."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} is serrated."
    DetailedIdealDescription = "The {EssentialPart} is serrated."
    Adjective = ""

    InventoryName = "Serrated"
    InventoryDescription = "Converts 25% of Slashing damage to scalable Piercing damage"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Serrated " + weapon.name
