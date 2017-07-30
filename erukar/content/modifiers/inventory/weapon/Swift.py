from ...base.WeaponMod import WeaponMod

class Swift(WeaponMod):
    Probability = 1
    Desirability = 2.0

    BriefDescription = ""
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = ""
    VisualIdealDescription = "There is a slight shimmer around the {EssentialPart} of the {BaseName}."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You feel that the {EssentialPart} is faster than it should be."
    DetailedMinimalDescription = "You sense magic emanating from the {BaseName}."
    DetailedIdealDescription = "The {EssentialPart} shimmers slightly from a magical enchantment which makes the {BaseName} more agile."
    Adjective = ""

    InventoryName = "Swift"
    InventoryDescription = "Increases dexterity scaling by 125%"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Swift " + weapon.name
