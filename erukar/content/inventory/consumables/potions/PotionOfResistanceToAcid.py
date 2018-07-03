from ...base.Potion import Potion
import erukar


class PotionOfResistanceToAcid(Potion):
    BaseName = "Potion of Resistance to Acid"
    BriefDescription = "a translucent blue potion"

    def price(self, econ=None):
        return 1

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.AddMitigation
        ]

    def get_kwargs(self):
        return {
            'damage_type': 'aqueous',
            'percent': 0.20
        }
