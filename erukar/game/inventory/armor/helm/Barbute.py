from erukar.engine.inventory.Armor import Armor

class Barbute(Armor):
    EquipmentLocations = ['head']
    BaseName="Barbute"
    Probability = 1

    def __init__(self):
        super().__init__("Barbute")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
