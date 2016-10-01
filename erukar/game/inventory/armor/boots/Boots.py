from erukar.engine.inventory.Armor import Armor

class Boots(Armor):
    EquipmentLocations = ['feet']
    Probability = 1
    BaseName = "Boots"

    def __init__(self):
        super().__init__("Boots")
        self.armor_class_modifier = 1
        self.max_dex_mod = 15
