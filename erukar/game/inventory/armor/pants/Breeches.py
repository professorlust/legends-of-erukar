from erukar.engine.inventory.LegArmor import LegArmor

class Breeches(LegArmor):
    BaseName="Breeches"
    Probability = 1

    def __init__(self):
        super().__init__("Breeches")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
