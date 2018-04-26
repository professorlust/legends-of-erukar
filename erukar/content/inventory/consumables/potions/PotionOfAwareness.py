from ...base.Potion import Potion
import erukar, random

class PotionOfAwareness(Potion):
    BaseName = "Potion of Awareness"
    BriefDescription = "a whitish-gold potion"

    def price(self, econ=None):
        return 110

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.InflictCondition
        ]

    def get_kwargs(self, effect_type):
        if effect_type == erukar.content.InflictCondition:
            return {'type': erukar.content.conditions.Wisened}
        return {}
