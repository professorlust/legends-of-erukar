from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Bronze(MaterialModifier):
    Probability = 0.05
    Desirability = 2.0

    def apply_to(self, item):
        item.name = 'Bronze ' + item.name

