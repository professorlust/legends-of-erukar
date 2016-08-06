from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Leather(MaterialModifier):
    Probability = 1.0

    def apply_to(self, item):
        item.name = 'Leather ' + item.name
