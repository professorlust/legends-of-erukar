from erukar.engine.inventory.LegArmor import LegArmor

class Legplates(LegArmor):
    BaseName="Legplates"
    Probability = 1

    def __init__(self):
        super().__init__("Legplates")
        self.armor_class_modifier = 0
        self.max_dex_mod = 20
