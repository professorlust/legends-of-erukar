from ...base.Potion import Potion
import erukar


class PotionOfEndurance(Potion):
    BaseName = "Potion of Endurance"
    BriefDescription = "a translucent red potion"

    def price(self, econ=None):
        return 110

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.InflictCondition
        ]

    def get_kwargs(self):
        return {'type': erukar.content.conditions.Fortified}
