from erukar.engine.inventory.ChestArmor import ChestArmor

class Brigandine(ChestArmor):
    BaseName="Brigandine"
    Probability = 1

    def __init__(self):
        super().__init__("Brigandine")
        self.armor_class_modifier = 5
        self.max_dex_mod = 20
