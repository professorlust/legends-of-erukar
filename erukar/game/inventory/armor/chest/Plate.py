from erukar.engine.inventory.ChestArmor import ChestArmor

class Plate(ChestArmor):
    BaseName="Plate"
    Probability = 1

    def __init__(self):
        super().__init__("Plate")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
