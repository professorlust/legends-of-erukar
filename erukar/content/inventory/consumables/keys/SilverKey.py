from erukar.system.engine import TieredKey
from erukar.content.modifiers import Silver

class SilverKey(TieredKey):
    Probability = 8
    Tier = 'Silver'
    BasePrice = 400

    def __init__(self):
        super().__init__()
        Silver().apply_to(self)
