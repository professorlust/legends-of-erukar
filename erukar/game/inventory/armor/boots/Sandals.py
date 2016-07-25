from erukar.engine.inventory.FootArmor import FootArmor

class Sandals(FootArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Sandals")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


