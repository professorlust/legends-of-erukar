from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Divinum(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Divinum ' + item.name

