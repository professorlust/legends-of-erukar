from erukar.engine.inventory.Armor import Armor

class CloseHelm(Armor):
    EquipmentLocations = ['head']
    BaseName="Close Helm"
    Probability = 1

    def __init__(self):
        super().__init__("CloseHelm")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
