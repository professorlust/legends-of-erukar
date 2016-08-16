from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Iron(MaterialModifier):
    Probability = 0.05
    Desirability = 1.0

    def apply_to(self, item):
        item.name = 'Iron ' + item.name

