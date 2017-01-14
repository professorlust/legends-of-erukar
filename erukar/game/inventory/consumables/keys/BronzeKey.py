from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class BronzeKey(TieredKey):
    Probability = 16
    BasePrice = 200
    Tier = 'Bronze'

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Bronze().apply_to(self)
