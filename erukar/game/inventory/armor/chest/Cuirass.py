from erukar.engine.inventory.ChestArmor import ChestArmor

class Cuirass(ChestArmor):
    BaseName="Cuirass"
    Probability = 1

    def __init__(self):
        super().__init__("Cuirass")
        self.armor_class_modifier = 6
        self.max_dex_mod = 20
