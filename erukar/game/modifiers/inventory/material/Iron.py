from erukar.game.modifiers.MaterialModifier import MaterialModifier

class Iron(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'Iron ' + item.name

