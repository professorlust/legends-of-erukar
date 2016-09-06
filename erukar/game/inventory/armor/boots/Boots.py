from erukar.engine.inventory.FootArmor import FootArmor

class Boots(FootArmor):
    Probability = 1
    BaseName = "Boots"

    def __init__(self):
        super().__init__("Boots")
        self.armor_class_modifier = 1
        self.max_dex_mod = 15
