from erukar.engine.inventory.ChestArmor import ChestArmor

class Plackart(ChestArmor):
    BaseName="Plackart"
    Probability = 1

    def __init__(self):
        super().__init__("Plackart")
        self.armor_class_modifier = 5
        self.max_dex_mod = 20
