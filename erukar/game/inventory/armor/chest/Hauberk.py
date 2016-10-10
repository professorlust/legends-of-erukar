from erukar.engine.inventory.Armor import Armor

class Hauberk(Armor):
    EquipmentLocations = ['chest']
    BaseName="Hauberk"
    Probability = 1
    DexterityPenalty = 3
    DamageMitigations = {
        # type, mitigation percent, glancing range
        'slashing': (0.12, 6),
        'piercing': (0.075, 3)
    }

    def __init__(self):
        super().__init__("Hauberk")
        self.armor_class_modifier = 7
        self.max_dex_mod = 20
