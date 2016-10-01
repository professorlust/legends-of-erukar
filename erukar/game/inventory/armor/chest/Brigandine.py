from erukar.engine.inventory.Armor import Armor

class Brigandine(Armor):
    EquipmentLocations = ['chest']
    BaseName="Brigandine"
    Probability = 1

    def __init__(self):
        super().__init__("Brigandine")
        self.armor_class_modifier = 5
        self.max_dex_mod = 20
