from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Ceramic(MaterialModifier):
    Probability = 200
    Desirability = 0.25

    InventoryName = 'Ceramic'
    InventoryDescription = 'Reduces durability to 10%; Lowers weight by 60%'
    BriefDescription = "a matte tan {BaseName}"
    AbsoluteMinimalDescription = "The {EssentialPart} is tan."
    VisualMinimalDescription = "The tan {EssentialPart} of this {BaseName} has dull, flat finish."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} has crafted from clay and kilned into a fine ceramic."
    SensoryMinimalDescription = "The {BaseName} is lightweight but feels highly fragile."
    SensoryIdealDescription = "The {EssentialPart} of the {BaseName} is light and feels like a kilned ceramic. You suspect that it is very fragile."
    DetailedMinimalDescription = "The lightweight ceramic of the {EssentialPart} has a matte tan finish. You suspect that it is likely fragile."
    DetailedIdealDescription = "The ceramic {EssentialPart} of the {BaseName} has been crafted with care. You suspect that, while likely fragile, it has the potential to enhance sharpness."
    Adjective = "Ceramic"

    def apply_to(self, item):
        super().apply_to(item)
        item.MaxDurability /= 10
