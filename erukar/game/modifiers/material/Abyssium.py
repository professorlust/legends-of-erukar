from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Abyssium(MaterialModifier):
    Probability = 400
    ProbabilityFromSanctity = -1.0
    Desirability = 2.0
    AbsoluteMinimalDescription = "The {EssentialPart} is a reddish black color."
    VisualMinimalDescription = "The {EssentialPart} has been carved out of a dark, reddish black stone that seems to glow a faint red color."
    VisualIdealDescription = "The {EssentialPart} of the {BaseName} has been carved out of a chunk of Abyssium. The dark red Abyssium {EssentialPart} seems to reflect a faint reddish light."
    SensoryMinimalDescription = "The {BaseName} makes you feel uneasy, even at a distance."
    SensoryIdealDescription = "You can sense that the {BaseName} is made of an unholy rock known as Abyssium."
    DetailedMinimalDescription = "The {EssentialPart} of the {BaseName} has been crafted out of a reddish black stone which emanates a faint red aura. You feel uneasy being in the same room as it."
    DetailedIdealDescription = "The {BaseName} uses an unholy stone called \"Abyssium\", from which the {EssentialPart} has been carved. The unholy {BaseName} consumes your optimism and fills it with dread."
    Adjective = "Abyssium"

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Abyssium ' + item.name
