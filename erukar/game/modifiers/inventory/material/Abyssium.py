from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Abyssium(MaterialModifier):
    Probability = 0.1
    ProbabilityFromSanctity = -1.0
    Desirability = 2.0 

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Abyssium ' + item.name
