from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Wood(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Wood ' + item.name

