from erukar.game.modifiers.inventory.Enhancement import Enhancement

class DexterityEnhancement(Enhancement):
    Probability = 0.333333
    Desirability = 4.0
    StatEnhancement = "Dexterity Enhancement"
    dexterity = 2

    InventoryDescription = "Dexterity +2"
    BriefDescription = "the {SupportPart} glows with yellow arcane runes"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} seems to glow in certain areas."
    VisualIdealDescription = "You see that the {SupportPart} is glowing with yellow arcane runes."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense Augmentation Magics emanating from the {SupportPart} of the {BaseName}."
    DetailedMinimalDescription = "You sense some sort of augmentation magic emanating from certain areas of the {BaseName}."
    DetailedIdealDescription = "The {BaseName}'s {SupportPart} is enchanted with yellow augmentation runes which enhance the user's Dexterity."
    Adjective = ""

