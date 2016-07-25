from erukar.engine.inventory.HeadArmor import HeadArmor

class Sallet(HeadArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Sallet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
