from erukar.engine.inventory.Armor import Armor

class Armet(Armor):
    EquipmentLocations = ['head']
    BaseName="Armet"
    Probability = 1

    def __init__(self):
        super().__init__("Armet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
