from erukar.engine.inventory.Armor import Armor

class Raiment(Armor):
    EquipmentLocations = ['chest']
    BaseName="Raiment"
    Probability = 1

    def __init__(self):
        super().__init__("Raiment")
        self.armor_class_modifier = 3
        self.max_dex_mod = 20
