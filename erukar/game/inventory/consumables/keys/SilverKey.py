from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class SilverKey(TieredKey):
    Probability = 8
    Tier = 'Silver'
    BasePrice = 400

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Silver().apply_to(self)
