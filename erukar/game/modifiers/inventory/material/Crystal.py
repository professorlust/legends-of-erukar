from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Crystal(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Crystal ' + item.name

