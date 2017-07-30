from erukar.system.engine import TieredKey
from erukar.content.modifiers import Bronze

class BronzeKey(TieredKey):
    Probability = 16
    BasePrice = 200
    Tier = 'Bronze'

    def __init__(self):
        super().__init__()
        Bronze().apply_to(self)
