from erukar.engine.inventory.Armor import Armor

class Plackart(Armor):
    EquipmentLocations = ['chest']
    BaseName="Plackart"
    Probability = 1

    def __init__(self):
        super().__init__("Plackart")
        self.armor_class_modifier = 5
        self.max_dex_mod = 20
