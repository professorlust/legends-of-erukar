from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class SteelKey(TieredKey):
    Probability = 64
    Tier = 'Steel'

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Steel().apply_to(self)
