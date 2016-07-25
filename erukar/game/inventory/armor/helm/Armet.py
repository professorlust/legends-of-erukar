from erukar.engine.inventory.HeadArmor import HeadArmor

class Armet(HeadArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Armet")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
