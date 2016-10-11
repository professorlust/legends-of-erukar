from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Large(WeaponMod):
    Probability = 1
    Desirability = 2.0

    BriefDescription = "The {EssentialPart} is disproportionately large."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems large."
    VisualIdealDescription = "The {EssentialPart} is disproportionately large in comparison to the rest of the {BaseName}."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} seems large."
    DetailedIdealDescription = "The {EssentialPart} is disproportionately large in comparison to the rest of the {BaseName}."
    Adjective = ""

    InventoryDescription = "Increases weight by 20%; changes dexterity scaling to 67%, strength scaling to 125%"
    InventoryName = "Large"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Large " + weapon.name
        if 'strength' in weapon.stat_influences:
            weapon.stat_influences['strength']['max_scale'] *= 1.25
        if 'dexterity' in weapon.stat_influences:
            weapon.stat_influences['dexterity']['max_scale'] *= 0.667
