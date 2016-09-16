from erukar.game.modifiers.inventory.Enhancement import Enhancement

class StrengthEnhancement(Enhancement):
    Probability = 0.333333
    Desirability = 4.0
    strength = 2
    StatEnhancement = "Strength Enhancement"

    InventoryDescription = "Strength +2"
    BriefDescription = "the {SupportPart} glows with red arcane runes"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} seems to glow in certain areas."
    VisualIdealDescription = "You see that the {SupportPart} is glowing with red arcane runes."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense Augmentation Magics emanating from the {SupportPart} of the {BaseName}."
    DetailedMinimalDescription = "You sense some sort of augmentation magic emanating from certain areas of the {BaseName}."
    DetailedIdealDescription = "The {BaseName}'s {SupportPart} is enchanted with red augmentation runes which enhance the user's Strength."
    Adjective = ""

