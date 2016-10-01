from erukar.engine.inventory.Armor import Armor

class Gauntlets(Armor):
    EquipmentLocations = ['arms']
    BaseName="Gauntlets"
    Probability = 1

    def __init__(self):
        super().__init__("Gauntlets")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
