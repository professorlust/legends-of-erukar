from erukar.engine.inventory.Armor import Armor

class GreatHelm(Armor):
    EquipmentLocations = ['head']
    BaseName="Great Helm"
    Probability = 1

    def __init__(self):
        super().__init__("GreatHelm")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
