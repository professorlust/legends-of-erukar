from erukar.engine.inventory.ChestArmor import ChestArmor

class Greatplate(ChestArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Greatplate")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
