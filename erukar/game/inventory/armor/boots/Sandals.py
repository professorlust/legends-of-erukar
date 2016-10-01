from erukar.engine.inventory.Armor import Armor

class Sandals(Armor):
    EquipmentLocations = ['feet']
    BaseName="Sandals"
    Probability = 1

    def __init__(self):
        super().__init__("Sandals")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


