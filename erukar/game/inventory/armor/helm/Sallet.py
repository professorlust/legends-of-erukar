from erukar.engine.inventory.Armor import Armor

class Sallet(Armor):
    EquipmentLocations = ['head']
    BaseName="Sallet"
    Probability = 1

    def __init__(self):
        super().__init__("Sallet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
