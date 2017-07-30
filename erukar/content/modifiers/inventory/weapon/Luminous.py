from ..base.LightManipulatingItemModifier import LightManipulatingItemModifier
from erukar.system.engine import Weapon

class Luminous(LightManipulatingItemModifier):
    Probability = 0.1
    Desirability = 4.0

    AuraDescription = "A Bright light pours into the room from {relative_direction}."
    BriefDescription = "The {EssentialPart} emanates a white light."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} is glows brightly."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} glows a bright white light."
    SensoryMinimalDescription = "You feel that the room is brighter."
    SensoryIdealDescription = "You sense that the {EssentialPart} has an enchantment of some sort which causes it to glow."
    DetailedMinimalDescription = "The {EssentialPart} glows a soft white light magically."
    DetailedIdealDescription = "The {SupportPart} supports bright white runes that cause the {EssentialPart} to radiate light, greatly illuminating the room."
    Adjective = ""

    InventoryName = "Luminous"
    InventoryDescription = "Adds runes which glow as bright as a torch"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.aura_decay = 0.5
        self.aura_strength = 6
        self.light_power = 0.5
        weapon.name = "Luminous " + weapon.name





