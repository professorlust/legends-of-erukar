from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Glowing(WeaponMod):
    Probability = 0.2
    Desirability = 4.0

    InventoryDescription = "Slightly increases room's light level"
    BriefDescription = "The {EssentialPart} glows a soft white."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} is seems to glow slightly."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} glows a soft white light."
    SensoryMinimalDescription = "You feel that the room is slightly more illuminated."
    SensoryIdealDescription = "You sense that the {EssentialPart} has an enchantment of some sort which causes it to glow."
    DetailedMinimalDescription = "The {EssentialPart} glows a soft white light magically."
    DetailedIdealDescription = "The {SupportPart} supports off-white runes that cause the {EssentialPart} to glow, illuminating the room in a soft white light."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Glowing " + weapon.name



