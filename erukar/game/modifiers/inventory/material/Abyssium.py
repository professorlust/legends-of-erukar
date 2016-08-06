from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Abyssium(MaterialModifier):
    Probability = 0.1
    ProbabilityFromSanctity = -1.0

    def apply_to(self, item):
        item.name = 'Abyssium ' + item.name
