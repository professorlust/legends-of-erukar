from ...base.Potion import Potion
import erukar, random

class PotionOfHealing(Potion):
    BaseName = "Potion of Healing"
    BriefDescription = "a reddish potion"

    def price(self, econ=None):
        return 25

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.AddHealth
        ]
