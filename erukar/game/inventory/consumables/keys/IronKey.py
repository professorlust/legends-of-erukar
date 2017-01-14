from erukar.engine.inventory.TieredKey import TieredKey
import erukar

class IronKey(TieredKey):
    Probability = 128
    Tier = 'Iron'
    BasePrice = 25

    def __init__(self):
        super().__init__()
        erukar.game.modifiers.material.Iron().apply_to(self)
