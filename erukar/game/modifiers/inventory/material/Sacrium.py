from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Sacrium(MaterialModifier):
    Probability = 0.05
    Desirability = 4.0

    def apply_to(self, item):
        item.name = 'Sacrium ' + item.name

