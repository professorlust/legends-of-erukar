from ...base.Potion import Potion
import erukar


class PotionOfCamouflage(Potion):
    BaseName = "Potion of Camouflage"
    BriefDescription = "a clear potion"

    def price(self, econ=None):
        return 200

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.InflictCondition
        ]

    def get_kwargs(self):
        return {'type': erukar.content.conditions.Cloaked}
