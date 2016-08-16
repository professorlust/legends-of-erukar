from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Negacite(MaterialModifier):
    Probability = 0.05
    Desirability = 8.0

    def apply_to(self, item):
        item.name = 'Negacite ' + item.name

