from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Magicite(MaterialModifier):
    Probability = 0.05
    Desirability = 8.0

    def apply_to(self, item):
        item.name = 'Magicite ' + item.name

