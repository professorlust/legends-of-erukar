from erukar.engine.inventory.Armor import Armor

class Vest(Armor):
    EquipmentLocations = ['chest']
    BaseName="Vest"
    Probability = 1

    def __init__(self):
        super().__init__("Vest")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
