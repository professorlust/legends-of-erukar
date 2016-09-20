from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Wood(MaterialModifier):
    Probability = 0.05
    Desirability = 0.125

    InventoryDescription = "Lightweight and masterfully carved"
    BriefDescription = "a wooden {BaseName}"
    AbsoluteMinimalDescription = "The {EssentialPart} is made of wood."
    VisualMinimalDescription = "The {EssentialPart} of this {BaseName} is wood."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} has been carved out of a fine wood."
    SensoryMinimalDescription = ""
    SensoryIdealDescription = ""
    DetailedMinimalDescription = "The {EssentialPart} of this {BaseName} is wood."
    DetailedIdealDescription = "The {EssentialPart} of the {BaseName} has been carved out of a fine wood."
    Adjective = "Wooden"
