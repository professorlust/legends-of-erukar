from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Ceramic(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Ceramic ' + item.name

