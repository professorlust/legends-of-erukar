from ...base.Potion import Potion
import erukar, random

class PotionOfGreaterHealing(Potion):
    BaseName = "Potion of Greater Healing"
    BriefDescription = "a deep red potion"

    def price(self, econ=None):
        return 100

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.AddHealth
        ]

    def get_kwargs(self, effect_type):
        if effect_type == erukar.content.AddHealth:
            return {'range': (25, 50)}
        return {}
