from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Small(WeaponMod):
    Probability = 1
    Desirability = 0.5

    BriefDescription = "The {EssentialPart} is disproportionately small."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {EssentialPart} seems small."
    VisualIdealDescription = "The {EssentialPart} is disproportionately small in comparison to the rest of the {BaseName}."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} seems small."
    DetailedIdealDescription = "The {EssentialPart} is disproportionately small in comparison to the rest of the {BaseName}."
    Adjective = ""

    InventoryDescription = "Reduces weight by 20%; changes strength scaling to 67%, dexterity scaling to 125%"
    InventoryName = "Small"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Small " + weapon.name
        if 'strength' in weapon.stat_influences:
            weapon.stat_influences['strength']['max_scale'] *= 0.667
        if 'dexterity' in weapon.stat_influences:
            weapon.stat_influences['dexterity']['max_scale'] *= 1.25
