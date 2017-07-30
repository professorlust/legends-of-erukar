from erukar.system.engine import TieredKey
from erukar.content.modifiers import Platinum

class PlatinumKey(TieredKey):
    Probability = 2
    Tier = 'Platinum'
    BasePrice = 1600

    def __init__(self):
        super().__init__()
        Platinum().apply_to(self)
