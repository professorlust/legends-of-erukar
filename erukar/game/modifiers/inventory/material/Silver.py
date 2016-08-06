from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Silver(MaterialModifier):
    Probability = 0.25

    def apply_to(self, item):
        item.name = 'Silver ' + item.name

