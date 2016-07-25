from erukar.engine.inventory.FootArmor import FootArmor

class Spurs(FootArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Spurs")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20


