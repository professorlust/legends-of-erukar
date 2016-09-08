from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Brass(MaterialModifier):
    Probability = 0.05
    Desirability = 1.0

    def apply_to(self, item):
        super().apply_to(item)
        item.name = 'Brass ' + item.name
