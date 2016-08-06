from erukar.game.modifiers.MaterialModifier import MaterialModifier

class StuddedLeather(MaterialModifier):
    Probability = 0.05

    def apply_to(self, item):
        item.name = 'StuddedLeather ' + item.name

