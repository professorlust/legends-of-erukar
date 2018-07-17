from ...base.Potion import Potion
import erukar


class PotionOfResistanceToElectricity(Potion):
    BaseName = "Potion of Resistance to Electricity"
    BriefDescription = "a translucent yellow potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Electromorph,
            erukar.content.AddMitigation
        ]
