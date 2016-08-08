from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Atherite(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Atherite ' + item.name

