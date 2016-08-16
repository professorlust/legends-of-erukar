from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Glass(MaterialModifier):
    Probability = 0.05
    Desirability = 0.5

    def apply_to(self, item):
        item.name = 'Glass ' + item.name
