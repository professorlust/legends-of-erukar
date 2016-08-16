from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Aluminum(MaterialModifier):
    Probability = 0.4
    ProbabilityFromFabrication = 0.1
    Desirability = 1.0

    def apply_to(self, item):
        item.name = 'Aluminum ' + item.name
