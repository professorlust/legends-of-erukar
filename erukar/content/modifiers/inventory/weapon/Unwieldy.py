from ...base.WeaponMod import WeaponMod

class Unwieldy(WeaponMod):
    Probability = 1
    Desirability = 0.5

    BriefDescription = ""
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = ""
    VisualIdealDescription = "There is a slight shimmer around the {EssentialPart} of the {BaseName}."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You feel that the {EssentialPart} is slower than it should be."
    DetailedMinimalDescription = "You sense magic emanating from the {BaseName}."
    DetailedIdealDescription = "The {EssentialPart} shimmers slightly from a magical enchantment which makes the {BaseName} less agile."
    Adjective = ""

    InventoryName = "Swift"
    InventoryDescription = "Reduces dexterity scaling to 67%"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Unwieldy " + weapon.name
