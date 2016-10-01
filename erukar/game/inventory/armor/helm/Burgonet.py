from erukar.engine.inventory.Armor import Armor

class Burgonet(Armor):
    EquipmentLocations = ['head']
    BaseName="Burgonet"
    Probability = 1

    def __init__(self):
        super().__init__("Burgonet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
