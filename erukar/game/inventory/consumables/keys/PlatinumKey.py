from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class PlatinumKey(TieredKey):
    Probability = 2
    Tier = 'Platinum'
    BasePrice = 1600

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Platinum().apply_to(self)
