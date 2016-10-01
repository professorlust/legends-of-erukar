from erukar.engine.inventory.Armor import Armor

class Warboots(Armor):
    EquipmentLocations = ['feet']
    BaseName="Warboots"
    Probability = 1

    def __init__(self):
        super().__init__("Warboots")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


