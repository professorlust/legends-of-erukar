from erukar.engine.inventory.HeadArmor import HeadArmor

class Cap(HeadArmor):
    BaseName="Cap"
    Probability = 1

    def __init__(self):
        super().__init__("Cap")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
