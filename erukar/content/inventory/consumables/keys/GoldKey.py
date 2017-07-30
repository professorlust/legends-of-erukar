from erukar.system.engine import TieredKey
from erukar.content.modifiers import Gold

class GoldKey(TieredKey):
    Probability = 4
    Tier = 'Gold'
    BasePrice = 800

    def __init__(self):
        super().__init__()
        Gold().apply_to(self)
