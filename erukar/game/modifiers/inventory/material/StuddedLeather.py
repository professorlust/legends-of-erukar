from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar import Weapon

class StuddedLeather(MaterialModifier):
    Probability = 0.05
    Desirability = 2.0

    def __init__(self):
        super().__init__()
        self.prohibited_entities = [Weapon]

    def apply_to(self, item):
        item.name = 'Studded Leather ' + item.name

