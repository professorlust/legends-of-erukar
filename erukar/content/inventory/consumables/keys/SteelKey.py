from erukar.system.engine import TieredKey
from erukar.content.modifiers import Steel

class SteelKey(TieredKey):
    Probability = 64
    Tier = 'Steel'
    BasePrice = 50

    def __init__(self):
        super().__init__()
        Steel().apply_to(self)
