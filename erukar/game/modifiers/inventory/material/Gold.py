from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Gold(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Gold ' + item.name

