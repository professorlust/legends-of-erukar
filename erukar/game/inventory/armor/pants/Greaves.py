from erukar.engine.inventory.Armor import Armor

class Greaves(Armor):
    EquipmentLocations = ['legs']
    BaseName="Greaves"
    Probability = 1

    def __init__(self):
        super().__init__("Greaves")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
