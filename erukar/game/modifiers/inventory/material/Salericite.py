from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Salericite(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Salericite ' + item.name

