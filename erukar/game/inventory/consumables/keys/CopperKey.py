from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class CopperKey(TieredKey):
    Probability = 32
    Tier = 'Copper'
    BasePrice = 100

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Copper().apply_to(self)
