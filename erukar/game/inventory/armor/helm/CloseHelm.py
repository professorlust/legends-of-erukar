from erukar.engine.inventory.HeadArmor import HeadArmor

class CloseHelm(HeadArmor):
    Probability = 1

    def __init__(self):
        super().__init__("CloseHelm")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
