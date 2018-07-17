from ...base.Potion import Potion
import erukar


class HolyWater(Potion):
    BaseName = "Holy Water"
    BriefDescription = "Clear liquid blessed by Aegis"

    def price(self, econ=None):
        return 15

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Divinomorph,
            erukar.content.CreateSanctityAura
        ]

    def get_kwargs(self):
        return {'sanctity': 1}
