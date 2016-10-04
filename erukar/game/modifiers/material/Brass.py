from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Brass(MaterialModifier):
    Probability = 200
    Desirability = 1.0

    InventoryName = 'Brass'
    InventoryDescription = 'Decreases weight by 10%; Decreases Durability by 5%'
    BriefDescription = "a metallic yellow {BaseName}"
    AbsoluteMinimalDescription = "The {EssentialPart} is made of a yellow metal."
    VisualMinimalDescription = "The {EssentialPart} of this {BaseName} is nicely polished yellow metal."
    VisualIdealDescription = "The reflective yellow {EssentialPart} of the {BaseName} has been forged from Brass."
    SensoryMinimalDescription = "The {BaseName} appears to be made of an expensive metal."
    SensoryIdealDescription = "The {EssentialPart} appears to be made of gold, but is too light. You suspect it may be made of Brass."
    DetailedMinimalDescription = "The semi-reflective yellow metal {EssentialPart} appears expensive, but is too light to be made of Gold."
    DetailedIdealDescription = "The metallic {EssentialPart} has been forged from Brass, making it a lightweight yet resilient {BaseName}."
    Adjective = "Brass"
