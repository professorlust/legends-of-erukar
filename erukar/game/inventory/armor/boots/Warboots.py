from erukar.engine.inventory.FootArmor import FootArmor

class Warboots(FootArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Warboots")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


