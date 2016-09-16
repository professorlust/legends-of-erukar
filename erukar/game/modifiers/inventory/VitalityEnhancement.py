from erukar.game.modifiers.inventory.Enhancement import Enhancement

class VitalityEnhancement(Enhancement):
    Probability = 0.333333
    Desirability = 4.0
    vitality = 2
    StatEnhancement = "Vitality Enhancement"

    InventoryDescription = "Vitality +2"
    BriefDescription = "the {SupportPart} glows with orange arcane runes"
    AbsoluteMinimalDescription = ""
    VisualMinimalDescription = "The {BaseName} seems to glow in certain areas."
    VisualIdealDescription = "You see that the {SupportPart} is glowing with orange arcane runes."
    SensoryMinimalDescription = "You sense magic emanating from the {BaseName}."
    SensoryIdealDescription = "You sense Augmentation Magics emanating from the {SupportPart} of the {BaseName}."
    DetailedMinimalDescription = "You sense some sort of augmentation magic emanating from certain areas of the {BaseName}."
    DetailedIdealDescription = "The {BaseName}'s {SupportPart} is enchanted with orange augmentation runes which enhance the user's Vitality."
    Adjective = ""

