from ...base.Potion import Potion
import erukar


class PotionOfResistanceToIce(Potion):
    BaseName = "Potion of Resistance to Ice"
    BriefDescription = "a translucent white potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.AddMitigation
        ]

    def get_kwargs(self):
        return {
            'damage_type': 'ice',
            'percent': 0.20
        }
