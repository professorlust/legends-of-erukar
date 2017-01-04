from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class GoldKey(TieredKey):
    Probability = 4
    Tier = 'Gold'

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Gold().apply_to(self)
