from ...base.Potion import Potion
import erukar


class FoulLiquid(Potion):
    BaseName = "Foul Liquid"
    BriefDescription = "A murky, tar-like liquid from the depths of Ulgavoth'"

    def price(self, econ=None):
        return 15

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Daemomorph,
            erukar.content.CreateSanctityAura
        ]
