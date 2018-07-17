from ...base.Potion import Potion
import erukar


class PotionOfResistanceToFire(Potion):
    BaseName = "Potion of Resistance to Fire"
    BriefDescription = "a translucent red potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Pyromorph,
            erukar.content.AddMitigation
        ]
