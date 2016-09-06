from erukar.engine.inventory.HeadArmor import HeadArmor

class FrogMouthHelm(HeadArmor):
    BaseName="Frog Mouth Helm"
    Probability = 1

    def __init__(self):
        super().__init__("FrogMouthHelm")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
