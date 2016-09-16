from erukar.game.modifiers.inventory.Enhancement import Enhancement

class MinorVitalityEnhancement(Enhancement):
    Probability = 0.333333
    Desirability = 2.0
    vitality = 1
    StatEnhancement = "Minor Vitality Enhancement"

    InventoryDescription = "Vitality +1"
    BriefDescription = "the {SupportPart} glows with yellow arcane runes"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} seems to glow in certain areas."
    VisualIdealDescription = "You see that the {SupportPart} is glowing with faint yellow arcane runes."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense weak Augmentation Magics emanating from the {SupportPart} of the {BaseName}."
    DetailedMinimalDescription = "You sense some sort of augmentation magic emanating from certain areas of the {BaseName}."
    DetailedIdealDescription = "The {BaseName}'s {SupportPart} is enchanted with faint yellow augmentation runes which slightly enhance the user's Vitality."
    Adjective = ""

