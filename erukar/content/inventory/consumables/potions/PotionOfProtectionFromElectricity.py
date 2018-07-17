from ...base.Potion import Potion
import erukar


class PotionOfProtectionFromElectricity(Potion):
    BaseName = "Potion of Protection From Electricity"
    BriefDescription = "a transparent yellow potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Electromorph,
            erukar.content.AddDeflection
        ]
