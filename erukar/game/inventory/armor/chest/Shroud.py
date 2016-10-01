from erukar.engine.inventory.Armor import Armor

class Shroud(Armor):
    EquipmentLocations = ['chest']
    BaseName="Shroud"
    Probability = 1

    def __init__(self):
        super().__init__("Shroud")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
