from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar import Weapon

class Chainmail(MaterialModifier):
    ProhibitedEntities = [Weapon]
    Probability = 0.05
    Desirability = 2.0

    def apply_to(self, item):
        item.name = 'Chainmail ' + item.name

