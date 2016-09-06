from erukar.engine.inventory.HeadArmor import HeadArmor

class Barbute(HeadArmor):
    BaseName="Barbute"
    Probability = 1

    def __init__(self):
        super().__init__("Barbute")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
