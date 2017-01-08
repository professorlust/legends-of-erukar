from erukar.game.modifiers.MaterialModifier import MaterialModifier
from erukar import Weapon, Armor

class Leather(MaterialModifier):
    PermittedEntities = [Armor]
    ProhibitedEntities = [Weapon]
    Probability = 1.0
    Desirability = 2.0
    InventoryName = 'Leather'
