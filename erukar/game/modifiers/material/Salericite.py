from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Salericite(MaterialModifier):
    Probability = 0.05
    Desirability = 8.0

    def apply_to(self, item):
        item.name = 'Salericite ' + item.name
