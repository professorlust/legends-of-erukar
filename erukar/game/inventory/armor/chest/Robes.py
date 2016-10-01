from erukar.engine.inventory.Armor import Armor

class Robes(Armor):
    EquipmentLocations = ['chest']
    BaseName="Robes"
    Probability = 1

    def __init__(self):
        super().__init__("Robes")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
