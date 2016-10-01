from erukar.engine.inventory.Armor import Armor

class Mask(Armor):
    EquipmentLocations = ['head']
    BaseName="Mask"
    Probability = 1

    def __init__(self):
        super().__init__("Mask")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
