from erukar.engine.inventory.Armor import Armor

class FrogMouthHelm(Armor):
    EquipmentLocations = ['head']
    BaseName="Frog Mouth Helm"
    Probability = 1

    def __init__(self):
        super().__init__("FrogMouthHelm")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
