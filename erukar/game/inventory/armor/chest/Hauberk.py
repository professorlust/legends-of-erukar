from erukar.engine.inventory.Armor import Armor

class Hauberk(Armor):
    EquipmentLocations = ['chest']
    BaseName="Hauberk"
    Probability = 1

    def __init__(self):
        super().__init__("Hauberk")
        self.armor_class_modifier = 7
        self.max_dex_mod = 20
