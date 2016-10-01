from erukar.engine.inventory.Armor import Armor

class Coif(Armor):
    EquipmentLocations = ['head']
    BaseName="Coif"
    Probability = 1

    def __init__(self):
        super().__init__("Coif")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
