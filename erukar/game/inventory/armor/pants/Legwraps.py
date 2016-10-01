from erukar.engine.inventory.Armor import Armor

class Legwraps(Armor):
    EquipmentLocations = ['legs']
    BaseName="Legwraps"
    Probability = 1

    def __init__(self):
        super().__init__("Legwraps")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
