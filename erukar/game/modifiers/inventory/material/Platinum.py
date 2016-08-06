from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Platinum(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Platinum ' + item.name
