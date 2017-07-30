from erukar.system.engine import TieredKey
from erukar.content.modifiers import Iron

class IronKey(TieredKey):
    Probability = 128
    Tier = 'Iron'
    BasePrice = 25

    def __init__(self):
        super().__init__()
        Iron().apply_to(self)
