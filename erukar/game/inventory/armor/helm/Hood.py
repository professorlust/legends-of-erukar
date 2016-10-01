from erukar.engine.inventory.Armor import Armor

class Hood(Armor):
    EquipmentLocations = ['head']
    BaseName="Hood"
    Probability = 1

    def __init__(self):
        super().__init__("Hood")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
