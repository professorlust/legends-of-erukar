from erukar.engine.inventory.FootArmor import FootArmor

class Footguards(FootArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Footguards")
        self.armor_class_modifier = 2
        self.max_dex_mod = 10

