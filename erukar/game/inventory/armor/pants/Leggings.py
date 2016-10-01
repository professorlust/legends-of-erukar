from erukar.engine.inventory.Armor import Armor

class Leggings(Armor):
    BaseName="Leggings"
    Probability = 1

    def __init__(self):
        super().__init__("Leggings")
        self.equipment_locations = ['legs']
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
