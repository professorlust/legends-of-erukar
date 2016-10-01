from erukar.engine.inventory.Armor import Armor

class Cuirass(Armor):
    EquipmentLocations = ['chest']
    BaseName="Cuirass"
    Probability = 1

    def __init__(self):
        super().__init__("Cuirass")
        self.armor_class_modifier = 6
        self.max_dex_mod = 20
