from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon

class Luminous(WeaponMod):
    Probability = 0.1
    Desirability = 4.0

    InventoryDescription = "Increases room's light level"
    BriefDescription = "The {EssentialPart} emanates a white light."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} is glows brightly."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} glows a bright white light."
    SensoryMinimalDescription = "You feel that the room is brighter."
    SensoryIdealDescription = "You sense that the {EssentialPart} has an enchantment of some sort which causes it to glow."
    DetailedMinimalDescription = "The {EssentialPart} glows a soft white light magically."
    DetailedIdealDescription = "The {SupportPart} supports bright white runes that cause the {EssentialPart} to radiate light, greatly illuminating the room."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = "Luminous " + weapon.name





