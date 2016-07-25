from erukar.engine.inventory.ChestArmor import ChestArmor

class Plackart(ChestArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Plackart")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
