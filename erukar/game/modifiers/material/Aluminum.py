from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Aluminum(MaterialModifier):
    Probability = 200
    ProbabilityFromFabrication = 0.1
    Desirability = 1.0

    InventoryName = 'Aluminum'
    InventoryDescription = 'Lowers weight by 30%'
    BriefDescription = "a {BaseName} with a metallic gray {EssentialPart}"
    AbsoluteMinimalDescription = "The {EssentialPart} is an unpolished metallic gray."
    VisualMinimalDescription = "The {EssentialPart} has been forged with some sort of worked, gray metal."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} has been forged from an unpolished aluminum."
    SensoryMinimalDescription = "The {BaseName} is lighter than you anticipate."
    SensoryIdealDescription = "The {BaseName}, specifically the {EssentialPart} is much lighter than you anticipate when first lifting it."
    DetailedMinimalDescription = "The {EssentialPart} of the {BaseName} is very light, as it has been forged from some sort of unpolished aluminum."
    DetailedIdealDescription = "The {BaseName}'s {EssentialPart} has been forged from a sturdy and lightweight, yet unpolished, aluminum."
    Adjective = "Aluminum"

