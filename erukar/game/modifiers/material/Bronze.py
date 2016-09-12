from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Bronze(MaterialModifier):
    Probability = 200
    Desirability = 2.0

    BriefDescription = "a {BaseName} with a dark, unpolished metal {EssentialPart}"
    AbsoluteMinimalDescription = "The {EssentialPart} is made of a yellow metal."
    VisualMinimalDescription = "The {EssentialPart} of this {BaseName} is some sort of dark, unpolished metal which has a hint of yellow tint."
    VisualIdealDescription = "The dark and dull-yellow {EssentialPart} of the {BaseName} has been forged from Bronze."
    SensoryMinimalDescription = "The {BaseName} is significantly heavier than you expect."
    SensoryIdealDescription = "The {EssentialPart} has been made with a heavy alloy. Brushing the surface, you could tell that it is made of a difficult metal to forge."
    DetailedMinimalDescription = "The heavy {EssentialPart} is unpolished and rigid. It is made from a dark yellow metal pocked with forgeworking blemishes."
    DetailedIdealDescription = "The Bronze {EssentialPart} is unpolished, heavy, and full of imperfections. However, its craftsmanship is top notch."
    Adjective = "Bronze"
