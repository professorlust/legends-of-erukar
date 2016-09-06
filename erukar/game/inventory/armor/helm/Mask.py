from erukar.engine.inventory.HeadArmor import HeadArmor

class Mask(HeadArmor):
    BaseName="Mask"
    Probability = 1

    def __init__(self):
        super().__init__("Mask")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
