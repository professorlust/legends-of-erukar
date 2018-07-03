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
            erukar.content.AddDeflection
        ]

    def get_kwargs(self):
        return {
            'damage_type': 'aqueous',
            'power': 20.0
        }
