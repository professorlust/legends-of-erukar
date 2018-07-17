import erukar
from erukar.system.engine import Merchant


class Alchemist(Merchant):
    def __init__(self, world):
        super().__init__(world)
        self.desired_item_types = [
            erukar.content.Potion,
        ]

    def interaction_text(self):
        return 'Trade with Alchemist {}'.format(self.npc.alias())

    def standard_inventory(self):
        return [
            erukar.content.PotionOfHealing(50),
            erukar.content.PotionOfRenewal(50),
            erukar.content.PotionOfGreaterHealing(25),
            erukar.content.PotionOfBolstering(10),
            erukar.content.PotionOfGrace(10),
            erukar.content.PotionOfEndurance(10),
            erukar.content.PotionOfBrilliance(10),
            erukar.content.PotionOfAwareness(10),
            erukar.content.PotionOfCourage(10),
            erukar.content.FoulLiquid(25),
            erukar.content.HolyWater(25),
            erukar.content.PotionOfProtectionFromFire(10),
            erukar.content.PotionOfProtectionFromIce(10),
            erukar.content.PotionOfProtectionFromElectricity(10),
            erukar.content.PotionOfProtectionFromAcid(10),
            erukar.content.PotionOfResistanceToFire(10),
            erukar.content.PotionOfResistanceToIce(10),
            erukar.content.PotionOfResistanceToElectricity(10),
            erukar.content.PotionOfResistanceToAcid(10),
            erukar.content.PotionOfSkeletalSummoning(200),
            erukar.content.PotionOfExplosions(200)
        ]
