from erukar.game.modifiers.inventory.base.LightManipulatingItemModifier import LightManipulatingItemModifier

class Dark(LightManipulatingItemModifier):
    Probability = 0.2
    Desirability = 4.0

    AuraDescription = "Light seems to disappear unnaturally to {relative_direction}."
    InventoryDescription = "Reduces room's light level"
    BriefDescription = "The {EssentialPart} is draped in shadows."
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} is abnormally dark."
    VisualIdealDescription = "The {EssentialPart} is enveloped in darkness."
    SensoryMinimalDescription = "You feel that the room is slightly darker because of the {BaseName}."
    SensoryIdealDescription = "You sense that the {EssentialPart} has an enchantment of some sort which darkens the room."
    DetailedMinimalDescription = "The {EssentialPart} is covered in shadows which seem to darken the room."
    DetailedIdealDescription = "The {SupportPart} supports black runes that envelop the {EssentialPart} in shadows. The {BaseName} itself seems to steal light from the environment."
    Adjective = ""

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.aura_decay = 0.5
        self.aura_strength = 3
        self.light_power = 0.25
        weapon.name = "Dark " + weapon.name

