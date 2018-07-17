from ...base.Potion import Potion
import erukar


class PotionOfProtectionFromAcid(Potion):
    BaseName = "Potion of Protection from Acid"
    BriefDescription = "a transparent blue potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Hydromorph,
            erukar.content.AddDeflection
        ]
