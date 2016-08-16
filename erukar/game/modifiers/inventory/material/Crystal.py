from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Crystal(MaterialModifier):
    Probability = 0.05
    Desirability = 16.0

    def apply_to(self, item):
        item.name = 'Crystal ' + item.name

