from erukar.system.engine import StackableItem
import erukar

class Potion(StackableItem):
    Persistent = True
    BaseName = "Potion"
    BriefDescription = "a red potion"


    def __init__(self, quantity=1):
        super().__init__(self.BaseName, quantity)
        self.source = None
        self.effect = None

    def alias(self):
        return 'Potion'

    def price(self):
        return self.BasePrice * self.effect.PotionPriceMultiplier
