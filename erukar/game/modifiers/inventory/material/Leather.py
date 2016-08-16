from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar import Weapon

class Leather(MaterialModifier):
    Probability = 1.0
    Desirability = 2.0

    def __init__(self):
        super().__init__()
        self.prohibited_entities = [Weapon]

    def apply_to(self, item):
        item.name = 'Leather ' + item.name
