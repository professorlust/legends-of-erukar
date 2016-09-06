from erukar.engine.inventory.ChestArmor import ChestArmor

class Robes(ChestArmor):
    BaseName="Robes"
    Probability = 1

    def __init__(self):
        super().__init__("Robes")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
