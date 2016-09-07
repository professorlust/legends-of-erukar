from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Abyssium(MaterialModifier):
    Probability = 1000
    ProbabilityFromSanctity = -1.0
    Desirability = 2.0
    VisualMinimalDescription = "The {EssentialPart} has been carved out of a dark, reddish black stone that seems to glow a faint red color."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} has been carved out of a chunk of Abyssium. The dark red Abyssium {EssentialPart} seems to reflect a faint reddish light."
    SensoryMinimalDescription = "The {BaseName} makes you feel uneasy, even at a distance."
    SensoryIdealDescription = "You can sense that the {BaseName} is made of an unholy rock known as Abyssium."
    Adjective = "Abyssium"

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Abyssium ' + item.name
