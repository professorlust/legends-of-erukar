from ...base.Potion import Potion
import erukar


class PotionOfSkeletalSummoning(Potion):
    BaseName = "Potion of Skeletal Summoning"
    BriefDescription = "a test potion"

    def price(self, econ=None):
        return 0

    def __init__(self, quantity=1):
        super().__init__(quantity)
        self.effects = [
            erukar.content.PotionSource,
            erukar.content.Summon
        ]
