from ...base.Potion import Potion
import erukar


class PotionOfProtectionFromIce(Potion):
    BaseName = "Potion of Protection From Ice"
    BriefDescription = "a transparent white potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Cryomorph,
            erukar.content.AddDeflection
        ]
