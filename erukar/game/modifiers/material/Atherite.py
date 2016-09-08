from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Atherite(MaterialModifier):
    Probability = 200
    Desirability = 4.0

    BriefDescription = "a white {BaseName} which shimmers a faint blue light"
    AbsoluteMinimalDescription = "The {EssentialPart} is white."
    VisualMinimalDescription = "The {EssentialPart} of this {BaseName} is a whitish metal which shimmers a faint blue light."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} has been forged from a white, magical ore called Atherite which shimmers a faint blue light."
    SensoryMinimalDescription = "The {BaseName} gives off a slight sense of magic."
    SensoryIdealDescription = "The {BaseName}, specifically the {EssentialPart} which has been forged from a magical metal known as Atherite, gives off a feeling of chaotic magic."
    DetailedMinimalDescription = "The {EssentialPart} feels magical to you and has been forged from a whitish metal which shimmers a faint blue light."
    DetailedIdealDescription = "The {BaseName}'s {EssentialPart} has been forged from Atherite, a magical ore which is white and shimmers a blue light; you feel that this weapon possesses some link to magical chaos."
    Adjective = "Atherite"

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Atherite ' + item.name

