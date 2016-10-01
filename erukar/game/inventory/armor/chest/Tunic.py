from erukar.engine.inventory.Armor import Armor

class Tunic(Armor):
    EquipmentLocations = ['chest']
    BaseName="Tunic"
    Probability = 1

    def __init__(self):
        super().__init__("Tunic")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
