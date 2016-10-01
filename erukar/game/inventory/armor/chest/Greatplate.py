from erukar.engine.inventory.Armor import Armor

class Greatplate(Armor):
    EquipmentLocations = ['chest']
    BaseName="Greatplate"
    Probability = 1

    def __init__(self):
        super().__init__("Greatplate")
        self.armor_class_modifier = 10
        self.max_dex_mod = 20
