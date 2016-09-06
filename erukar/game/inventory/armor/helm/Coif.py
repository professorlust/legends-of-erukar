from erukar.engine.inventory.HeadArmor import HeadArmor

class Coif(HeadArmor):
    BaseName="Coif"
    Probability = 1

    def __init__(self):
        super().__init__("Coif")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
