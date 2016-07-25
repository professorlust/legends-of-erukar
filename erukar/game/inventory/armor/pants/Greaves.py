from erukar.engine.inventory.LegArmor import LegArmor

class Greaves(LegArmor):
    Probability = 1

    def __init__(self):
        super().__init__("Greaves")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
