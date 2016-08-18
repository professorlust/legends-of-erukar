from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar import Weapon, Armor

class Chainmail(MaterialModifier):
    ProhibitedEntities = [Weapon]
    PermittedEntities = [Armor]
    Probability = 0.05
    Desirability = 2.0

    def apply_to(self, item):
        item.name = 'Chainmail ' + item.name

