from erukar.engine.inventory.LegArmor import LegArmor

class Legwraps(LegArmor):
    BaseName="Legwraps"
    Probability = 1

    def __init__(self):
        super().__init__("Legwraps")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
