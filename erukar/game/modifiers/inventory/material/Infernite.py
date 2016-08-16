from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Infernite(MaterialModifier):
    Probability = 0.05
    Desirability = 4.0

    def apply_to(self, item):
        item.name = 'Infernite ' + item.name

