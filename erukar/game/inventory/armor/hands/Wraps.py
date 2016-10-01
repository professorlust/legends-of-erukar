from erukar.engine.inventory.Armor import Armor

class Wraps(Armor):
    EquipmentLocations = ['arms']
    BaseName="Wraps"
    Probability = 1

    def __init__(self):
        super().__init__("Wraps")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
