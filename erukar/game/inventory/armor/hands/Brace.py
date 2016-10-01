from erukar.engine.inventory.Armor import Armor

class Brace(Armor):
    EquipmentLocations = ['arms']
    BaseName="Brace"
    Probability = 1

    def __init__(self):
        super().__init__("Brace")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
