from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Infernite(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Infernite ' + item.name

