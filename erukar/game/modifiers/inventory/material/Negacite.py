from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Negacite(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Negacite ' + item.name

