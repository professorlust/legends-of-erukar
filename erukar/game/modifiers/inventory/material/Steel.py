from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Steel(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Steel ' + item.name

