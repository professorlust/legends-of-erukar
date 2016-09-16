from erukar.game.modifiers.inventory.Enhancement import Enhancement

class AcuityEnhancement(Enhancement):
    Probability = 0.333333
    Desirability = 4.0
    StatEnhancement = "Acuity Enhancement"
    acuity = 2

    InventoryDescription = "Acuity +2"
    BriefDescription = "the {SupportPart} glows with blue arcane runes"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} seems to glow in certain areas."
    VisualIdealDescription = "You see that the {SupportPart} is glowing with blue arcane runes."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense Augmentation Magics emanating from the {SupportPart} of the {BaseName}."
    DetailedMinimalDescription = "You sense some sort of augmentation magic emanating from certain areas of the {BaseName}."
    DetailedIdealDescription = "The {BaseName}'s {SupportPart} is enchanted with blue augmentation runes which enhance the user's Acuity."
    Adjective = ""
