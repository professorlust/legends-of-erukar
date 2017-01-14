from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class DiamondKey(TieredKey):
    Probability = 1
    Tier = 'Diamond'
    BasePrice = 3200

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Crystal().apply_to(self)
