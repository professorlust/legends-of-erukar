from erukar.game.modifiers.inventory.Enhancement import Enhancement

class MinorStrengthEnhancement(Enhancement):
    Probability = 0.333333
    Desirability = 2.0
    strength = 1
    StatEnhancement = "Minor Strength Enhancement"

    InventoryDescription = "Strength +1"
    BriefDescription = "the {SupportPart} glows with red arcane runes"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} seems to glow in certain areas."
    VisualIdealDescription = "You see that the {SupportPart} is glowing with faint red arcane runes."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense weak Augmentation Magics emanating from the {SupportPart} of the {BaseName}."
    DetailedMinimalDescription = "You sense some sort of augmentation magic emanating from certain areas of the {BaseName}."
    DetailedIdealDescription = "The {BaseName}'s {SupportPart} is enchanted with faint red augmentation runes which slightly enhance the user's Strength."
    Adjective = ""

