from erukar.system.engine import TieredKey
from erukar.content.modifiers import Crystal

class DiamondKey(TieredKey):
    Probability = 1
    Tier = 'Diamond'
    BasePrice = 3200

    def __init__(self):
        super().__init__()
        Crystal().apply_to(self)
