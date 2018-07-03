from ...base.Potion import Potion
import erukar


class PotionOfCourage(Potion):
    BaseName = "Potion of Courage"
    BriefDescription = "a dark green potion"

    def price(self, econ=None):
        return 110

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.InflictCondition
        ]

    def get_kwargs(self):
        return {'type': erukar.content.conditions.Inspired}
