from ...base.Potion import Potion
import erukar


class PotionOfExplosions(Potion):
    BaseName = "Potion of Explosions"
    BriefDescription = "a test potion"

    def price(self, econ=None):
        return 0

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Pyromorph,
            erukar.content.RadialArea,
            erukar.content.InflictDamage
        ]
