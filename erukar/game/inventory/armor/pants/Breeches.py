from erukar.engine.inventory.Armor import Armor

class Breeches(Armor):
    EquipmentLocations = ['legs']
    BaseName="Breeches"
    Probability = 1

    def __init__(self):
        super().__init__("Breeches")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
