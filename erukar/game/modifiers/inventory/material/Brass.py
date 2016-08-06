from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Brass(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Brass ' + item.name
