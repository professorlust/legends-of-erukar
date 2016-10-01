from erukar.engine.inventory.Armor import Armor

class Plate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Plate"
    Probability = 1

    def __init__(self):
        super().__init__("Plate")
        self.armor_class_modifier = 9
        self.max_dex_mod = 20
