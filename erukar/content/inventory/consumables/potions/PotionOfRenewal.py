from ...base.Potion import Potion
import erukar


class PotionOfRenewal(Potion):
    BaseName = "Potion of Renewal"
    BriefDescription = "a orangeish potion"

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.AddEnergy
        ]

    def price(self, econ=None):
        return 30
