from erukar.system.engine import TieredKey
from erukar.content.modifiers import Copper

class CopperKey(TieredKey):
    Probability = 32
    Tier = 'Copper'
    BasePrice = 100

    def __init__(self):
        super().__init__()
        Copper().apply_to(self)
